from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", 12345))


clients = {}
addresses = {}


def broadcast_message(message, prefix=""):
    for client_socket in clients:
        client_socket.send(bytes(prefix + message, "utf-8"))


def handle_client(client_socket):
    name = client_socket.recv(1024).decode("utf-8")
    clients[client_socket] = name
    client_socket.send(b"Type {quit} to leave the chat")
    broadcast_message("%s has joined the chat" % name)
    
    while True:
        message = client_socket.recv(1024).decode("utf-8")
        
        if message == "{quit}":
            del clients[client_socket]
            broadcast_message("%s left the chat" % name)
            print("%s:%s has broken connection" % addresses[client_socket])
            del addresses[client_socket]
            break
        else:
            broadcast_message(message, name+":")
            

def accept_connection():
    while True:
        client_socket, client_address = server_socket.accept()
        addresses[client_socket] = client_address
        print("%s:%s has been connected" % client_address)
        client_socket.send(b"Welcome to the chat! What is your name?")
        Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    server_socket.listen(2)
    server_thread = Thread(target=accept_connection)
    server_thread.start()
    server_thread.join()
    server_socket.close()