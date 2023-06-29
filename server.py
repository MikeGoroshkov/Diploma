#!/bin/python3
import socket
import threading

# Connection Data
host = '192.168.43.14'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
savings = []

# Handling Messages From Clients
def send(client, saving):
    while True:
        try:
            client.send(saving.encode('ascii'))
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        input_message = client.recv(1024).decode('ascii')
        if input_message.split()[0] == 'request':
            for saving in savings:
                if saving.split(";")[0] == input_message.split()[1]:
                    thread = threading.Thread(target=send, args=(client, saving))
                    thread.start()
                    nickname = input_message.split()[1]
                    print(f"Sended saving to {nickname}:{address}")
        else:
            savings.append(input_message)
            nickname = input_message.split(";")[0]
            print(f"Writed saving from {nickname}:{address}")

        nicknames.append(nickname)
        clients.append(client)


print("Server if listening...")
receive()
