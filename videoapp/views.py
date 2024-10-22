# videoapp/views.py
import logging
from django.shortcuts import render
import re
from django.http import HttpResponse
from django.conf import settings
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import markdown2

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GOOGLE_API_KEY)
GOOGLE_MODEL = settings.GOOGLE_MODEL

def extract_video_id(url):
    match = re.search(r"(?<=v=)[\w-]+|(?<=youtu.be/)[\w-]+", url)
    if match:
        return match.group(0)
    raise ValueError("Invalid YouTube URL")

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        return " ".join(entry["text"] for entry in transcript)
    except Exception as e:
        logger.error(f"Error getting transcript: {str(e)}")
        raise

def video_summarization(request):
    if request.method == "POST":
        video_url = request.POST.get("video_url")
        try:
            video_id = extract_video_id(video_url)
            transcript = get_video_transcript(video_id)

            model = genai.GenerativeModel(GOOGLE_MODEL)
            
            summary_prompt = f"Given a video, create a set of main summary headings. Transcript: {transcript}"
            summary_response = model.generate_content(summary_prompt)
            summary = markdown2.markdown(summary_response.text)
            
            descriptive_prompt = f"Given a video, create a descriptive summary of this video without timestamp, a detailed explanation of the given video. Transcript: {transcript}"
            descriptive_response = model.generate_content(descriptive_prompt)
            descriptive_summary = markdown2.markdown(descriptive_response.text)

            return render(
                request,
                "video_summarizer.html",
                {"summary": summary, "descriptive_summary": descriptive_summary, "video_url": video_url}
            )
        except ValueError as ve:
            logger.error(f"Invalid URL: {str(ve)}")
            return render(request, "video_summarizer.html", {"error": "Invalid YouTube URL. Please check the URL and try again."})
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return render(request, "video_summarizer.html", {"error": "An error occurred while processing your request. Please try again later."})
    
    return render(request, "video_summarizer.html")
