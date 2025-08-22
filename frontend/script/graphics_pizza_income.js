document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("graficoPizzaReceita").getContext("2d");

    const labels = JSON.parse(document.getElementById("categoriasLabels").value);
    const data = JSON.parse(document.getElementById("categoriasValues").value);

    function corDaCategoria(nome) {
        let hash = 0;
        for (let i = 0; i < nome.length; i++) {
            hash = nome.charCodeAt(i) + ((hash << 5) - hash);
        }
        const c = (hash & 0x00ffffff).toString(16).toUpperCase();
        return "#" + "000000".substring(0, 6 - c.length) + c;
    }

    const colors = labels.map(corDaCategoria);

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Receitas por Categoria",
                    data: data,
                    backgroundColor: colors,
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
