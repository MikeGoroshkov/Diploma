import pygame

label_0 = pygame.font.Font('fonts/Pangolin-Regular.ttf', 50)
label = pygame.font.Font('fonts/Pangolin-Regular.ttf', 30)
label_2 = pygame.font.Font('fonts/Pangolin-Regular.ttf', 15)

name_label = label_0.render("Escape from Zefira", False, (209, 151, 27))
lose_label = label.render("You lose!", False, (219, 24, 24))
restart_label = label.render("Restart game", False, (219, 24, 24))
restart_label_rect = restart_label.get_rect(topleft=(240, 90))

continue_label = label.render("Continue", False, (219, 24, 24))
continue_label_rect = continue_label.get_rect(topleft=(240, 250))

start_label = [label.render("Start game", False, (150 + i * 20, 151, 27)) for i in range(5)]
start_label_count = 0

scene_1_text = ['Главный герой игры, Алекс, молодой ученый, работающий ',
               'над экспериментом в области телепортации на секретной лабораторной базе.',
               'Во время одного из экспериментов происходит неожиданная неудача, и Алекс',
               'оказывается телепортированным в другой инопланетный мир.']

scene_2_text = ['Главный герой игры, Алекс, молодой ученый, работающий ',
               'над экспериментом в области телепортации на секретной лабораторной базе.',
               'Во время одного из экспериментов происходит неожиданная неудача, и Алекс',
               'оказывается телепортированным в другой инопланетный мир.']


scene_label_count = 1
scene_line = 0
scene_y = 20

heart_icon = pygame.image.load('images/heart.png').convert_alpha()
hp_icon = pygame.image.load('images/hp.png').convert_alpha()
