const API = '/api/alerts/';

console.log("alerts.js loaded");

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

const patient_id = patient?.patient_id;

// Load alerts
async function loadAlerts() {
  if (!patient_id) return;

  const res = await fetch(`${API}?patient_id=${patient_id}`);
  const alerts = await res.json();
  const tbody = document.getElementById('alertsBody');
  tbody.innerHTML = '';

  console.log("Fetched alerts:", alerts);

  if (alerts.length > 0) {
    alerts.forEach(alert => {
      console.log("Alert object:", alert); 

      const tr = document.createElement('tr');
      tr.dataset.alertId = alert.id || alert._id; 

      tr.innerHTML = `
        <td contenteditable="false">${alert.sensor_type}</td>
        <td>${alert.measured_value ?? ''}</td>
        <td contenteditable="false">${alert.threshold_value}</td>
        <td contenteditable="false">${alert.comparison}</td>
        <td contenteditable="false">${alert.message}</td>
        <td>${alert.is_sent}</td>
        <td>${alert.timestamp ? new Date(alert.timestamp).toLocaleString() : ''}</td>
        <td>
          <div class="actions">
            <button class='edit-btn' id="edit-btn">Edit</button>
            <button class='save-btn' id="save-btn" style="display:none;">Save</button>
            <button class='delete-btn' id="delete-btn">
                <i class="fas fa-trash" aria-hidden="true"></i>
            </button>
            </div>
        </td>
      `;

      tbody.appendChild(tr);
    });

    attachEditListeners();
  } else {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;">No alerts found.</td></tr>';
  }
}

function attachEditListeners() {
  // Edit
  document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.onclick = () => {
      const row = btn.closest('tr');
      row.querySelectorAll('td[contenteditable]').forEach(td => td.contentEditable = true);
      btn.style.display = 'none';
      row.querySelector('.save-btn').style.display = 'inline-block';
    };
  });

  // Save
  document.querySelectorAll('.save-btn').forEach(btn => {
    btn.onclick = async () => {
      const row = btn.closest('tr');
      const alertId = row.dataset.alertId;
      const cells = row.querySelectorAll('td');

      const payload = {
        sensor_type: cells[0].innerText.trim(),
        threshold_value: parseFloat(cells[2].innerText),
        comparison: cells[3].innerText.trim(),
        message: cells[4].innerText.trim()
      };

      console.log('Updating alert', alertId, payload);

      const res = await fetch(`/api/alerts/${alertId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        alert("Alert updated.");
        loadAlerts();
      } else {
        console.error('Failed to update alert');
        alert("Update failed.");
      }
    };
  });

  // Delete
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.onclick = async () => {
      const row = btn.closest('tr');
      const alertId = row.dataset.alertId;
      if (!confirm('Are you sure you want to delete this alert?')) return;

      console.log('Deleting alert', alertId);

      const res = await fetch(`/api/alerts/${alertId}`, {
        method: 'DELETE'
      });

      if (res.ok) {
        alert('Alert deleted.');
        loadAlerts();
      } else {
        console.error('Failed to delete alert', await res.text());
        alert('Delete failed.');
      }
    };
  });
}

// Create new alert
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('alertForm');

  form?.addEventListener('submit', async e => {
    e.preventDefault();

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

  loadAlerts();
});
