
export async function getResponseFromAI(sessionID, input) {
    try {
        const response = await fetch('http://127.0.0.1:5000/chatbot', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sessionID, input }),
        });

        // Parse the JSON response
        const data = await response.json();
        
        // Log the response from AI
        //console.log("The response from AI is:", data);
        return data.result; 
    } catch (error) {
        console.error('Error Grabbing Response From AI:', error);
    }
}


export async function generateConversationTitle(sessionID, input) {
    try {
        const response = await fetch('http://127.0.0.1:5000/gtitle', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sessionID, input }),
        });

        // Parse the JSON response
        const data = await response.json();
        
        // Log the response from AI
        //console.log("The title from AI is:", data);
        return data.result;  
    } catch (error) {
        console.error('Error Generating Title:', error);
    }
}

export async function generateProjectRequirement(sessionID, level, application, alg ) {
    /*fetch(`http://127.0.0.1:5000/gproject`, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sessionID, level, application, alg }),
    })
    .then(response => response.json())
    .then(data => {
        return data.result;
    })
    .catch(error => console.error('Error Generating Requirement:', error));*/
    try {
        const response = await fetch('http://127.0.0.1:5000/gproject', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sessionID, level, application, alg }),
        });

        // Parse the JSON response
        const data = await response.json();
        
        // Log the response from AI
        //console.log("The title from AI is:", data);
        return data.result;  
    } catch (error) {
        console.error('Error Generating Requirement:', error);
    }
}

export async function getProjectAssistantResponse(sessionID, input, projectRequirement ) {
    /*fetch(`http://127.0.0.1:5000/codingchatbot`, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sessionID, input, projectRequirement  }),
    })
    .then(response => response.json())
    .then(data => {
        return data.result;
    })
    .catch(error => console.error('Error Grabbing Response From Coding Assistant AI:', error));*/
    try {
        const response = await fetch('http://127.0.0.1:5000/codingchatbot', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sessionID, input, projectRequirement  }),
        });

        // Parse the JSON response
        const data = await response.json();
        return data.result;  
    } catch (error) {
        console.error('Error Grabbing Response From Coding Assistant AI:', error);
    }
}