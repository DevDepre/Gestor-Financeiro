document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("graficoPizza").getContext("2d");

    const receita = parseFloat(document.getElementById("receitaTotal").value);
    const despesa = parseFloat(document.getElementById("despesaTotal").value);

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Receita", "Despesa"],
            datasets: [
                {
                    label: "Distribuição",
                    data: [receita, despesa],
                    backgroundColor: ["#d4edda", "#f8d7da"], // verde e vermelho
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
                title: {
                    display: true,
                    text: "Distribuição de Ganhos e Gastos",
                },
            },
        },
    });
});
