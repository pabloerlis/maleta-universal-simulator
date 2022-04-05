function loadFileAsText() { // função que busca e lê arquivo txt
    var fileToLoad = document.getElementById("fileToLoad").files[0]; //a intenção é não precisar de botões pra escolher arquivo e nem para
    var fileReader = new FileReader(); //executar o script, tudo deve acontecer quando cricar para abrir a aplicação
    fileReader.onload = function(fileLoadedEvent) {
        var textFromFileLoaded = fileLoadedEvent.target.result;
        var texto = textFromFileLoaded;
        listar(texto);
    };
    fileReader.readAsText(fileToLoad, "UTF-8");

}

function listar(texto) {
    var quantidade = document.getElementById("lista").rows.length; // está pré definido que será usado o tamanho total do arquivo
    if (quantidade > 1) { // quantidade representa o número indefinido de linhas que pode haver
        for (var cont = 1; cont <= quantidade; cont++) {
            document.getElementById("lista").deleteRow(cont); // lista é o nome atribuído ao conteúdo do arquivo txt
        }
    }

    var itens = texto.split("LOG_"); // define que linhas devem ser consultadas
    for (var i = 1; i < itens.length; i++) {

        var valores = itens[i].split("\t"); // espaços TAB definem colunas que serão consultadas
        document.getElementById("lista").innerHTML += '<tr><td>' + valores[1] + '</td><td>' + valores[6 & 1] + '</td><td>' + valores[2] + '</td></tr>';