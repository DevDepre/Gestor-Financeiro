document.addEventListener("DOMContentLoaded", async function () {
    const ctx = document.getElementById("graficoBarrasReceita").getContext("2d");

    const response = await fetch("/api/graficos_income/mensal");
    const data = await response.json();

    const mesesNomes = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];

    const ganhosPorMes = new Array(12).fill(0);

    data.ganhos.forEach((item) => {
        ganhosPorMes[item.mes - 1] = item.total;
    });

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: mesesNomes,
            datasets: [
                {
                    label: "Ganhos",
                    backgroundColor: "#ACE1AF",
                    data: ganhosPorMes,
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
