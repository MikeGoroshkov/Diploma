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
saves = []

def send(client, save):
    try:
        client.send(save.encode('ascii'))
    except:
        print("Failed to send save")

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        input_message = client.recv(1024).decode('ascii')
        if input_message.split()[0] == 'request':
            for save in saves:
                if save.split(";")[0] == input_message.split()[1]:
                    thread = threading.Thread(target=send, args=(client, save))
                    thread.start()
                    nickname = input_message.split()[1]
                    print(f"Sended save to {nickname}:{address}")
        else:
            for i, save in enumerate(saves):
                if save.split(";")[0] == input_message.split(";")[0]:
                    saves.pop(i)
            saves.append(input_message)
            nickname = input_message.split(";")[0]
            print(f"Writed save from {nickname}:{address}")
            print(saves)


print("Server if listening...")
receive()
