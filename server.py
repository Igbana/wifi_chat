import json
import socket
import threading

HOST = '127.0.0.1'
PORT = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


clients = {}


def broadcast(message):
    print(message.decode())
    for client in clients:
        client.send(message)

def handle_connection(client):
    stop = False
    while not stop:
        try:
            message = client.recv(1024).decode()
            if message == 'xKill':
                client.close()
                del clients[client]
                print('Stopped')
                stop = True
            elif message == 'x-Kill':
                message = 'xKill'
                broadcast(f'{{"{clients[client]}": "{message}"}}'.encode())
            else:
                broadcast(f'{{"{clients[client]}": "{message}"}}'.encode())
        except Exception as e:
            usr = clients[client]
            del clients[client]
            broadcast(f"{usr} left the chat!".encode())
            print('Stopped')
            stop = True

def main():
    print("Server is running")
    while True:
        client, addr = server.accept()
        print(f"Connected to {addr}")
        
        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        clients[client] = nickname

        print("Nickname: " + nickname)
        # broadcast(f"{nickname} joined the chat!".encode())
        # client.send("You are now connected".encode())
        threading.Thread(target=handle_connection, args=(client,)).start()

if __name__ == '__main__':
    main()