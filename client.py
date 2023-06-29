# Система авто сохранения на удаленном сервере в игре

import socket
import threading
import time

# Тестовые значения параметров
nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y = 'player', 50, 142, 100, 100, 25, 0, 1, 0, 0

def save_game(nickname = 'player', player_x = 50, player_y = 142, hp = 100, hp_max = 100, player_damage = 25, experience = 0, level = 1, bg_x = 0, bg_y = 0):
    try:
        save_message = f'{nickname};{player_x};{player_y};{hp};{hp_max};{player_damage};{experience};{level};{bg_x};{bg_y}'
        return save_message
    except:
        print("Failed to save game!")

def load_game(load_message):
    global nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y
    try:
        nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y = tuple(load_message.split(";"))
        print("Saving is loaded")
    except:
        print("Failed to load game!")


# Connecting To Server
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('192.168.43.14', 55555))

# Listening to Server and Sending Nickname
def receive():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.43.14', 55555))
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            load_game(message)
            print("Saving is loaded")
            break
        except:
            client.close()
            break

def send_saving():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('192.168.43.14', 55555))
            save_message = save_game(nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y)
            client.send(save_message.encode('ascii'))
            print("Saving is sended")
        except:
            break

def request_saving():
    global nickname
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('192.168.43.14', 55555))
            client.send(f'request {nickname}'.encode('ascii'))
            print("Request is sended")
        except:
            break


send_saving_thread = threading.Thread(target=send_saving)
send_saving_thread.start()

load_saving_thread = threading.Thread(target=request_saving)
load_saving_thread.start()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

# while True:
#     try:
#         load_saving_thread = threading.Thread(target=request_saving)
#         load_saving_thread.start()
#     except:
#         pass
#     time.sleep(10)

