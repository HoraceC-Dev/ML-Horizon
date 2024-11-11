import { loadData, replaceData, getSessionID } from "../js/mongoDataHandler.js";
import { getResponseFromAI, generateConversationTitle } from "../js/chatbotDataHandler.js";
import { createThinkingAnimation, deleteThinkingAnimation } from "../js/thinking.js";

const messagesContainer = document.getElementById('messages');
const inputField = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const newChatButton = document.getElementById('new-chat-button'); // New chat button
const conversationList = document.getElementById('conversation-list');
let userData;
let USERID;

let conversations = {};
let sessionIDs = [];
let titles = {};
let currentSessionID; //CHANGE NEEDED
let currentConversationIndex = 0;


// Function to add a new message
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
    disableAllClicks();
    //toggleInput();
    if (userInput) {
        const mc = createMessageContainer(true);
        addMessage(userInput, mc[0], false);
        inputField.value = '';    
        //setTimeout(() => {
            if (currentConversationIndex === Object.keys(conversations).length) {currentSessionID = newSessionID();} // NEEDS UPDATE
            const botResponse = await getResponseFromAI( currentSessionID, userInput);
            //const botResponse = "Bot responding to: " + userInput;

            deleteThinkingAnimation();
            await addMessage(botResponse, mc[1], true);
            await saveConversation(userInput, botResponse, currentSessionID);
            enableAllClicks();
            //toggleInput();
        //}, 1000);
    }else{
        enableAllClicks();
        //toggleInput();
    }
});

// Allow sending message with Enter key
inputField.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendButton.click(); // Trigger the click event
    }
});

function toggleInput() {
    let disabled = sendButton.disabled;
    if(!disabled) {
        sendButton.disabled = true;
        sendButton.style.backgroundColor = "#3f3a3a";
    }else{
        sendButton.disabled = false;
        sendButton.style.backgroundColor = "#357ab8";
    }
}

// Save conversation
async function saveConversation(userMessage, botResponse, sessionID) {
    // Create a new conversation or update the current one
    if (currentConversationIndex === Object.keys(conversations).length) {
        sessionIDs.push(sessionID.toString());
        conversations[sessionID] = [[userMessage, botResponse]];
        currentConversationIndex = Object.keys(conversations).length - 1;
        await generateTitle(sessionID, userMessage);
        updateConversationList();
    } else {
        conversations[sessionIDs[currentConversationIndex]].push([userMessage, botResponse]);
    }
    const conv = {"sessionIDs" : sessionIDs, "conversations": conversations, "titles": titles};
    replaceData(USERID, undefined, undefined, undefined, undefined, conv, undefined);
}

function newSessionID() { //TEMPORARY
    return getSessionID();
}


async function generateTitle(sessionID, input) {
    const title = await generateConversationTitle(sessionID, input);
    if(title) {titles[sessionID] = title;}
    else {titles[sessionID] = input};
}

// Update the conversation list in the sidebar
function updateConversationList() {  //might change sessionid
    conversationList.innerHTML = '';
    Object.keys(conversations).forEach((sessionID) => {
        const conv = conversations[sessionID];
        const listItem = document.createElement('pre');
        //listItem.textContent = conv[0][0].substring(0,1).toUpperCase() + conv[0][0].substring(1);
        listItem.textContent = titles[sessionID];
        listItem.addEventListener('click', () => displayConversation(sessionIDs.indexOf(sessionID)));
        conversationList.appendChild(listItem);
    });
}

// Display selected conversation in the chat area
function displayConversation(index) {
    currentConversationIndex = index;
    currentSessionID = sessionIDs[currentConversationIndex];
    messagesContainer.innerHTML = ''; // Clear current messages
    conversations[sessionIDs[index]].forEach(([userMessage, botMessage]) => {
        const mc = createMessageContainer(false);
        addMessage(userMessage, mc[0], false);
        addMessage(botMessage, mc[1], false);
    });
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Function to start a new chat
function startNewChat() {
    inputField.value = '';
    messagesContainer.innerHTML = '';
    currentConversationIndex = Object.keys(conversations).length; // Reset current conversation index
}

function typeAnimation(text, textContainer) {
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


// New chat button event
newChatButton.addEventListener('click', startNewChat);

// Initialize the app

async function init() {
    userData = await loadData();
    USERID = userData["USERID"];
    //userData = getDocument(getGoogleID());
    const convs = userData["chatBotConversations"]; //A Map from {sessionID: Conversation}
    if (Object.keys(convs).length > 0) {
        conversations = convs["conversations"];
        sessionIDs = convs["sessionIDs"];
        titles = convs["titles"];
        currentConversationIndex = Object.keys(conversations).length -1;
        updateConversationList();
        displayConversation(currentConversationIndex);
    }
    if (sessionIDs.length == 0) {
        currentSessionID = newSessionID().toString();
        sessionIDs.push(currentSessionID.toString());
    }
}

function disableAllClicks() {
    document.body.style.pointerEvents = "none";
}

// Function to enable clicking on all clickable elements
function enableAllClicks() {
    document.body.style.pointerEvents = "auto";
}



// Call init to set up anything needed on load
init();
