const patient = JSON.parse(localStorage.getItem("patient"));

function isTokenExpired(token) {
  try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const now = Math.floor(Date.now() / 1000); // current time in seconds
      return payload.exp < now;
  } catch (e) {
      console.error("Error decoding token:", e);
      return true; // fail-safe: assume expired
  }
  }
  
if (!patient || isTokenExpired(patient.access_token)) {
  localStorage.removeItem("patient");
  window.location.href = "/";
}

const token = JSON.parse(localStorage.getItem("patient"))?.access_token;

async function loadSettings() {
  const res = await fetch("/api/patient/current", {
    headers: { Authorization: `Bearer ${token}` },
  });

  

  if (res.ok) {
    const data = await res.json();
    console.log('data',data);

    document.getElementById('username').value = data.username || '';
    // document.getElementById("name").value = data.name || "";
    document.getElementById("email").value = data.email || "";
    document.getElementById("phone_number").value = data.phone_number || "";
    document.getElementById('dob').value = data.dob || '';
    document.getElementById('height').value = data.height || '';
    document.getElementById('weight').value = data.weight || '';
    document.getElementById('biological_gender').value = data.biological_gender || '';
  } else {
    alert("Failed to load settings.");
  }
}

document.getElementById("settingsForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  alert("Update Functionality Not Built Yet.");
});

loadSettings();
