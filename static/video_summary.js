// Get the combined text from the HTML element
const combinedTextElement = document.getElementById('descriptive_summary');
const combinedText = combinedTextElement.innerHTML.trim();
if (combinedText.length > 0) {

  // Replace the unwanted characters and split the combined text into an array of strings
  var inputList = combinedText
    .replace(/', '', '/g, ' ')
    .replace(/\['/g, '')
    .replace(/'\]/g, '')
    .replace(/", '', '/g, ' ')
    .replace(/', '', "/g, ' ')
    .replace(/', '', '/g, ' ')
    .replace(/', '', '/g, ' ');

  // Clear the content of the HTML element
  combinedTextElement.innerHTML = '';
  combinedTextElement.innerHTML = inputList;
}


// // pop-up loading
// document.addEventListener("DOMContentLoaded", function () {
//   // Get the "Generate" button using the class
//   const generateButton = document.querySelector('.border-0');

//   // Attach a click event listener to the "Generate" button
//   generateButton.addEventListener("click", function () {
//     // Show the loading overlay
//     document.getElementById("loading-overlay").style.display = "flex";
//   });

//   // Hide the loading overlay when the page finishes loading
//   window.addEventListener("load", function () {
//     document.getElementById("loading-overlay").style.display = "none";
//   });
// });
