let predictionChart;

// ======================================
// Update Risk Card
// ======================================

function updateRiskCard(risk) {

    const card = document.getElementById("riskCard");
    const riskText = document.getElementById("risk");
    const icon = document.getElementById("riskIcon");
    const recommendation = document.getElementById("recommendation");

    card.className = "card shadow-lg text-center text-white";

    if (risk === "Low") {

        card.classList.add("bg-success");

        icon.className = "bi bi-shield-check display-1";

        recommendation.innerHTML =
            "✅ Air quality conditions indicate a <b>Low Acid Rain Risk</b>.<br><br>" +
            "Outdoor activities can continue normally. Continue environmental monitoring.";

    }

    else if (risk === "Medium") {

        card.classList.add("bg-warning");

        icon.className = "bi bi-exclamation-triangle display-1";

        recommendation.innerHTML =
            "⚠ Atmospheric conditions indicate a <b>Medium Acid Rain Risk</b>.<br><br>" +
            "Continue monitoring SO₂ and NO₂ levels.";

    }

    else {

        card.classList.add("bg-danger");

        icon.className = "bi bi-cloud-rain-heavy-fill display-1";

        recommendation.innerHTML =
            "🚨 Environmental conditions indicate a <b>High Acid Rain Risk</b>.<br><br>" +
            "Avoid prolonged outdoor exposure and continue monitoring.";

    }

    riskText.innerHTML = risk.toUpperCase();

}

// ======================================
// Trend Chart
// ======================================
function drawPredictionChart(history) {

    const canvas = document.getElementById("predictionChart");

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    if (predictionChart) {
        predictionChart.destroy();
    }

    const labels = [];
    const values = [];

    // Create a copy instead of modifying the original array
    const chartData = [...history].reverse();

    chartData.forEach(item => {

        labels.push(
            new Date(item.time).toLocaleTimeString()
        );

        switch (item.risk) {

            case "Low":
                values.push(1);
                break;

            case "Medium":
                values.push(2);
                break;

            case "High":
                values.push(3);
                break;

            default:
                values.push(0);
        }

    });

    predictionChart = new Chart(ctx, {

        type: "line",

        data: {

            labels: labels,

            datasets: [{

                label: "Risk",

                data: values,

                borderColor: "#0d6efd",

                backgroundColor: "rgba(13,110,253,0.2)",

                borderWidth: 3,

                pointRadius: 5,

                fill: true,

                tension: 0.4

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

                    min: 1,

                    max: 3,

                    ticks: {

                        stepSize: 1,

                        callback: function(value) {

                            if (value === 1) return "Low";
                            if (value === 2) return "Medium";
                            if (value === 3) return "High";

                            return "";

                        }

                    }

                }

            }

        }

    });

}

// ======================================
// Load Prediction
// ======================================

async function loadPrediction() {

    try {

        const response = await fetch("/api/predict");

        if (!response.ok) {

            throw new Error("Prediction API Error");

        }

        const data = await response.json();

        document.getElementById("predictionTime").innerHTML =
            new Date().toLocaleString();

        document.getElementById("summaryTime").innerHTML =
            new Date().toLocaleString();

        document.getElementById("aqi").innerHTML =
            data.pollution.aqi;

        document.getElementById("city").innerHTML =
            data.pollution.city;

        updateRiskCard(data.risk);

        document.getElementById("predictionStatus").className =
            "badge bg-success fs-6";

        document.getElementById("predictionStatus").innerHTML =
            "🟢 LIVE";

    }

    catch (error) {

        console.error(error);

        document.getElementById("predictionStatus").className =
            "badge bg-danger fs-6";

        document.getElementById("predictionStatus").innerHTML =
            "🔴 OFFLINE";

    }

}

// ======================================
// Prediction History
// ======================================

async function loadPredictionHistory() {

    try {

        const response = await fetch("/api/prediction/history");

        if (!response.ok) return;

        const history = await response.json();

        let rows = "";

        history.forEach((item, index) => {

            let badge = "bg-success";

            if (item.risk === "Medium") {

                badge = "bg-warning";

            }

            if (item.risk === "High") {

                badge = "bg-danger";

            }

            rows += `

            <tr>

                <td>${index + 1}</td>

                <td>${new Date(item.time).toLocaleString()}</td>

                <td>

                    <span class="badge ${badge}">

                        ${item.risk}

                    </span>

                </td>

            </tr>

            `;

        });

        document.getElementById("predictionHistory").innerHTML = rows;

        drawPredictionChart(history);

    }

    catch (error) {

        console.error(error);

    }

}

// ======================================
// Initial Load
// ======================================

loadPrediction();

loadPredictionHistory();

// ======================================
// Auto Refresh
// ======================================

setInterval(() => {

    loadPrediction();

    loadPredictionHistory();

}, 10000);