import socket
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(1)

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
        connection.close()
        print(data)
