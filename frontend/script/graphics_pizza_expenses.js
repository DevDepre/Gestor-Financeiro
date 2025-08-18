document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("graficoPizzaDespesas").getContext("2d");

    const despesa = parseFloat(document.getElementById("despesaTotal").value);

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Despesa"],
            datasets: [
                {
                    label: "Distribuição",
                    data: [despesa],
                    backgroundColor: ["#F05945"],
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: "top",
                },
            },
        },
    });
});
