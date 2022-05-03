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
groups = []
pairs = []

# funcao para enviar mensagens para todos os clientes


def broadcast(message):
    # enviar mensagem para todos os clientes do grupo
    print(f'Enviando mensagem para todos os clientes do grupo {currentGroup}')
    if currentGroup in groups:
        for pair in pairs:
            if pair[1] == currentGroup:
                pair[0].send(message)
        # index = groups.index(currentGroup)
        # client = pairs[index][0]
        # client.send(message)
        # client.send(message)


def broadcastG(message):
    # enviar mensagem para todos os clientes
    print(f'Enviando mensagem para todos os clientes')
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

            # achar par do cliente e remover
            for pair in pairs:
                if pair[0] == client:
                    pairs.remove(pair)
            # checar se tem grupo sem par
            for group in groups:
                if group not in [pair[1] for pair in pairs]:
                    groups.remove(group)

            break


def receive():
    while True:
        print('Lista de clientes:')
        print(nicknames)
        print('Lista de grupos:')
        print(groups)
        print('Lista de pares:')
        print(pairs)

        # aceitar conexão e receber endereços
        client, adress = server.accept()
        print(f'Conectado em {str(adress)}')

        # pegar apelido dp cliente e adicionar a lista de apelidos
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        print(f'Apelido: {nickname}')
        nicknames.append(nickname)
        clients.append(client)

        # pegar grupo do cliente e adicionar a lista de grupos
        client.send("GROUP".encode('utf-8'))
        group = client.recv(1024).decode('utf-8')
        print(f'Grupo: {group}')
        # checar se o grupo existe
        if group not in groups:
            groups.append(group)

        # check se o par existe
        if (client, group) not in pairs:
            # adicionar par cliente/grupo a lista de pares
            pairs.append((client, group))

        global currentGroup  # declarar como global
        currentGroup = group

        print(f'Usuario {nickname} foi adicionado a lista')  # print log
        # enviar mensagem de entrada para todos os clientes
        broadcast(f'{nickname} entrou no chat!'.encode('utf-8'))

        # criar thread para tratar mensagens
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# start the server
print('Server esta rodando...')
receive()
