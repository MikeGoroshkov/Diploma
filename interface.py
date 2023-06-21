import pygame

label_0 = pygame.font.Font('fonts/Pangolin-Regular.ttf', 50)
label = pygame.font.Font('fonts/Pangolin-Regular.ttf', 30)
label_2 = pygame.font.Font('fonts/Pangolin-Regular.ttf', 20)
label_3 = pygame.font.Font('fonts/Pangolin-Regular.ttf', 16)

name_label = label_0.render("Escape from Zefira", False, (209, 151, 27))
lose_label = label.render("You lose!", False, (219, 24, 24))
restart_label = label.render("Restart game", False, (219, 24, 24))
restart_label_rect = restart_label.get_rect(topleft=(240, 90))

continue_label = label.render("Continue", False, (209, 151, 27))
continue_label_rect = continue_label.get_rect(topleft=(250, 250))

start_label = [label.render("Start game", False, (150 + i * 20, 151, 27)) for i in range(5)]
start_label_count = 0

controls_label = label.render("Controls", False, (209, 151, 27))
back_start_menu_label = label.render("Back start menu", False, (209, 151, 27))

controls_text = ['CONTROLS:',
                 'space - get/put away a weapon',
                 'B - shoot',
                 'N - jump',
                 'V - use item',
                 '< - switch item',
                 'left, right - walk',
                 'up - climb up',
                 'down - sit down, climb down']


scene_count = 1
scene_1_text = ['Главный герой игры, Алекс, молодой ученый, работающий ',
               'над экспериментом в области телепортации на секретной',
               'лабораторной базе.Во время одного из экспериментов',
               'происходит неожиданная неудача, и Алекс оказывается',
                'телепортированным в другой инопланетный мир']
bg_scene_1 = pygame.image.load('images/bg_scene_1.png').convert_alpha()

scene_2_text = ['Алекс встречает там местную сопротивление',
                'группу ученых, инженеров и бойцов, которые сражаются против',
               'захватчиков. Оказывается, что враждебные инопланетные существа',
                'начали вторжение, пытаясь захватить планету и использовать ее',
                'ресурсы для своих зловещих целей']
bg_scene_2 = pygame.image.load('images/bg_scene_2.png').convert_alpha()

scene_label_count = 1
scene_line = 0
scene_y = 20
