import socket as Socket
import select 
import sys


socket = Socket.socket()
host = Socket.gethostname()
port = 6667
socket.connect((host,port))
print(socket.recv(1024).decode())
# socket_list = [socket, sys.stdin]

while True:
    # readable_socks, _, _ = select.select(socket_list, [], [])
    message = input()
    if message == 'exit':
        print('bye!')
        break
    if len(message.split(' ')) != 4:
        print('Entrada incorreta \n')
        continue
    socket.send(message.encode())
    response = socket.recv(1024).decode()
    print(response)

socket.close()