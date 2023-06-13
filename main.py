import pygame
from hero import *
from levels import *


# image_path = '/data/data/org.petuhondriy.myapp/files/app/'

clock = pygame.time.Clock()


# square = pygame.Surface((250, 170))
# square.fill('Blue')
# myfont = pygame.font.Font('fonts/Pangolin-Regular.ttf', 40)  #https://fonts.google.com/
# text_surface = myfont.render('first_game', False, 'Red') #False - antilissing

ghost = [
    pygame.image.load('images/ghost_1.png').convert_alpha(),
    pygame.image.load('images/ghost_2.png').convert_alpha()
    ]
ghost_list_in_game = []

player_anim_count = 0
player_anim_timer = 0
ghost_anim_count = 0
ghost_anim_timer = 0

player_speed = 5
player_x = 10
player_y = 10

bg_x = 0

is_jump = False
jump_count = 8

bg_count = 0

# pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
bg_sound = pygame.mixer.Sound('sounds/Loops_Of_Fury.mp3')
bg_sound.play(loops=-1)

ghost_timer = pygame.USEREVENT = 1
pygame.time.set_timer(ghost_timer, 2500)

label = pygame.font.Font('fonts/Pangolin-Regular.ttf', 30)
lose_label = label.render("You lose!", False, (219, 24, 24))
restart_label = label.render("Restart game!", False, (219, 24, 24))
restart_label_rect = restart_label.get_rect(topleft=(50, 150))

bullets_left = 5
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []

gameplay = True

running = True
while running:
    # screen.blit(square, (100,0))
    # screen.blit(text_surface, (text_x, text_y))

    screen.blit(bg[bg_count], (0,0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
        ghost_rect = ghost[0].get_rect(topleft=(screen_width, 10))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost[ghost_anim_count], el)
                el.x -= 8
                if el.x < -10:
                    ghost_list_in_game.pop(i)
                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x >= 0:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x <= screen_width:
            player_x += player_speed

        if player_x > 630:
            bg_count += 1
            player_x = 0
        if player_x < 0:
            bg_count -= 1
            player_x = 630

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        player_anim_timer += 1
        if player_anim_count == 2 and player_anim_timer == 5:
            player_anim_count = 0
            player_anim_timer = 0
        elif player_anim_timer == 5:
            player_anim_count += 1
            player_anim_timer = 0

        ghost_anim_timer += 1
        if ghost_anim_count == 0 and ghost_anim_timer == 10:
            ghost_anim_count = 1
            ghost_anim_timer = 0
        elif ghost_anim_timer == 10:
            ghost_anim_count = 0
            ghost_anim_timer = 0

        # pygame.draw.circle(square, 'Red', (10, 10), 5)
        #screen.fill((3, 202, 252)) #google color picker

        if bullets:
            for (i,el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 15

                if el.x > screen_width:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((95, 165, 179))
        screen.blit(lose_label, (50, 50))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 10
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost_rect)
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b:
            bullets.append(bullet.get_rect(topleft=(player_x+30,player_y+10)))
            bullets_left -= 1

    clock.tick(30)
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_a:
        #         screen.fill((132, 3, 252))



