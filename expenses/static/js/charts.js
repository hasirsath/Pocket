
document.addEventListener("DOMContentLoaded", function () {

    if (!window.pieLabels || !window.pieValues) return;

    const ctx = document.getElementById("expensePieChart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: window.pieLabels,
            datasets: [{
                data: window.pieValues,
                backgroundColor: [
                    "#6C63FF",
                    "#FFB703",
                    "#4CAF50",
                    "#FF6F61",
                    "#00B4D8",
                    "#9B5DE5"
                ],
                borderWidth: 0,
                cutout: "65%"
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        boxWidth: 12,
                        padding: 15
                    }
                }
            }
        }
    });
});
