let $create = document.createElement.bind(document) //alias
let $sel = document.querySelector.bind(document) //alias 
let $all = document.querySelectorAll.bind(document) //alias
    //WEBSOCKET ABAIXO
const servidor1 = "wss://echo.websocket.org"
const servidor2 = "ws://localhost:9001"
let ws = new WebSocket(servidor2);
let topic = 'input';


let lst_receitas_ = {}


let inputs = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]
let outputs = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

let lst_carga = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]
let carga = 0;
let comum_saidas = 0;
let comum_entradas = 0;
let ultimo_btn_saida_carga = null

function sendMessage(topic, message) {
    // Make the request to the WebSocket.
    ws.send(JSON.stringify({ topic, message }))
}


ws.onmessage = function(evt) {
    let messageDict = JSON.parse(evt.data);
    if ('new_client' == Object.keys(messageDict)) {
        console.log(messageDict['new_client'])
            //carregar a lst_receitas de acordo com o banco 
        sendMessage('carregar_receita', [])
    }
    if ('inputs' == Object.keys(messageDict)) {
        outputs = messageDict['inputs']
        config_layout_outputs()
    }

    if ('outputs' == messageDict[0]) {
        lst_receitas_ = messageDict[1]
    }

};

/*
ws.onmessage = function(evt) {
    let messageDict = JSON.parse(evt.data);
    console.log(messageDict)
    outputs = messageDict;
    config_layout_outputs();
};
*/
//WEBSOCKET ACIMA

//---------------------------------------------------

//CÓDIGO MAIN ABAIXO

const func_main = function(id) {
    console.log(id)
        //se for for ENTRADA
    if (document.getElementById(id).className.indexOf("btn_input") != -1) {
        //comuta o valor do botão na lista de inputs conforme ele é pressionado
        a = id.split('in')[1] //armazena o id do botão na variável a
        if (inputs[a - 1] == 0) { //se o elemento na lista referente ao botão for 0
            inputs[a - 1] = 1 //agora este mesmo elemento passa a ser 1
        } else {
            inputs[a - 1] = 0 //se o elemento na lista referente ao botão for 1, passa a ser 0
        }
        config_layout_inputs() //em seguida a função que configura o layout das entradas é chamada
        sendMessage('output', inputs) //em seguida a nova lista de entradas é enviada ao servidor
    }
    //trata dos botões de SAÍDAS -  bnt_output
    if (document.getElementById(id).className.indexOf("btn_output") != -1 && carga) {
        let c = id.split('out')[1]
        if (lst_carga[c - 1] == 0) {
            for (let index = 0; index < lst_carga.length; index++) {
                lst_carga[index] = 0
            }
            lst_carga[c - 1] = 1
        } else {
            for (let index = 0; index < lst_carga.length; index++) {
                lst_carga[index] = 0
            }
        }
        ultimo_btn_saida_carga = c
        sendMessage('load', [c - 1, lst_carga[c - 1], carga]) //envie ao servidor a posição na lista, carga no mesmo endereço, e se o botão de carga está pressionado
        config_layout_outputs()
    }
    if (id == 'outcarga') { //se for pressionado o botão de acionamento da carga:
        carga = !carga //mude o valor da variável que armazena o estado da carga
        if (carga == 0) { //Quando desativar a carga:
            sendMessage('load', lst_carga, 0) //envie uma mensagem para o servidor zerar as saídas pertinentes a carga
            for (let i = 0; i < lst_carga.length; i++) {
                lst_carga[i] = 0
            }
        }
    }
    if (id == 'comum_saidas') {
        comum_saidas = !comum_saidas
        sendMessage('comum_saidas', [comum_saidas])
        layout_comum_saidas()
    }

    if (id == 'comum_entradas') {
        comum_entradas = !comum_entradas
        sendMessage('comum_entradas', [comum_entradas])
        layout_comum_entradas()
    }

    if (id == "salvar") {
        sendMessage('salvar_receita', { 'PabloErlis': inputs })
        sendMessage('carregar_receita', [])
    }

    if (id == "carregar") {
        sendMessage('carregar_receita', [])
    }

    layout_carga()
    config_layout_outputs()
}


//CÓDIGO MAIN ACIMA

const config_layout_inputs = function() {
    for (let i = 0; i < 64; i++) {
        if (inputs[i] == 0) {
            let a = 'in' + (i + 1);
            document.getElementById(a).className = "btn btn-secondary btn_input"
        }
        if (inputs[i] == 1) {
            let a = 'in' + (i + 1);
            document.getElementById(a).className = "btn btn-success btn_input"
        }
    }
}

