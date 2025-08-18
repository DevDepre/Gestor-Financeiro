document.addEventListener("DOMContentLoaded", async function () {
    const ctx = document.getElementById("graficoBarrasDespesas").getContext("2d");

    const response = await fetch("/api/graficos_expenses/mensal");
    const data = await response.json();

    const mesesNomes = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];

    const gastosPorMes = new Array(12).fill(0);

    data.gastos.forEach((item) => {
        gastosPorMes[item.mes - 1] = item.total;
    });

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: mesesNomes,
            datasets: [
                {
                    label: "Gastos",
                    backgroundColor: "#F05945",
                    data: gastosPorMes,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "top",
                },
            },
        },
    });
});
