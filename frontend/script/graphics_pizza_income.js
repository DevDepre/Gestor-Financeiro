document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("graficoPizzaReceita").getContext("2d");

    const receita = parseFloat(document.getElementById("receitaTotal").value);

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Receita"],
            datasets: [
                {
                    label: "Distribuição",
                    data: [receita],
                    backgroundColor: ["#ACE1AF"],
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
