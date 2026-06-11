const quill = new Quill('#editor', {
    theme: 'snow',
    placeholder: 'Escreva seu capítulo aqui...'
});

// carregar conteúdo inicial (editar capítulo)
if (window.conteudoInicial) {
    quill.root.innerHTML = window.conteudoInicial;
}