# Система сохранения на удаленном сервере в игре

import socket
import threading
import time

# Тестовые значения параметров
nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y = 'player', 50, 142, 100, 100, 25, 0, 1, 0, 0

def save_game(nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y):
    try:
        save_message = f'{nickname};{player_x};{player_y};{hp};{hp_max};{player_damage};{experience};{level};{bg_x};{bg_y}'
        return save_message
    except:
        print("Failed to save game!")

def load_game(load_message):
    global nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y
    try:
        nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y = tuple(load_message.split(";"))
        print("Saving applied")
    except:
        print("Failed to load game!")


def send_save():
    start_time = time.time()
    while True:
        timer = time.time()
        if timer - start_time < 10:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('192.168.43.14', 55555))
                save_message = save_game(nickname, player_x, player_y, hp, hp_max, player_damage, experience, level, bg_x, bg_y)
                client.send(save_message.encode('ascii'))
                print("Saving sent")
                client.close()
                break
            except:
                pass
        else:
            print("server not responding, save failed")
            break

def request_save():
    start_time = time.time()
    while True:
        timer = time.time()
        if timer - start_time < 10:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('192.168.43.14', 55555))
                client.send(f'request {nickname}'.encode('ascii'))
                print("Request sent")
                break
            except:
                pass
        else:
            print("server not responding, load failed")
            break
    while True:
        timer = time.time()
        if timer - start_time < 10:
            try:
                message = client.recv(1024).decode('ascii')
                print("Save loaded")
                load_game(message)
                client.close()
                break
            except:
                pass
        else:
            print("server not responding, load failed")
            break


send_save_thread = threading.Thread(target=send_save)
send_save_thread.start()
time.sleep(3)

load_save_thread = threading.Thread(target=request_save)
load_save_thread.start()