const config_layout_outputs = function(carga) {
    for (let i = 0; i < 64; i++) {
        if (outputs[i] == 0 && lst_carga[i] == 0) {
            let a = 'out' + (i + 1);
            document.getElementById(a).className = "btn btn-secondary btn_output"
        }
        if (outputs[i] == 1 && lst_carga[i] == 0) {
            let a = 'out' + (i + 1);
            document.getElementById(a).className = "btn btn-danger btn_output"
        }
        // CARGA ABAIXO
        if (outputs[i] == 0 && lst_carga[i] == 1) {
            let a = 'out' + (i + 1);
            document.getElementById(a).className = "btn btn-secondary btn_output load-active animate__animated animate__flash animate__delay-0s"
        }
        if (outputs[i] == 1 & lst_carga[i] == 1) {
            let a = 'out' + (i + 1);
            document.getElementById(a).className = "btn btn-danger btn_output load-active animate__animated animate__flash animate__delay-0s"
        }

        //CARGA ACIMA

    }
}

const layout_carga = function() {
    if (carga) {
        document.getElementById('outcarga').className = "btn btn-danger"
        document.getElementById('outcarga').textContent = "Desativar Carga"
        document.getElementById('alert_carga').textContent = '⚡CARGA ATIVA⚡'
        document.getElementById('alert_carga').className = "alert alert-danger animate__animated animate__flash animate__delay-0s"
    } else {
        document.getElementById('outcarga').className = "btn btn-primary"
        document.getElementById('alert_carga').textContent = 'Teste sem carga'
        document.getElementById('outcarga').textContent = "⚡Ativar Carga⚡"
        document.getElementById('alert_carga').className = "alert alert-primary animate__animated animate__fadeIn animate__delay-0s"
    }


}

const layout_comum_saidas = function() {
    if (comum_saidas) {
        document.getElementById('comum_saidas').className = "btn btn-danger btn-comum-saidas-24"
        document.getElementById('comum_saidas').textContent = "24V COMUM"
    } else {
        document.getElementById('comum_saidas').className = "btn btn-dark btn-comum-saidas-0"
        document.getElementById('comum_saidas').textContent = 'GND COMUM'
    }
}

const layout_comum_entradas = function() {
    if (comum_entradas) {
        document.getElementById('comum_entradas').className = "btn btn-danger btn-comum-saidas-24"
        document.getElementById('comum_entradas').textContent = "24V COMUM"
    } else {
        document.getElementById('comum_entradas').className = "btn btn-dark btn-comum-saidas-0"
        document.getElementById('comum_entradas').textContent = 'GND COMUM'
    }
}



//----------------------------------------------

function show_receitas() {
    remover_elementos('#sel')
    $sel("#salvar").style.display = 'none'
    $sel("#carregar").style.display = 'none'
    let select_receitas = $sel('#sel') // select de receitas
    let lst_receitas = Object.keys(lst_receitas_)
    for (let i = 0; i < lst_receitas.length; i++) {
        receita = $create("option")
        receita.textContent = lst_receitas[i]
        select_receitas.appendChild(receita)
    }
    $sel('form').style.display = 'block'
}

function carregar_receita() {
    esconder_receitas()
    lst_options = $sel('select').options
    if (lst_options['selectedIndex'] != -1) {
        //teste abaixo
        inputs = lst_receitas_[lst_options[lst_options['selectedIndex']].textContent]
        config_layout_inputs()
        sendMessage('output', inputs)
            //teste acima
            //enviar mensagem ao servidor
    } else {
        console.log('Não foi selecionado uma opção')
    }
    remover_elementos('#sel')
}

function remover_elementos(id) {
    const item = $sel(id)
    while (item.firstChild) {
        item.removeChild(item.firstChild)
    }
}

function esconder_receitas() {
    $sel("#salvar").style.display = 'inline-block'
    $sel("#carregar").style.display = 'inline-block'

    $sel('form').style.display = 'none'
}

//ESTOU DESENVOLVENDO AQUI ##########################################
function show_salvar() {
    $sel('#box-salvar').style.display = 'block'
}

function layout_salvar() {
    let texto = $sel('#text_salvar').value
    let dict = {}
    dict[texto] = inputs
    sendMessage('salvar_receita', dict)
    sendMessage('carregar_receita', [])
    $sel('#box-salvar').style.display = 'none'
    $sel('#box-salvar').style.value = '' //Apaga o campo de texto de salvar
}


function cancelar_salvar() {
    $sel('#box-salvar').style.display = 'none'
}





function lub(obj) {
    let a = $sel(".modal-body")
    let b = $create("button")
    b.textContent = 'teste'
    a.appendChild(b)
    console.log(b)
}