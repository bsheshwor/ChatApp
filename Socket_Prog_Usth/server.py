import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
port = 1024  # initiate port no above 1024
server_socket = socket.socket()
#host = socket.gethostname()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ##modifies the socket to allow us to reuse the address
server_socket = socket.socket()  # get instance
 # look closely. The bind() function takes tuple as argument
server_socket.bind((IP, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
server_socket.listen()
## creating dict of clients and list of sockets
sockets_list = [server_socket]
clients = {}
#print(f'Listening for connections on {IP}:{port}...')
#HANDLING messeges received
def receive_messege(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_messege(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
        else:
            message = receive_messege(notified_socket)
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]

                continue
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
            

            ##handle for the exception/error sockets with:
            for notified_socket in exception_sockets:
                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]



