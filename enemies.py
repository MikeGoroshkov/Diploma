import pygame

ghost_timer = pygame.USEREVENT = 1
pygame.time.set_timer(ghost_timer, 2500)
ghost_anim_count = 0
ghost_anim_timer = 0

ghost = [
    pygame.image.load('images/ghost_1.png').convert_alpha(),
    pygame.image.load('images/ghost_2.png').convert_alpha()
    ]
ghost_list_in_game = []