let googleID = getGoogleID("googleID");

function toggleMenu() {
    const dropdown = document.getElementById('dropdown');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

function toggleProfile() {
    const profile = document.getElementById('profile');
    profile.style.display = profile.style.display === 'block' ? 'none' : 'block';
}

async function loadHeader(){
    await fetch('../static/dropDownHeader.html')
      .then(response => response.text())
      .then(data => {
        document.getElementById('TopHeader').innerHTML = data;
      });
      const dropdown = document.getElementById('dropdown');
    addMenu();
    addProfile();
}

function getGoogleID(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
  }

function addMenu(){
    const dropdown = document.getElementById('dropdown');
    const a1 = document.createElement('a');
    const a4 = document.createElement('a');
    const a5 = document.createElement('a');
    a1.href = `../../about?googleID=${encodeURIComponent(googleID)}`
    a4.href = `../../canvas?googleID=${encodeURIComponent(googleID)}`
    a5.href = `../../ai?googleID=${encodeURIComponent(googleID)}`

    a1.innerHTML = "About";
    a4.innerHTML = "Canvas";
    a5.innerHTML = "Chat Bot";
    dropdown.appendChild(a1);
    dropdown.appendChild(a4);
    dropdown.appendChild(a5);
}

function addProfile(){
    const profile = document.getElementById('profile');
    const a1 = document.createElement('a');
    const a2 = document.createElement('button');
    a1.href = `../../profile?googleID=${encodeURIComponent(googleID)}`
    a2.onclick = function() {
        window.location.href = "../../";
    }
    a1.innerHTML = "Profile";
    a2.innerHTML = "Logout";
    a2.id = "logout";
    profile.appendChild(a1);
    profile.appendChild(a2);
}

window.addEventListener('click', function(event) {
    const dropdown = document.getElementById('dropdown');
    const profile = document.getElementById('profile');
    const menuButton = document.querySelector('.menu-button');
    const profileButton = document.querySelector('.profile-button');
    if (!dropdown.contains(event.target) && !menuButton.contains(event.target)) {
        dropdown.style.display = 'none';
    }
    if (!profile.contains(event.target) && !profileButton.contains(event.target)) {
        profile.style.display = 'none';
    }
});
loadHeader();

