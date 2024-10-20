// pop-up loading
document.addEventListener("DOMContentLoaded", function () {
    // Get the "Generate" button using the class
    const generateButton = document.querySelector('.load');
  
    // Attach a click event listener to the "Generate" button
    generateButton.addEventListener("click", function () {
      // Show the loading overlay
      document.getElementById("loading-overlay").style.display = "flex";
    });
  
    // Hide the loading overlay when the page finishes loading
    window.addEventListener("load", function () {
      document.getElementById("loading-overlay").style.display = "none";
    });
  });


