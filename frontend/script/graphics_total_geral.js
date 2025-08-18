document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("graficoTotal").getContext("2d");

    const receita = parseFloat(document.getElementById("receitaTotal").value);
    const despesa = parseFloat(document.getElementById("despesaTotal").value);

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: [""],
            datasets: [
                {
                    label: "Ganhos",
                    data: [receita],
                    backgroundColor: "#ACE1AF",
                    borderWidth: 1,
                    borderSkipped: false,
                },
                {
                    label: "Gastos",
                    data: [despesa],
                    backgroundColor: "#F05945",
                    borderWidth: 1,
                    borderSkipped: false,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
                title: {
                    display: true,
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
});
