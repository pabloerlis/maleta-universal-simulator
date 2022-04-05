from control_74165 import Control_74165
from control_74595 import Control_74595
from comum import mudar_comum_saidas, mudar_comum_entradas
import server, json

IN = Control_74165(pin_ENABLEn=36, pin_LATCHn=38, pin_CLOCK=40, pin_DATA=32, qty_ci=8)
OUT = Control_74595(pin_RESETn=12, pin_LATCH=18, pin_CLOCK=16, pin_DATA=22, qty_ci=8)
global lst_saidas_organizadas
lst_saidas_organizadas = list(map(lambda a : 0, range(64)))#armazena a lista de entradas
#-----------CORRIGE A ORDEM DOS PINOS DE ENTRADAS-----------
def corrige_conector(lst_input):#corrige o problema de ordenação das entradas com base no hardware.
    new_lst_input = []
    s = 0
    for k in range(int(len(lst_input) / 8)):
        lst_input_temp = lst_input[s:(s+8)]
        new_lst_input += lst_input_temp[::-1]
        s += 8
    return new_lst_input
#-----------CORRIGE A ORDEM DOS RELÉS-----------
def corrige_reles (lst_carga):
    new_lst = []
    s = 0
    for k in range(int(len(lst_carga) / 8)):
        lst_carga_temp = lst_carga[::-1][s:(s+8)]
        new_lst += lst_carga_temp
        s += 8
    return new_lst
#--------COMANDA AS SAÍDAS----------
def comand_output(lst_output):
    global lst_saidas_organizadas
    a = []
    if len(OUT.old_list_data) == 80:
        a = OUT.old_list_data[64:]
    else:
        a = list(map(lambda a : 0, range(OUT.qty_ci * 8)))
    b = corrige_reles(lst_output)
    c = b + a#primeiro rele da entrada depois os da saída
    lst_saidas_organizadas = b
    OUT.write(c)

    
#---COMANDA A LEITURA DAS ENTRADAS---
def comand_input():
    while True:
        if IN.read():
            a = corrige_conector(IN.list_data)
            server.send({'inputs':a})
            #server.send(corrige_conector(IN.list_data))
            IN.delay(100)
#----------COMANDA A CARGA-----------
def comand_load(lst):
    global lst_saidas_organizadas
    lst_temp = list(map(lambda a : 0, range(OUT.qty_ci * 8)))
    try:
        lst_temp[lst[0]] = lst[1]
    except:
        OUT.write(lst_saidas_organizadas + list(map(lambda a : 0, range(OUT.qty_ci * 8))))
    #teste abaixo
    a = corrige_reles(lst_temp)[:OUT.qty_ci * 8]
    a = a[::-1]
    a = a[:OUT.qty_ci * 8]
    a = a[::-1]
    OUT.write(lst_saidas_organizadas + a)
    #teste acima
    #OUT.write(corrige_reles(lst_temp)[:OUT.qty_ci * 8])
#---COMANDA O COMUM DAS SAÍDAS DIGITAIS---
def comand_comum_saidas(nvl):
    mudar_comum_saidas(nvl[0])

#---COMANDA O COMUM DAS ENTRADAS DIGITAIS---
def comand_comum_entradas(nvl):
    mudar_comum_entradas(nvl[0])

#-----------SALVAR RECEITA---------
def salvar_receita(dict_receita=None):
    if '' not in dict_receita:
        path = "/var/www/html/receitas/receitas.ek"
        arquivo = open(path, 'r')
        conteudo = json.loads(arquivo.readline())
        conteudo.update(dict_receita)
        arquivo = open(path, 'w')
        arquivo.writelines(json.dumps(conteudo))
        arquivo.close()
    else:
        pass
#----------CARREGAR RECEITA---------
def carregar_receita():
    path = path = "/var/www/html/receitas/receitas.ek"
    arquivo = open(path, 'r')
    for linha in arquivo:
        receita = json.loads(linha)
        return ["outputs",receita]
        server.send(["outputs",receita])


                
def _main(topic, lst=None):
    print(topic, lst)
    '''O servidor utiliza esta função para passar as mensagens que chegam
    no servidor websocket. Esta função é reponsável por direcionar listas
    refenrente as entradas, saídas e carga.
    Ela identifica o tópico e com base nele envia a lista recebida para a
    sua respectiva função.'''
    if topic == "output":
        comand_output(lst)
    elif topic == "input":
        comand_input(lst)
    elif topic == "load":
        comand_load(lst)
    elif topic == "comum_saidas":
        comand_comum_saidas(lst)
    elif topic == "comum_entradas":
        comand_comum_entradas(lst)
    elif topic == "salvar_receita":
        salvar_receita(lst)
    elif topic == "carregar_receita":
        server.send(carregar_receita())
    else:
        print("Topic error! => ", topic)

if __name__ == '__main__':
    import server, time, threading, json
    #salvar_receita({"TESTE": [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0]})
    OUT.write(list(map(lambda a : 0, range(OUT.qty_ci * 8))))
    comand_input = threading.Thread(target=comand_input)
    comand_input.start()