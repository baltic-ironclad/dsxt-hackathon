import socket

from tkinter import *
from eth_hash.auto import keccak


def send_hash(hash, address, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((address, port))

    try:
        client.sendall(hash)
        received = 0
        expected = len(hash)

        while received < expected:
            data = client.recv(32)
            received += len(data)
    finally:
        client.close()


def clicked():
    hash = keccak(bytes(text.get(), encoding='utf-8'))
    send_hash(hash, 'localhost', 8080)


window = Tk()
window.title('Stock')

label = Label(window, text='Hash:')
label.grid(column=0, row=0)
text = Entry(window)
text.grid(column=1, row=0)

button = Button(window, text='Send', command=clicked)
button.grid(column=2, row=0)

window.mainloop()
