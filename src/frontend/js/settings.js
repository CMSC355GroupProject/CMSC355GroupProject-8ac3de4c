const token = JSON.parse(localStorage.getItem("patient"))?.access_token;

async function loadSettings() {
  const res = await fetch("/api/patient/current", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (res.ok) {
    const data = await res.json();
    // can add all of these fields: 
    // "username": "joey_testing_new66",
    // "email": "joey_test_new66@gmail.com",
    // "password": "password",
    // "dob": "01-30-1997",
    // "height": 180,
    // "weight": 75,
    // "biological_gender": "male",
    // "phone_number": "+15555551234"
    
    
    document.getElementById('username').value = data.username || '';
    document.getElementById('email').value = data.email || '';
    document.getElementById('password').value = data.password || '';
    document.getElementById('dob').value = data.dob || '';
    document.getElementById('height').value = data.height || '';
    document.getElementById('weight').value = data.weight || '';
    document.getElementById('biological_gender').value = data.biological_gender || '';
    document.getElementById('phone_number').value = data.email || '';
  } else {
    alert("Failed to load settings.");
  }
}

document.getElementById("settingsForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  alert("Update Functionality Not Built Yet.");
});

loadSettings();
