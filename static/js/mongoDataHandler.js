export async function loadData() {
  let USERID = getGoogleID("googleID");
  let userData;

  // Change the URL to your MongoDB API endpoint
  await fetch(`http://127.0.0.1:5000/users`)
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          userData = data[USERID];
      })
      .catch(error => console.error('There has been a problem with your fetch operation:', error));
    return userData;
}

export async function replaceData(USERID, googleID, firstName, lastName, email, chatBotConversations, canvasConversations) {
  // Send the updated conversations to the MongoDB API
  const response = await fetch(`http://127.0.0.1:5000/users`, {
      method: 'PUT', // Use PUT method to update the user data
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ USERID, googleID, firstName, lastName, email, chatBotConversations, canvasConversations }),
  });

  if (response.ok) {
      console.log('User data updated successfully');
  } else {
      alert('Error updating user data');
  }
}

export async function generateUserData(USERID, googleID, firstName, lastName, email) {
  const response = await fetch('http://127.0.0.1:5000/users', { // Use the correct endpoint to add a new user
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ USERID, googleID, firstName, lastName, email }),
  });

  if (response.ok) {
      console.log('User added successfully');
  } else {
      alert('Error adding user');
  }
}

export function getSessionID() {
    return crypto.randomUUID();
}


function getGoogleID(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}
