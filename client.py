import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring(
            "Nickname", "Escolha seu apelido:")
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    # sem funcionalidade so a interface front-end

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightblue")

        self.chat_label = tkinter.Label(self.win, text="Chat", bg='lightblue')
        self.chat_label.configure(font=("Courier", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.chat_text = tkinter.scrolledtext.ScrolledText(
            self.win, width=40, height=10)
        self.chat_text.pack(padx=20, pady=5)

        self.input_label = tkinter.Label(
            self.win, text="Mensagem", bg='lightblue')
        self.input_label.pack(padx=20, pady=5)

        # maybe is input_text instead of input_text
        self.input_text = tkinter.Entry(self.win, width=40)
        self.input_text.configure(font=("Courier", 12))
        self.input_text.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(
            self.win, text="Enviar", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        # message = f"{self.nickname}: {self.input_text.get('1.0', 'end')}"
        message = f"{self.nickname}: {self.input_text.get()}"
        self.socket.send(message.encode('utf-8'))
        self.input_text.delete(first=0, last='end')
        # self.input_text.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.socket.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.socket.send(message.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.chat_text.config(state='normal')
                        self.chat_text.insert('end', message + '\n')
                        self.chat_text.yview('end')
                        self.chat_text.config(state='disabled')
            except ConnectionAbortedError():
                break
            except:
                print("Error")
                self.sock.close()
                break


client = Client(HOST, PORT)
