const patient = JSON.parse(localStorage.getItem("patient"));

function isTokenExpired(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const now = Math.floor(Date.now() / 1000);
    return payload.exp < now;
  } catch (e) {
    console.error("Error decoding token:", e);
    return true;
  }
}

if (!patient || isTokenExpired(patient.access_token)) {
  localStorage.removeItem("patient");
  window.location.href = "/";
}

const token = patient?.access_token;

async function loadSettings() {
  const res = await fetch("/api/patient/current", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (res.ok) {
    const data = await res.json();

    document.getElementById('username').value = data.username || '';
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

function toggleFields(enabled) {
  const fields = ['phone_number', 'dob', 'height', 'weight', 'biological_gender'];
  fields.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.disabled = !enabled;
  });
}

document.getElementById("editSaveButton").addEventListener("click", async () => {
  const button = document.getElementById("editSaveButton");
  const isEditing = button.textContent === "Edit";

  if (isEditing) {
    // Enable fields for editing
    toggleFields(true);
    button.textContent = "Save Changes";
  } else {
    // Save changes
    const updatedData = {
      username: document.getElementById('username').value,
      email: document.getElementById('email').value,
      phone_number: document.getElementById('phone_number').value,
      dob: document.getElementById('dob').value,
      height: document.getElementById('height').value,
      weight: document.getElementById('weight').value,
      biological_gender: document.getElementById('biological_gender').value,
    };

    const res = await fetch("/api/patient/update", {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(updatedData),
    });

    if (res.ok) {
      alert("Your settings have been updated.");
      loadSettings();
      toggleFields(false);
      button.textContent = "Edit";
    } else {
      const error = await res.json();
      alert(`Failed to update: ${error.error}`);
    }
  }
});

loadSettings();
