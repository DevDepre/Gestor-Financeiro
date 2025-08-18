document.addEventListener("DOMContentLoaded", function () {
    const btnAnterior = document.getElementById("mesAnterior");
    const btnPosterior = document.getElementById("mesPosterior");
    const spanMesAtual = document.getElementById("mesAtual");

    let mesAtual = parseInt(spanMesAtual.dataset.mes);

    btnAnterior.addEventListener("click", () => {
        if (mesAtual > 1) {
            mesAtual -= 1;
            window.location.href = `/dashboard_income?mes=${mesAtual}`;
        }
    });

    btnPosterior.addEventListener("click", () => {
        if (mesAtual < 12) {
            mesAtual += 1;
            window.location.href = `/dashboard_income?mes=${mesAtual}`;
        }
    });
});
