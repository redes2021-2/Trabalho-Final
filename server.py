import socket
import threading
from tkinter import simpledialog

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
sizes = []
pairs = []
# para enviar para lista na GUI
# clientsInGroup = []


def getTotalClientsGroup(group):
    total = 0
    for pair in pairs:
        if pair[1] == group:
            total += 1
    return total

# funcao para enviar mensagens para todos os clientes


def broadcast(message):
    clientsInGroup = []
    # enviar mensagem para todos os clientes do grupo
    print(f'Enviando mensagem para todos os clientes do grupo {currentGroup}')
    if currentGroup in groups:
        for pair in pairs:
            if pair[1] == currentGroup:
                pair[0].send(message)
                # get nickname from client
                index = clients.index(pair[0])
                nickname = nicknames[index]
                # adiciona nickname a lista de clientes do grupos
                # clientsInGroup.append(nickname)


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

            # enviar lista de clientes para o cliente
            # client.send(str(clientsInGroup).encode('utf-8'))
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
            # for group in groups:
                # if group not in [pair[1] for pair in pairs]:
                    # groups.remove(group)

            # se o total de clientes no grupo for 0, deletar grupo
            if getTotalClientsGroup(currentGroup) == 0:
                groups.remove(currentGroup)
                sizes.remove(size[groups.index(currentGroup)])

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

            size = simpledialog.askstring(
                "Size Group", "Escolha o tamanho do grupo:")
            sizes.append(int(size))
            print(f'Tamanho do grupo: {size}')

        # check se o par existe
        if (client, group) not in pairs:
            # adicionar par cliente/grupo a lista de pares
            pairs.append((client, group))

        # declarar como global
        global currentGroup
        currentGroup = group

        # checar se o grupo ja alcançou o tamanho maximo
        check = getTotalClientsGroup(group)
        print('-------------------------------------------------------------------------------')
        print(f'Total de clientes no grupo: {check}')
        print(f'Tamanho do grupo no vetor: {sizes[groups.index(group)]}')
        print('-------------------------------------------------------------------------------')

        flag = check > sizes[groups.index(group)]

        if flag:
            print('Grupo alcançou o tamanho maximo')
            alert = 'Grupo alcançou o tamanho maximo'
            broadcast(alert.encode('utf-8'))
            msg = 'MAX'
            client.send(msg.encode('utf-8'))

            # deletar cliente do grupo
            index = clients.index(client)   # pegar indice do cliente
            clients.remove(client)          # remover cliente da lista
            client.close()                  # fechar conexão
            nickname = nicknames[index]     # pegar apelido do cliente
            nicknames.remove(nickname)      # remover apelido da lista

            # achar par do cliente e remover
            for pair in pairs:
                if pair[0] == client:
                    pairs.remove(pair)

            break

        print(f'Usuario {nickname} foi adicionado a lista')  # print log
        # enviar mensagem de entrada para todos os clientes
        broadcast(f'{nickname} entrou no chat!'.encode('utf-8'))

        # criar thread para tratar mensagens
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# start the server
print('Server esta rodando...')
receive()
