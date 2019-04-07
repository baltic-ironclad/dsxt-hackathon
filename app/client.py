import socket
import json

from tkinter import *
from eth_hash.auto import keccak


def send_request(data, address, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((address, port))

    # Dictionary to bytes
    try:
        raw = json.dumps(data, ensure_ascii=False).encode('utf-8')
        client.sendall(raw)
    finally:
        client.close()


class Order(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title('Stock Exchange')

        # Private key of the wallet
        hash_label = Label(self, text='Hash:')
        hash_label.grid(column=0, row=0)
        self.hash_text = Entry(self)
        self.hash_text.grid(column=1, row=0)

        # Currency
        self.currency = StringVar(self)
        currency_label = Label(self, text='Currency:')
        currency_label.grid(column=0, row=1)
        currency_menu = OptionMenu(self, self.currency, 'USD', 'BTC')
        currency_menu.grid(column=1, row=1)

        # Amount of money to send
        amount_label = Label(self, text='Amount:')
        amount_label.grid(column=0, row=2)
        self.amount_text = Entry(self)
        self.amount_text.grid(column=1, row=2)

        # Price of the order
        price_label = Label(self, text='Price:')
        price_label.grid(column=0, row=3)
        self.price_text = Entry(self)
        self.price_text.grid(column=1, row=3)

        # Direction of transaction
        self.direction = StringVar(self)
        direction_label = Label(self, text='Direction:')
        direction_label.grid(column=0, row=4)
        direction_menu = OptionMenu(self, self.direction, 'BUY', 'SELL')
        direction_menu.grid(column=1, row=4)

        # Send collected data to server
        button = Button(self, text='Send', command=self.clicked)
        button.grid(column=1, row=5)

        self.pack()

    def clicked(self):
        data = {
            'hash': self.hash_text.get(),
            'currency': self.currency.get(),
            'amount': self.amount_text.get(),
            'price': self.price_text.get(),
            'direction': self.direction.get()
        }
        data['hash'] = str(keccak(bytes(data['hash'], encoding='utf-8')))

        try:
            send_request(data, 'localhost', 8080)
        except ConnectionRefusedError:
            print('Server is down')
            exit(0)


def main():
    root = Tk()
    app = Order(root)
    root.mainloop()


if __name__ == '__main__':
    main()
