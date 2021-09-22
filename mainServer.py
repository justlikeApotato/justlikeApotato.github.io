import threading 
import socket
import select

head_len = 10
host_ip = "185.199.108.153"
port = 48787

server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server_socket.bind((host_ip,port))

server_socket.listen()

clients = []
nickNames = []

def brodcast(msg):
    for client in clients:
        client.send(msg)

    # def receive_msg(client_socket):
    #     try:
    #         msg_header = client_socket.recv(head_len)
        
    #         if not len(msg_header):
    #             return False

    #         msg_length = int(msg_header.decode("utf-8").strip())
    #         return {"header":msg_header , "data":client_socket.recv(msg_length)}

    #     except:
    #         return False


def handle(client):
    while True:
      try:
          msg = client.recv(1024)
          brodcast(msg)

      

      except:
          index = clients.index(client)
          clients.remove(client)
          client.close()
          nickName = nickNames[index]
          brodcast(f'{nickName} left the chat'.encode('ascii'))
          nickNames.remove(nickName)
          break


def receive():
    while True:
        client, address = server_socket.accept()
        print(f'connected with {str(address)}')

        client.send("NICK".encode('ascii'))
        nickName = client.recv(1024).decode("ascii")
        nickNames.append(nickName)
        clients.append(client)

        print(f'Nickname is {nickName}!')
        brodcast(f'{nickName} has joined!!!!'.encode('ascii'))

        client.send("Coonnected to the server".encode('ascii'))

        thread = threading.Thread(target = handle , args=(client,))
        thread.start()

print("Server is running")
receive()
