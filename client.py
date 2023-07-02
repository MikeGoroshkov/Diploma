# Система сохранения на удаленном сервере в игре

import socket
import threading
import time

# Тестовые значения параметров
# player.nickname, player.x, player.y, player.hp, player.hp_max, player.damage, player.experience, player.level, bg_x, bg_y = 'player', 50, 142, 100, 100, 25, 0, 1, 0, 0

def save_game(nickname, x, y, hp, hp_max, damage, experience, level, bg_x, bg_y, scene_count):
    try:
        save_message = f'{nickname};{str(int(x))};{str(int(y))};{str(int(hp))};{str(int(hp_max))};{str(int(damage))};{str(int(experience))};{str(int(level))};{str(int(bg_x))};{str(int(bg_y))};{str(int(scene_count))}'
        return save_message
    except:
        print("Failed to save game!")

def load_game(load_message):
    try:
        load_tuple = tuple(load_message.split(";"))
        nickname = load_tuple[0]
        x = int(load_tuple[1])
        y = int(load_tuple[2])
        hp = int(load_tuple[3])
        hp_max = int(load_tuple[4])
        damage = int(load_tuple[5])
        experience = int(load_tuple[6])
        level = int(load_tuple[7])
        bg_x = int(load_tuple[8])
        bg_y = int(load_tuple[9])
        scene_count = int(load_tuple[10])
        print("Save applied")
        game_loaded = True
        return game_loaded, nickname, x, y, hp, hp_max, damage, experience, level, bg_x, bg_y, scene_count
    except:
        print("Failed to load game!")


def send_save(nickname, x, y, hp, hp_max, damage, experience, level, bg_x, bg_y, scene_count):
    start_time = time.time()
    while True:
        timer = time.time()
        if timer - start_time < 10:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('89.223.122.20', 55555))
                save_message = save_game(nickname, x, y, hp, hp_max, damage, experience, level, bg_x, bg_y, scene_count)
                client.send(save_message.encode('ascii'))
                print("Save sent")
                client.close()
                break
            except:
                pass
        else:
            print("server not responding, save failed")
            break

def request_save(nickname):
    start_time = time.time()
    while True:
        timer = time.time()
        if timer - start_time < 10:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('89.223.122.20', 55555))
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
                game_loaded, nickname, x, y, hp, hp_max, damage, experience, level, bg_x, bg_y, scene_count = load_game(message)
                client.close()
                return game_loaded, nickname, x, y, hp, hp_max, damage, experience, level, bg_x, bg_y, scene_count
            except:
                pass
        else:
            print("server not responding, load failed")
            break


# send_save_thread = threading.Thread(target=send_save)
# send_save_thread.start()
# time.sleep(3)
#
# load_save_thread = threading.Thread(target=request_save)
# load_save_thread.start()


