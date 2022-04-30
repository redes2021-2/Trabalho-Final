import socket
import threading
# imports de biblioteca para GUI
# se não tiver o tkinter, instale-o com o comando:
# sudo apt install python3-tk
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

# Declarar ip host e porta
HOST = '127.0.0.1'
PORT = 9090


class Client:

    def __init__(self, host, port):
        # Etapa de conexão
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)     # criar socket
        # conectar ao host
        self.socket.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        # pedir nickname
        self.nickname = simpledialog.askstring(
            "Nickname", "Escolha seu apelido:")
        # pedir grupo
        self.group = simpledialog.askstring(
            "Group", "Escolha seu grupo:")

        self.gui_done = False
        self.running = True

        # thread para receber mensagens
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    # sem funcionalidade so a interface front-end
    def gui_loop(self):
        # criar janela
        self.win = tkinter.Tk()
        self.win.configure(bg="lightblue")
        self.win.title("Chat")
        self.win.geometry("400x400")

        # input text
        self.chat_label = tkinter.Label(
            self.win, text=self.group, bg='lightblue')
        self.chat_label.configure(font=("Courier", 12))
        self.chat_label.pack(padx=20, pady=5)

        # campo de texto
        self.chat_text = tkinter.scrolledtext.ScrolledText(
            self.win, width=40, height=10)
        self.chat_text.pack(padx=20, pady=5)

        # label para input de mensagem
        self.input_label = tkinter.Label(
            self.win, text="Mensagem", bg='lightblue')
        self.input_label.pack(padx=20, pady=5)

        # campo de texto de entrada
        self.input_text = tkinter.Entry(self.win, width=40)
        self.input_text.configure(font=("Courier", 12))
        self.input_text.pack(padx=20, pady=5)

        # botao para enviar mensagem
        self.send_button = tkinter.Button(
            self.win, text="Enviar", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        # ao fechar janela chamar stop
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        # pegar mensagem do input
        message = f"{self.nickname}: {self.input_text.get()}"
        # enviar mensagem
        self.socket.send(message.encode('utf-8'))
        # limpar campo de texto
        self.input_text.delete(first=0, last='end')

    def stop(self):
        self.running = False    # parar loop
        self.win.destroy()      # fechar janela
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.close()     # fechar socket
        exit()

    def receive(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.socket.send(self.nickname.encode(
                        'utf-8'))  # enviar nickname
                elif message == 'GROUP':
                    self.socket.send(self.group.encode(
                        'utf-8'))   # enviar grupo
                else:
                    if self.gui_done:
                        # adicionar mensagem ao chat
                        self.chat_text.config(state='normal')
                        self.chat_text.insert('end', message + '\n')
                        self.chat_text.yview('end')
                        self.chat_text.config(state='disabled')
            except ConnectionAbortedError():
                break
            except:
                print("Error")
                self.sock.close()   # fechar socket
                break


# iniciar cliente
client = Client(HOST, PORT)
