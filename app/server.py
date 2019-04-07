import socket
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(5)

while True:
    connection, address = server.accept()

    try:
        while True:
            data = connection.recv(32)
            if not data:
                break
            connection.sendall(data)
            print('Data received')
    finally:
        connection.close()
        print('Client disconnected')
