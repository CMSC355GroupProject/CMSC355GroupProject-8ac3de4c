const API = '/api/alerts/';

console.log("alerts.js loaded");

const patient = JSON.parse(localStorage.getItem("patient"));
console.log("Retrieved patient from localStorage outside listener:", patient);

// Load existing alerts
async function loadAlerts() {
  const res = await fetch(API);
  const alerts = await res.json();
  const tbody = document.getElementById('alertsBody');
  tbody.innerHTML = '';

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

    const patient = JSON.parse(localStorage.getItem("patient"));
    console.log("Retrieved patient from localStorage inside submit:", patient);

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

  // Load alerts on page load
  loadAlerts();
});
