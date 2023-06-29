# Система авто сохранения на удаленном сервере в игре

import socket
import threading
import time

# Тестовые значения параметров
nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y = 'player', 50, 142, 100, 100, 25, 0, 1, 0, 0

def save_game(nickname = 'player', player_x = 50, player_y = 142, hp = 100, hp_max = 100, player_damage = 25, experience = 0, level = 1, bg_x = 0, bg_y = 0):
    try:
        save_message = f'{nickname};{player_x};{player_y};{hp};{hp_max};{player_damage};{experience}{level};{player_x};{player_y};{bg_x};{bg_y}'
        return save_message
    except:
        print("Failed to load game!")

def load_game(load_message):
    try:
        nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y = tuple(load_message.split(";"))
        return nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y
    except:
        print("Failed to load game!")


# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.43.14', 55555))

# Listening to Server and Sending Nickname
def receive():
    global nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y = load_game(message)
            print("Saving is loaded")
        except:
            pass

def send_saving():
    while True:
        save_message = save_game(nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y)
        client.send(save_message.encode('ascii'))
        time.sleep(10)

def request_saving():
    global nickname
    client.send(f'request {nickname}'.encode('ascii'))


send_saving_thread = threading.Thread(target=send_saving)
send_saving_thread.start()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

load_saving_thread = threading.Thread(target=request_saving)
load_saving_thread.start()

