import { loadData, replaceData } from "../js/mongoDataHandler.js";

let userData;
let USERID;

let firstName;
let lastName;
let email;

document.getElementById("editButton").addEventListener("click", function() {
    document.getElementById("firstName").disabled = false;
    document.getElementById("lastName").disabled = false;
    
    document.getElementById("editButton").style.display = "none";
    document.getElementById("saveButton").style.display = "inline-block";
    document.getElementById("cancelButton").style.display = "inline-block";
});
  
document.getElementById("saveButton").addEventListener("click", function() {
    // Save the new information (this example only saves locally in variables)
    firstName = document.getElementById("firstName").value;
    lastName = document.getElementById("lastName").value;

    // Re-disable the inputs
    document.getElementById("firstName").disabled = true;
    document.getElementById("lastName").disabled = true;

    // Hide save and cancel buttons, show edit button
    document.getElementById("editButton").style.display = "inline-block";
    document.getElementById("saveButton").style.display = "none";
    document.getElementById("cancelButton").style.display = "none";

    // Optionally send data to a backend server here
    replaceData(USERID, undefined, firstName, lastName, undefined, undefined, undefined);
});

document.getElementById("cancelButton").addEventListener("click", function() {
    // Reset to previous values (if stored in a variable)
    document.getElementById("firstName").disabled = true;
    document.getElementById("lastName").disabled = true;

    document.getElementById("firstName").value = firstName;
    document.getElementById("lastName").value = lastName;

    document.getElementById("editButton").style.display = "inline-block";
    document.getElementById("saveButton").style.display = "none";
    document.getElementById("cancelButton").style.display = "none";
});

async function init() {
    userData = await loadData();
    USERID = userData["USERID"];
    document.getElementById("firstName").value = userData["firstName"];
    document.getElementById("lastName").value = userData["lastName"];
    document.getElementById("email").value = userData["email"];
    firstName = document.getElementById("firstName").value;
    lastName = document.getElementById("lastName").value;
    email = document.getElementById("email").value;
    
}

init();