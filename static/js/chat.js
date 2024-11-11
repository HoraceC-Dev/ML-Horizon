import { createThinkingAnimation, deleteThinkingAnimation } from "../js/thinking.js";
import { loadData, replaceData, getSessionID } from "../js/mongoDataHandler.js";
import { generateQuestion } from "../js/question.js";
import { getProjectAssistantResponse, generateProjectRequirement } from "../js/chatbotDataHandler.js";

const messagesContainer = document.getElementById('messages');
const inputField = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const requirementContainer = document.getElementById("requirement");

let userData;
let USERID;

let sessionIDs = [];
let projects = {};
let conversations = [];
let projectRequirement = "Requirement";
let currentSessionID; //CHANGE NEEDED
let currentProjectIndex = 0;

async function addMessage(text, container, animate) {
    if (animate) {
        await typeAnimation(text, container);
    }else{
        container.textContent = text;
    }
}

function createMessageContainer(thinking) { 
    const botMessageElement = document.createElement('div');
    const userMessageElement = document.createElement('div');

    userMessageElement.className = "user-message";
    const userMessage = document.createElement('pre');
    userMessage.className = "message";
    userMessageElement.appendChild(userMessage);

    botMessageElement.className = "bot-message-container";
    const botImageContainer = document.createElement('div');
    const botImage = document.createElement('img');
    const botMessageContainer = document.createElement('div');
    const botMessage = document.createElement('pre');

    const think = createThinkingAnimation();
    botImageContainer.className="bot-image-container";
    botImage.className = "bot-image";
    botMessageContainer.className = "bot-message";
    botMessage.className = "message";

    botImage.src = "../static/img/MLHorizonLogo.png";
    botImageContainer.appendChild(botImage);
    botMessageContainer.appendChild(botMessage);
    botMessageElement.appendChild(botImageContainer);
    if(thinking) {botMessageElement.appendChild(think);}
    botMessageElement.appendChild(botMessageContainer);

    messagesContainer.appendChild(userMessageElement);
    messagesContainer.appendChild(botMessageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight; // Scroll to the bottom

    return([userMessage, botMessage]);
}

sendButton.addEventListener('click', async function() {
    const userInput = inputField.value.trim();
    //toggleInput();
    disableAllClicks();
    if (userInput) {
        const mc = createMessageContainer(true);
        addMessage(userInput, mc[0], false);
        inputField.value = '';    
        //setTimeout(() => {
            if(!currentSessionID){currentSessionID = newSessionID()}; // NEED CHANGE
            const botResponse = await getProjectAssistantResponse( currentSessionID, userInput, projectRequirement);
            //const botResponse = "Bot responding to: " + userInput;

            deleteThinkingAnimation();
            await addMessage(botResponse, mc[1], true);
            await saveConversation(userInput, botResponse, currentSessionID);
            //toggleInput();
            enableAllClicks();
        //}, 1000);
    }else{
        //toggleInput();
        enableAllClicks();
    }
});

// Allow sending message with Enter key
inputField.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendButton.click(); // Trigger the click event
    }
});

// Save conversation
async function saveConversation(userMessage, botResponse, sessionID) {
    // Create a new conversation or update the current one
    if (conversations.length == 0) {
        conversations = [[userMessage, botResponse]];
    } else {
        conversations.push([userMessage, botResponse]);
    }
    projects[sessionIDs] = {"projectRequirement" : projectRequirement, "conversations": conversations};
    const canvasconv = {"sessionIDs" : sessionIDs, "projects": projects};
    replaceData(USERID, undefined, undefined, undefined, undefined, undefined, canvasconv);
}

function displayAll() {
    conversations.forEach(([userMessage, botMessage]) => {
        const mc = createMessageContainer(false);
        addMessage(userMessage, mc[0], false);
        addMessage(botMessage, mc[1], false);
    });
    requirementContainer.innerText = projectRequirement;
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}


async function typeAnimation(text, textContainer) {
    return new Promise((resolve) => { // Wrap in a Promise
        let index = 0; // Initialize the character index

        function typeCharacter() {
            if (index < text.length) {
                textContainer.textContent += text.charAt(index); // Add character
                index++; // Move to next character
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                setTimeout(typeCharacter, 5); // Call again after delay
            } else {
                resolve(); // Resolve the promise when done
            }
        }
        
        typeCharacter();
    });
}

function newSessionID() { //TEMPORARY
    return getSessionID();
}


export async function respond(input) {
    let userInput = input;
    //toggleInput();
    disableAllClicks();
    if (userInput) {
        const mc = createMessageContainer();
        addMessage(userInput, mc[0], false);  
        //setTimeout(() => {
            if(!currentSessionID){currentSessionID = newSessionID()} // NEEDS UPDATE
            const botResponse = await getProjectAssistantResponse( currentSessionID, userInput, projectRequirement);
            //const botResponse = "Bot responding to: " + userInput;
            deleteThinkingAnimation();
            await addMessage(botResponse, mc[1], true);
            await saveConversation(userInput, botResponse, currentSessionID);
            //toggleInput();
            enableAllClicks();
        //}, 1000);
    }else{
        //toggleInput();
        enableAllClicks();
    }
}

function disableAllClicks() {
    document.body.style.pointerEvents = "none";
}

// Function to enable clicking on all clickable elements
function enableAllClicks() {
    document.body.style.pointerEvents = "auto";
}

export async function createProjectRequirement(answer) {
    requirementContainer.appendChild(createThinkingAnimation());
    projectRequirement = await generateProjectRequirement(currentSessionID, answer[0], answer[1], answer[2]);
    deleteThinkingAnimation();
    await typeAnimation(projectRequirement, requirementContainer);
    //projectRequirement = answer;
    //requirementContainer.innerText = projectRequirement;
    projects[sessionIDs] = {"projectRequirement" : projectRequirement, "conversations": conversations};
    const canvasconv = {"sessionIDs" : sessionIDs, "projects": projects};
    replaceData(USERID, undefined, undefined, undefined, undefined, undefined, canvasconv);
}

// Initialize the app
async function init() {
    userData = await loadData();
    let canvasConvs;
    if(userData){   
        USERID = userData["USERID"];
        canvasConvs = userData["canvasConversations"]; 
        if (Object.keys(canvasConvs).length != 0) {
            sessionIDs = canvasConvs["sessionIDs"];
            currentSessionID = sessionIDs[0];
            conversations = canvasConvs["projects"][currentSessionID]["conversations"];
            projectRequirement = canvasConvs["projects"][currentSessionID]["projectRequirement"];
            displayAll();
        }
    }
    if (!sessionIDs || sessionIDs.length == 0) {
        generateQuestion();
        currentSessionID = newSessionID().toString();
        sessionIDs.push(currentSessionID.toString());
    }
}

// Call init to set up anything needed on load
init();
