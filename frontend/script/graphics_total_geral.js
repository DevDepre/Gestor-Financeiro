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
                    backgroundColor: "#d4edda",
                    borderWidth: 1,
                    borderRadius: 10,
                    borderSkipped: false,
                },
                {
                    label: "Gastos",
                    data: [despesa],
                    backgroundColor: "#f8d7da",
                    borderWidth: 1,
                    borderRadius: 10,
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
                    text: "Comparação entre Ganhos e Gastos",
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
