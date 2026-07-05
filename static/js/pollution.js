let pollutionChart;

// ======================================
// Pollution Chart
// ======================================

function drawPollutionChart(data) {

    const canvas = document.getElementById("pollutionChart");

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    if (pollutionChart) {
        pollutionChart.destroy();
    }

    pollutionChart = new Chart(ctx, {

        type: "bar",

        data: {

            labels: [
                "PM2.5",
                "PM10",
                "CO",
                "NO₂",
                "SO₂",
                "NH₃",
                "O₃"
            ],

            datasets: [{

                label: "Pollution Level",

                data: [

                    data.pm25 || 0,
                    data.pm10 || 0,
                    data.co || 0,
                    data.no2 || 0,
                    data.so2 || 0,
                    data.nh3 || 0,
                    data.o3 || 0

                ],

                backgroundColor: [
                    "#0d6efd",
                    "#0dcaf0",
                    "#ffc107",
                    "#dc3545",
                    "#198754",
                    "#6f42c1",
                    "#fd7e14"
                ],

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true

                }

            }

        }

    });

}

// ======================================
// AQI Status
// ======================================

function getAQIStatus(aqi) {

    switch (Number(aqi)) {

        case 1:
            return { text: "Good", color: "bg-success" };

        case 2:
            return { text: "Fair", color: "bg-info" };

        case 3:
            return { text: "Moderate", color: "bg-warning" };

        case 4:
            return { text: "Poor", color: "bg-danger" };

        case 5:
            return { text: "Very Poor", color: "bg-dark" };

        default:
            return { text: "--", color: "bg-secondary" };

    }

}

// ======================================
// Load Latest Pollution
// ======================================

async function loadPollution() {

    try {

        const response = await fetch("/api/pollution/latest");

        if (!response.ok) {

            throw new Error("Failed to fetch pollution data.");

        }

        const data = await response.json();

        document.getElementById("aqi").innerHTML = data.aqi;

        document.getElementById("pressure").innerHTML =
            Number(data.pressure || 0).toFixed(0);

        document.getElementById("pm25").innerHTML =
            Number(data.pm25 || 0).toFixed(2);

        document.getElementById("pm10").innerHTML =
            Number(data.pm10 || 0).toFixed(2);

        document.getElementById("co").innerHTML =
            Number(data.co || 0).toFixed(2);

        document.getElementById("no2").innerHTML =
            Number(data.no2 || 0).toFixed(2);

        document.getElementById("so2").innerHTML =
            Number(data.so2 || 0).toFixed(2);

        document.getElementById("nh3").innerHTML =
            Number(data.nh3 || 0).toFixed(2);

        document.getElementById("o3").innerHTML =
            Number(data.o3 || 0).toFixed(2);

        document.getElementById("city").innerHTML =
            data.city || "--";

        document.getElementById("latitude").innerHTML =
            data.latitude || "--";

        document.getElementById("longitude").innerHTML =
            data.longitude || "--";

        document.getElementById("time").innerHTML =
            new Date(data.time).toLocaleString();

        const status = getAQIStatus(data.aqi);

        document.getElementById("aqiStatus").innerHTML =
            status.text;

        const badge = document.getElementById("connectionStatus");

        if (badge) {

            badge.className = "badge " + status.color;

            badge.innerHTML = "🟢 LIVE";

        }

        drawPollutionChart(data);

    }

    catch (error) {

        console.error(error);

        const badge = document.getElementById("connectionStatus");

        if (badge) {

            badge.className = "badge bg-danger";

            badge.innerHTML = "🔴 OFFLINE";

        }

    }

}

// ======================================
// Load Pollution History
// ======================================

async function loadPollutionHistory() {

    try {

        const response = await fetch("/api/pollution/history");

        if (!response.ok) {

            throw new Error("Failed to fetch pollution history.");

        }

        const history = await response.json();

        let rows = "";

        history.forEach((item, index) => {

            rows += `
            <tr>
                <td>${index + 1}</td>
                <td>${item.aqi}</td>
                <td>${Number(item.pm25 || 0).toFixed(2)}</td>
                <td>${Number(item.pm10 || 0).toFixed(2)}</td>
                <td>${Number(item.co || 0).toFixed(2)}</td>
                <td>${Number(item.no2 || 0).toFixed(2)}</td>
                <td>${Number(item.so2 || 0).toFixed(2)}</td>
                <td>${Number(item.nh3 || 0).toFixed(2)}</td>
                <td>${Number(item.o3 || 0).toFixed(2)}</td>
                <td>${new Date(item.time).toLocaleString()}</td>
            </tr>
            `;

        });

        document.getElementById("historyTable").innerHTML = rows;

    }

    catch (error) {

        console.error(error);

    }

}

// ======================================
// Initial Load
// ======================================

loadPollution();
loadPollutionHistory();

// ======================================
// Auto Refresh
// ======================================

setInterval(() => {

    loadPollution();

    loadPollutionHistory();

}, 10000);