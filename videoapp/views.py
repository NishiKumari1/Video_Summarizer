from django.shortcuts import render
import re
import markdown2
from django.http import HttpResponse
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from .web_config import GOOGLE_API_KEY, GOOGLE_MODEL

genai.configure(api_key=GOOGLE_API_KEY)

# Create your views here.

def extract_video_id(url):
    """function for video Summarization"""
    match = re.search(r"(?<=v=)[\w-]+|(?<=youtu.be/)[\w-]+", url)
    if match:
        return match.group(0)
    return HttpResponse(status_code=400, detail="Invalid YouTube URL")


def get_video_transcript(video_id):
    """Method to get video transcript"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        full_transcript = ""
        for entry in transcript:
            text = entry["text"]
            full_transcript += f"{text}\n"
        return full_transcript

    except Exception as e:
        return HttpResponse(status=500, content=f"An error occurred: {e}")
    
def video_summarization(request):
    """Method to summarize video"""
    if request.method == "POST":
        try:
            video_url = request.POST.get("video_url")
            video_id = extract_video_id(video_url)
            transcript = get_video_transcript(video_id)

            # Use Generative AI Gemini Pro for both main summary and descriptive summary
            model = genai.GenerativeModel(GOOGLE_MODEL)
            
            # Generate main summary headings
            response = model.generate_content(
                f"""Given a video, create a set of main summary headings.
                    Transcript:
                    {transcript}
                    """
            )
            summary = markdown2.markdown(response.text)
            # Generate descriptive summary without timestamp
            descriptive_response = model.generate_content(
                f"""
                Given a video, create a descriptive summary of this video without timestamp,
                a detailed explanation of the given video.
                Transcript:{transcript}.
                """
            )
            descriptive_summary = markdown2.markdown(descriptive_response.text)

            return render(
                request,
                "video_summarizer.html",
                {"summary": summary, "descriptive_summary": descriptive_summary},
            )
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return HttpResponse("An error occurred while processing your request.")
    
    return render(request, "video_summarizer.html")
