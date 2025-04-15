const API = '/api/alerts/';

console.log("alerts.js loaded");

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

// Get the patient_id from localStorage to filter alerts
const patient_id = patient ? patient.patient_id : null;

// Load existing alerts for the current patient
async function loadAlerts() {
  if (patient_id) {
    const res = await fetch(`${API}?patient_id=${patient_id}`);
    const alerts = await res.json();
    const tbody = document.getElementById('alertsBody');
    tbody.innerHTML = '';

    if (alerts.length > 0) {
      alerts.forEach(a => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${a.sensor_type || ''}</td>
          <td>${a.measured_value ?? ''}</td>
          <td>${a.threshold_value ?? ''}</td>
          <td>${a.comparison || ''}</td>
          <td>${a.message || ''}</td>
          <td>${a.is_sent}</td>
          <td>${a.timestamp ? new Date(a.timestamp).toLocaleString() : ''}</td>
        `;
        tbody.appendChild(tr);
      });
    } else {
      tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">No alerts found.</td></tr>';
    }
  } else {
    // If patient_id is missing, redirect to login
    alert("Patient data is missing. Please log in again.");
    window.location.href = "/";
  }
}

// Handle alert form submission
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('alertForm');

  if (!form) {
    console.error("alertForm not found in DOM");
    return;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!patient || !patient.patient_id) {
      alert('Patient ID missing from localStorage');
      return;
    }

    const payload = {
      patient_id: patient.patient_id,
      sensor_type: form.sensor_type.value,
      threshold_value: parseFloat(form.threshold_value.value),
      comparison: form.comparison.value,
      message: form.message.value
    };

    const res = await fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      form.reset();
      loadAlerts();
    } else {
      const err = await res.json();
      console.error('Failed to create alert:', err);
      alert('Failed to create alert');
    }
  });

  // Load alerts for the current patient on page load
  loadAlerts();
});
