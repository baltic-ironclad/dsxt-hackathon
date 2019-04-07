import socket
import json
import os
import web3

from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract
from match import Order, handle_new_order


class Storage:
    def __init__(self):
        self.path = 'users.json'

        if os.path.exists(self.path):
            self.load()
        else:
            self.data = []
            self.write()

    def load(self):
        with open(self.path, 'r') as storage:
            self.data = json.load(storage)

    def write(self):
        with open(self.path, 'w') as storage:
            json.dump(self.data, storage, indent=4)

    def update(self, new):
        for item in self.data:
            if item['address'] == new['hash']:
                break
        self.data.append({
            'id': self.data[-1]['id'] + 1 if len(self.data) != 0 else 1,
            'address': new['hash']
        })
        self.write()


def deploy_contract():
    with open('contract.sol', 'r') as contract_file:
        contract = contract_file.read()
    compiled = compile_source(contract)
    # TODO: Work with contract

    contract_id, contract_interface = compiled.popitem()

    contract_hash = w3.eth.contract(
       abi=contract_interface['abi'],
       bytecode=contract_interface['bin']).deploy()

    address = w3.eth.getTransactionReceipt(contract_hash)['contractAddress']


def start_matching():
    pass


def start_transaction():
    pass


def main(database):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8080))
    server.listen(100)

    while True:
        connection, address = server.accept()
        raw = b''

        try:
            while True:
                received = connection.recv(4096)
                if not received:
                    break
                raw += received
        finally:
            data = json.loads(raw.decode('utf-8'))
            order = Order(
                data['hash'],
                int(data['price']),
                int(data['amount']),
                data['direction'] == 'SELL'
            )
            handle_new_order(order)
            # print(data)
            # database.update(data)
            connection.close()


if __name__ == '__main__':
    database = Storage()
    main(database)
