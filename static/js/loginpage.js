import { generateUserData } from './mongoDataHandler.js';

let GOOGLID;

window.onload = function () {
    google.accounts.id.initialize({
        client_id: '269449559556-dgm4fmmbl0b9mso4tkfjl8iutgnkv533.apps.googleusercontent.com',
        callback: handleCredentialResponse
    });
    google.accounts.id.renderButton(
        document.getElementById("signInDiv"),
        { theme: "outline", size: "large" }
    );
    google.accounts.id.prompt(); 
};

async function handleCredentialResponse(response) {
    const userObject = jwt_decode(response.credential);
    const email = userObject.email;
    const firstName = userObject.given_name;
    const lastName = userObject.family_name;  
    const googleID = userObject.sub;
    document.getElementById("signInDiv").style.display = "none";
    document.getElementById("welcomeMessage").textContent = `Welcome, ${firstName} ${lastName}!`;
    GOOGLID = googleID;
    generateUserData(GOOGLID, googleID, firstName, lastName, email);

    redirectToAboutPage();
}

function redirectToAboutPage() {
    window.location.href = `../../about?googleID=${encodeURIComponent(GOOGLID)}`;
  }

