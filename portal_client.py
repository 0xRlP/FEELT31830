import crud_products
import socket as Socket 
import _thread as thread
import redis

socket = Socket.socket()
host = Socket.gethostname()
port = 6666

socket.bind((host,port))
socket.listen(10)
print('Server is running in port :', port)


def proccess_command(connection, address):
    while True:
        try:
            msg = connection.recv(1024).decode().strip()
            cid, cmd, data = msg.split(" ")
            data = data.split(',')
            if crud_products.validate_restaurant(cid):
                if 'create' in msg:
                    response = crud_products.create_product(cid,data)
                    connection.send(response.encode())
                    
                elif 'read' in msg:
                    response = crud_products.read_product(data)
                    connection.send(response.encode())

                elif 'update' in msg:
                    response = crud_products.update_product(data)
                    connection.send(response.encode())
                
                elif 'delete' in msg:
                    response = crud_products.delete_product(data)
                    connection.send(response.encode())
                
                else:
                    connection.send('Command invalid'.encode())
            else:
                connection.send('Permission denied!'.encode())
        except:
            break

while True:
    connection, address = socket.accept()
    connection.send(f'Welcome!\n'.encode())
    thread.start_new_thread(proccess_command, (connection, address))