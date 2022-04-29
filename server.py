import socket
import threading

# Declarar ip host e porta
HOST = '127.0.0.1'
PORT = 9090

# etapas da conexao tcp
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # criar socket
server.bind((HOST, PORT))  # bind

# servidor espera por conexões
server.listen(5)

clients = []
nicknames = []

# funcao para enviar mensagens para todos os clientes


def broadcast(message):
    for client in clients:
        client.send(message)

# funcao para tratar as mensagens


def handle(client):
    while True:
        try:
            message = client.recv(1024)     # receber mensagem
            print(message)                  # print log da mensagem

            # enviar mensagem para todos os clientes
            broadcast(message)
        except:
            # se o cliente sair, remove-lo da lista

            index = clients.index(client)   # pegar indice do cliente
            clients.remove(client)          # remover cliente da lista
            client.close()                  # fechar conexão
            nickname = nicknames[index]     # pegar apelido do cliente
            nicknames.remove(nickname)      # remover apelido da lista
            break


def receive():
    while True:

        # aceitar conexão e receber endereços
        client, adress = server.accept()
        print(f'Conectado em {str(adress)}')

        # pegar apelido dp cliente e adicionar a lista de apelidos
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        print(f'Apelido: {nickname}')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Usuario {nickname} foi adicionado a lista')  # print log
        # enviar mensagem de entrada para todos os clientes
        broadcast(f'{nickname} entrou no chat!'.encode('utf-8'))

        # criar thread para tratar mensagens
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# start the server
print('Server esta rodando...')
receive()
