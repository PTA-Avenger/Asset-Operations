// Utility function for updating charts
function updateChart(chart, newData, newLabels) {
    chart.data.datasets[0].data = newData;
    if (newLabels) {
        chart.data.labels = newLabels;
    }
    chart.update();
}

// Charts
let efficiencyChart = new Chart(document.getElementById('efficiencyChart'), {
    type: 'line',
    data: {
        labels: [], // will be set dynamically
        datasets: [{
            label: 'Efficiency (%)',
            backgroundColor: '#2980b9',
            borderColor: '#424949',
            data: [],
            fill: false,
        }]
    },
    options: { responsive: true }
});

let anomalyChart = new Chart(document.getElementById('anomalyChart'), {
    type: 'bar',
    data: {
        labels: [], // will be set dynamically
        datasets: [{
            label: 'Anomalies',
            backgroundColor: '#4a235a',
            data: []
        }]
    },
    options: { responsive: true }
});

let maintenanceChart = new Chart(document.getElementById('maintenanceChart'), {
    type: 'doughnut',
    data: {
        labels: [], // will be set dynamically
        datasets: [{
            label: 'Maintenance ETA',
            backgroundColor: ['#7fb3d5', '#7dcea0', '#f7dc6f'],
            data: []
        }]
    },
    options: { responsive: true }
});

// Initialize Leaflet map for equipment
const equipmentMap = L.map('equipmentMap').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(equipmentMap);

// Fetch equipment data and update map
async function fetchEquipmentMap() {
  const res = await fetch('/api/assets/locations');
  const data = await res.json();
  data.forEach(equipment => {
    const marker = L.marker([equipment.lat, equipment.lon])
      .addTo(equipmentMap)
      .bindPopup(`<b>${equipment.name}</b><br>Status: ${equipment.status}`);
  });
}

fetchEquipmentMap();

// Real-time sensor fetch loop
function fetchSensorData() {
    fetch('/api/sensors/latest')
        .then(response => response.json())
        .then(data => {
            document.getElementById('sensor-data').textContent = JSON.stringify(data, null, 2);

            // Update efficiency chart
            if (data.efficiency && data.efficiency.values && data.efficiency.labels) {
                updateChart(efficiencyChart, data.efficiency.values, data.efficiency.labels);
            }

            // Update anomaly chart
            if (data.anomalies && data.anomalies.values && data.anomalies.labels) {
                updateChart(anomalyChart, data.anomalies.values, data.anomalies.labels);
            }

            // Update maintenance chart
            if (data.maintenance && data.maintenance.values && data.maintenance.labels) {
                updateChart(maintenanceChart, data.maintenance.values, data.maintenance.labels);
            }
        })
        .catch(err => console.error("Error fetching sensor data:", err));
}

setInterval(fetchSensorData, 3000);
fetchSensorData();

// Report modal logic (if you want to move from template to here)
window.showReport = function(type) {
    let url, title;
    if (type === "anomaly") {
        url = "/api/anomaly_report";
        title = "Anomaly Report";
    } else if (type === "efficiency") {
        url = "/api/efficiency_report";
        title = "Efficiency Report";
    } else if (type === "downtime") {
        url = "/api/downtime_report";
        title = "Downtime Report";
    }
    fetch(url)
        .then(r => r.json())
        .then(data => {
            document.getElementById('report-title').textContent = title;
            document.getElementById('report-content').textContent = JSON.stringify(data, null, 2);
            document.getElementById('report-modal').style.display = 'block';
        });
}
window.closeReport = function() {
    document.getElementById('report-modal').style.display = 'none';
}
