let sensorChart;
let pollutionChart;

// =====================================
// Sensor Chart
// =====================================

function drawSensorChart(sensor) {

    const ctx = document.getElementById("sensorChart");

    if (sensorChart) {
        sensorChart.destroy();
    }

    sensorChart = new Chart(ctx, {

        type: "bar",

        data: {

            labels: [
                "Temperature",
                "Humidity"
            ],

            datasets: [{

                label: "Sensor Data",

                data: [
                    sensor.temperature,
                    sensor.humidity
                ],

                backgroundColor: [
                    "#0d6efd",
                    "#0dcaf0"
                ]

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {
                    display: false
                }

            }

        }

    });

}

// =====================================
// Pollution Chart
// =====================================

function drawPollutionChart(pollution) {

    const ctx = document.getElementById("pollutionChart");

    if (pollutionChart) {
        pollutionChart.destroy();
    }

    pollutionChart = new Chart(ctx, {

        type: "bar",

        data: {

            labels: [
                "CO",
                "NO₂",
                "SO₂",
                "O₃",
                "NH₃"
            ],

            datasets: [{

                label: "Pollution",

                data: [

                    pollution.co,
                    pollution.no2,
                    pollution.so2,
                    pollution.o3,
                    pollution.nh3

                ],

                backgroundColor: [
                    "#ffc107",
                    "#dc3545",
                    "#20c997",
                    "#0dcaf0",
                    "#6f42c1"
                ]

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {
                    display: false
                }

            }

        }

    });

}

// =====================================
// Dashboard
// =====================================

async function loadDashboard() {

    document.getElementById("temperature").innerHTML = "--";
    document.getElementById("humidity").innerHTML = "--";
    document.getElementById("mq7").innerHTML = "--";
    document.getElementById("nh3").innerHTML = "--";
    document.getElementById("co2").innerHTML = "--";
    document.getElementById("aqi").innerHTML = "--";

    try {

        const response = await fetch("/api/predict", {

            method: "POST"

        });

        if (!response.ok) {

            throw new Error("Failed to fetch dashboard data.");

        }

        const data = await response.json();

        const sensor = data.sensor;
        const pollution = data.pollution;

        // ===============================
        // Connection
        // ===============================

        document.getElementById("connectionStatus").innerHTML =
            "🟢 LIVE";

        document.getElementById("connectionStatus").className =
            "badge bg-success";

        // ===============================
        // Temperature
        // ===============================

        document.getElementById("temperature").innerHTML =
            Number(sensor.temperature).toFixed(1) + " °C";

        // ===============================
        // Humidity
        // ===============================

        document.getElementById("humidity").innerHTML =
            Number(sensor.humidity).toFixed(1) + " %";

        // ===============================
        // CO
        // ===============================

        const mq7 = Number(sensor.mq7);

        if (!isNaN(mq7) && mq7 >= 0) {

            document.getElementById("mq7").innerHTML =
                mq7.toFixed(2) + " ppm";

        }
        else {

            document.getElementById("mq7").innerHTML =
                "--";

        }

        // ===============================
        // NH3
        // ===============================

        const nh3 = Number(sensor.nh3);

        if (!isNaN(nh3) && nh3 > 0) {

            document.getElementById("nh3").innerHTML =
                nh3.toFixed(3) + " ppm";

        }
        else {

            document.getElementById("nh3").innerHTML =
                "--";

        }

        // ===============================
        // CO2
        // ===============================

        const co2 = Number(sensor.co2);

        if (!isNaN(co2) && co2 > 0) {

            document.getElementById("co2").innerHTML =
                co2.toFixed(1) + " ppm";

        }
        else {

            document.getElementById("co2").innerHTML =
                "--";

        }

        // ===============================
        // AQI
        // ===============================

        const aqi = Number(pollution.aqi);

        document.getElementById("aqi").innerHTML = aqi;

        const aqiCard =
            document.getElementById("aqi").closest(".card");

        aqiCard.classList.remove(
            "bg-success",
            "bg-info",
            "bg-warning",
            "bg-danger"
        );

        if (aqi === 1) {

            aqiCard.classList.add("bg-success");

        }
        else if (aqi === 2) {

            aqiCard.classList.add("bg-info");

        }
        else if (aqi === 3) {

            aqiCard.classList.add("bg-warning");

        }
        else {

            aqiCard.classList.add("bg-danger");

        }

        // ===============================
        // Prediction Card
        // ===============================

        const riskCard =
            document.getElementById("risk");

        riskCard.innerHTML = `

            <div>

                <h2>${data.risk}</h2>

                <small>

                    Confidence

                </small>

                <h4>

                    ${data.probability}%

                </h4>

            </div>

        `;

        riskCard.classList.remove(
            "text-success",
            "text-warning",
            "text-danger"
        );

        if (data.risk === "Low") {

            riskCard.classList.add("text-success");

        }
        else if (data.risk === "Medium") {

            riskCard.classList.add("text-warning");

        }
        else {

            riskCard.classList.add("text-danger");

        }

        // ===============================
        // Progress Bar
        // ===============================

        const bar =
            document.getElementById("probabilityBar");

        bar.style.width =
            data.probability + "%";

        bar.innerHTML =
            data.probability + "%";

        bar.className =
            "progress-bar";

        if (data.risk === "Low") {

            bar.classList.add("bg-success");

        }
        else if (data.risk === "Medium") {

            bar.classList.add("bg-warning");

        }
        else {

            bar.classList.add("bg-danger");

        }

        // ===============================
        // Charts
        // ===============================

        drawSensorChart(sensor);

        drawPollutionChart(pollution);

        // ===============================
        // Last Update
        // ===============================

        document.getElementById("lastUpdate").innerHTML =
            new Date().toLocaleTimeString();

    }

    catch (error) {

        console.error(error);

        document.getElementById("connectionStatus").innerHTML =
            "🔴 OFFLINE";

        document.getElementById("connectionStatus").className =
            "badge bg-danger";

    }

}

// =====================================
// Sensor History
// =====================================

async function loadHistory() {

    try {

        const response =
            await fetch("/api/sensor/history");

        const history =
            await response.json();

        let rows = "";

        history.forEach((item, index) => {

            rows += `

            <tr>

                <td>${index + 1}</td>

                <td>${Number(item.temperature).toFixed(1)} °C</td>

                <td>${Number(item.humidity).toFixed(1)} %</td>

                <td>${
                    Number(item.mq7) >= 0
                    ? Number(item.mq7).toFixed(2) + " ppm"
                    : "--"
                }</td>

                <td>${
                    Number(item.nh3) > 0
                    ? Number(item.nh3).toFixed(3) + " ppm"
                    : "--"
                }</td>

                <td>${
                    Number(item.co2) > 0
                    ? Number(item.co2).toFixed(1) + " ppm"
                    : "--"
                }</td>

                <td>

                    ${new Date(item.time).toLocaleString()}

                </td>

            </tr>

            `;

        });

        document.getElementById("sensorTable").innerHTML =
            rows;

    }

    catch (error) {

        console.error(error);

    }

}

// =====================================
// Auto Refresh
// =====================================

loadDashboard();
loadHistory();

setInterval(() => {

    loadDashboard();
    loadHistory();

}, 10000);