import { respond } from "../js/chat.js"; 

const promptBox = document.getElementById("promptBox");
promptBox.innerHTML = '<div id="promptButton"><button id="askPrompt"">Ask AI</button></div><div id="promptPopup"><label for="promptInput">Enter your prompt:</label><br><input type="text" id="promptInput" placeholder="Type here..."><button id="submitButton">Submit</button></div>';

const promptButton = document.getElementById('promptButton');
const askPrompt = document.getElementById('askPrompt');
const promptPopup = document.getElementById('promptPopup');
const promptInput = document.getElementById('promptInput');
const submitButton = document.getElementById('submitButton');

askPrompt.addEventListener("click", () => enablePrompt());
submitButton.addEventListener("click", () => submitPrompt());

let highlightedText = "";

// Display prompt popup when text is highlighted
document.addEventListener('mouseup', () => {
  const selection = window.getSelection().toString();
  if (selection) {
    let x = event.clientX;
    let y = event.clientY;
    promptButton.style.left = `${x + window.scrollX}px`;
    promptButton.style.top = `${y + window.scrollY}px`;
    promptButton.style.display = 'block';
    promptPopup.style.display = 'none';
  } else {
    promptButton.style.display = 'none';
    promptPopup.style.display = 'none';
  }
});

function enablePrompt(){
  const selection = window.getSelection().toString().trim();
  highlightedText = selection;
  if (selection) {
    let x = event.clientX;
    let y = event.clientY;
    promptPopup.style.left = `${x + window.scrollX}px`;
    promptPopup.style.top = `${y + window.scrollY}px`;
    promptPopup.style.display = 'block';
    promptInput.value = '';
    promptInput.focus();
  } else {
    promptPopup.style.display = 'none';
  }
}
// Submit prompt function
function submitPrompt() {
  const userQuestion = promptInput.value.trim();
  if (userQuestion){
    sendPromptMessage(userQuestion + "\n based on the following text that you generated: " + highlightedText);
    promptPopup.style.display = 'none';
  }
}


function sendPromptMessage(message) {
    if (message.trim()) {
        respond(message);
    }
}


