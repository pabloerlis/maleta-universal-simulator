import json, threading
from websocket_server import WebsocketServer
from main import _main, OUT, IN

global new_client, client_left, message_received, send, start_server

PORT = 9001
server = WebsocketServer(PORT)

def new_client(client, server):
    #Este método é chamado assim que um novo client se conecta ao servidor.
    OUT.write(list(map(lambda a : 0, range(OUT.qty_ci * 8))))
    IN.read()
    message = {'new_client':"Novo cliente conectado."}
    print(message['new_client'], ("Client(%d)" % client['id']))
    send(message)
    


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])
    

# Called when a client sends a message
def message_received(client, server, message):
    #Este método é chamado assim que o servidor recebe uma nova mensagem. Ele chama o método main localizado no arquivo main.py
    topic = json.loads(message)['topic']
    lst = json.loads(message)['message']
    _main(topic, lst)
    

def send(msg):
    #Este método deve ser chamado quando se desejar publicar uma mensagem a todos os clientes.
    server.send_message_to_all(json.dumps(msg))
    

def start_server():
    #Inicializa o servidor
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()

start_server = threading.Thread(target=start_server)
start_server.start()
