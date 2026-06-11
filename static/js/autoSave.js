let idCapitulo = window.idCapituloInicial || null;
let idLivro = window.idLivro;

let timeout;

// pega conteúdo do editor
function getConteudo() {
    return quill.root.innerHTML;
}

// pega título do input
function getTitulo() {
    return document.getElementById("titulo").value;
}

// auto-save principal
function autoSave() {

    const conteudo = getConteudo();
    const titulo = getTitulo();

    fetch("/autoSave", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: idCapitulo,
            titulo: titulo,
            conteudo: conteudo,
            idLivro: idLivro
        })
    })
    .then(res => res.json())
    .then(data => {

        // se criou agora, guarda o id
        if (!idCapitulo) {
            idCapitulo = data.id;
        }

        console.log("Salvo ✔", idCapitulo);
    })
    .catch(err => {
        console.error("Erro ao salvar ❌", err);
    });
}

// detecta mudanças no editor
quill.on('text-change', () => {

    clearTimeout(timeout);

    timeout = setTimeout(() => {
        autoSave();
    }, 2000);
});

// detecta mudanças no título também
document.getElementById("titulo").addEventListener("input", () => {

    clearTimeout(timeout);

    timeout = setTimeout(() => {
        autoSave();
    }, 2000);
});