import pygame
from hero import *
from levels import *
from enemies import *
from interface import *

# image_path = '/data/data/org.petuhondriy.myapp/files/app/'

clock = pygame.time.Clock()

# pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
intro_sound = pygame.mixer.Sound('sounds/Overrated.mp3')
bg_sound = pygame.mixer.Sound('sounds/Loops_Of_Fury.mp3')
blaster_sound = pygame.mixer.Sound('sounds/laser-blast.mp3')
key_sound = pygame.mixer.Sound('sounds/key.mp3')

gameplay = False
running = False
intro = True
scene = False

intro_sound.play(loops=-1)
while intro:
    screen.blit(start_bg, (0, 0))
    start_label_rect = start_label[start_label_count].get_rect(topleft=(240, 90))
    screen.blit(start_label[start_label_count], start_label_rect)
    start_label_count += 1
    if start_label_count == 5:
        start_label_count = 0
    screen.blit(name_label, (120, 10))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    mouse = pygame.mouse.get_pos()
    if start_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
        intro = False
        running = True
        scene = True
    clock.tick(30)

intro_sound.stop()
bg_sound.play(loops=-1)

while running:
    while scene:
        screen.blit(eval(f'bg_scene_{scene_count}'), (0, 0))
        screen.blit(continue_label, continue_label_rect)
        scene_label = label_2.render(eval(f'scene_{scene_count}_text')[scene_line][:scene_label_count], False, (209, 151, 27))
        if scene_label_count == len(eval(f'scene_{scene_count}_text')[scene_line]):
            scene_label_count = 1
            scene_line += 1
            # scene_y += 30

        key_sound.play()
        screen.blit(scene_label, (50, scene_y))
        scene_label_count += 1

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if scene_line == len(eval(f'scene_{scene_count}_text')):
            scene = False
            gameplay = True
            running = True
            clock.tick(0.5)
            scene_label_count = 1
            scene_line = 0
            # scene_y = 20

        mouse = pygame.mouse.get_pos()
        if continue_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            scene = False
            gameplay = True
            scene_label_count = 1
            scene_line = 0
            # scene_y = 20

        clock.tick(15)


    if gameplay and not scene:
        screen.blit(bg[bg_x][bg_y], (0, 0))
        platforms = eval(f'platforms_{bg_x + 1}_{bg_y + 1}')
        # platforms.draw(screen)
        walls = eval(f'walls_{bg_x + 1}_{bg_y + 1}')
        # walls.draw(screen)
        ledges_right = eval(f'ledges_right_{bg_x + 1}_{bg_y + 1}')
        # ledges_right.draw(screen)
        ledges_left = eval(f'ledges_left_{bg_x + 1}_{bg_y + 1}')
        # ledges_left.draw(screen)
        screen.blit(hp_icon, (25, 5))
        for i in range(hp):
            screen.blit(heart_icon, (41 + i * 16, 5))


        player_rect = player.get_rect(topleft=(player_x, player_y))
        ghost_rect = ghost[0].get_rect(topleft=(screen_width, player_y))
        # if ghost_list_in_game:
        #     for (i, el) in enumerate(ghost_list_in_game):
        #         screen.blit(ghost[ghost_anim_count], el)
        #         el.x -= 5
        #         if el.x < -10:
        #             ghost_list_in_game.pop(i)
        #         if not is_wounded and player_rect.colliderect(el):
        #             is_wounded = True
        #             if hp == 1:
        #                 gameplay = False
        #             hp -= 1

        keys = pygame.key.get_pressed()

        on_platform = False
        for platform in platforms:
            for i in range(platform.width // 30):
                screen.blit(tile_1, (platform.rect.x + i * 30, platform.rect.y))
            if player_rect.colliderect(platform.rect) and not is_jump_up and not is_jump_down:
                if falling_high > 8:
                    is_getup = True
                    hp -= 1
                    falling_high = 0
                if is_fall:
                    if right_orient:
                        player_x += 25
                    if not right_orient:
                        player_x -= 25
                    is_fall = False
                    falling_high = 0
                if not is_sit:
                    player_y = platform.rect.top - 77
                else:
                    player_y = platform.rect.top - 37
                falling_anim_count = 0
                on_platform = True
                is_busy = False

        for wall in walls:
            for i in range(wall.height // 30):
                screen.blit(tile_2, (wall.rect.x, wall.rect.y + i * 30))
            if player_rect.colliderect(wall.rect):
                if right_orient and not is_wounded or not right_orient and is_wounded:
                    player_x -= 15
                else:
                    player_x += 15

        for ledge in ledges_right:
            for i in range(ledge.width // 30):
                screen.blit(tile_3, (ledge.rect.x + i * 30, ledge.rect.y))
        for ledge in ledges_left:
            for i in range(ledge.width // 30):
                screen.blit(tile_3, (ledge.rect.x + i * 30, ledge.rect.y))

        if not on_platform and not is_jump_up and not is_jump_down and not is_jump:
            is_fall = True
            is_busy = True
            if right_orient:
                screen.blit(falling_right[falling_anim_count], (player_x, player_y))
            if not right_orient:
                screen.blit(falling_left[falling_anim_count], (player_x - 15, player_y))
            falling_anim_timer += 1
            if falling_anim_count == 7 and falling_anim_timer == 3:
                falling_high += 1
                falling_anim_timer = 0
                player_y += 52
            elif falling_anim_timer == 3:
                falling_high += 1
                falling_anim_count += 1
                falling_anim_timer = 0
                player_y += 0.5 * falling_anim_count ** 2

        elif is_getup:
            is_busy = True
            if right_orient:
                if getup_anim_count > 8 and getup_anim_count < 13:
                    player_x += 1
                screen.blit(getup_right[getup_anim_count], (player_x, player_y))
            if not right_orient:
                if getup_anim_count > 8 and getup_anim_count < 13:
                    player_x -= 1
                screen.blit(getup_left[getup_anim_count], (player_x, player_y))
            getup_anim_timer += 1
            if getup_anim_count == 18 and getup_anim_timer == 3:
                getup_anim_timer = 0
                getup_anim_count = 0
                player_x -= 18
                is_getup = False
                is_busy = False
            elif getup_anim_timer == 3:
                getup_anim_count += 1
                getup_anim_timer = 0

        elif is_wounded:
            is_busy = True
            if right_orient:
                if wound_anim_count < 6:
                    player_x -= 5
                if wound_anim_count > 16 and wound_anim_count < 21:
                    player_x += 1
                screen.blit(wound_right[wound_anim_count], (player_x, player_y))
            if not right_orient:
                if wound_anim_count < 6:
                    player_x += 5
                if wound_anim_count > 16 and wound_anim_count < 21:
                    player_x -= 1
                screen.blit(wound_left[wound_anim_count], (player_x, player_y))
            wound_anim_timer += 1
            if wound_anim_count == 26 and wound_anim_timer == 3:
                wound_anim_timer = 0
                wound_anim_count = 0
                player_x -= 18
                is_wounded = False
                is_busy = False
            elif wound_anim_timer == 3:
                wound_anim_count += 1
                wound_anim_timer = 0

        elif is_climb:
            if climb_anim_count == 0:
                player_y -= 120
            if right_orient:
                screen.blit(climb_right[climb_anim_count], (player_x, player_y))
            if not right_orient:
                screen.blit(climb_left[climb_anim_count], (player_x, player_y))
            climb_anim_timer += 1
            if climb_anim_count == 24 and climb_anim_timer == 1:
                climb_anim_count = 0
                climb_anim_timer = 0
                if right_orient:
                    player_x += 20
                else:
                    player_x -= 20
                is_climb = False
                is_busy = False
            elif climb_anim_timer == 1:
                climb_anim_count += 1
                climb_anim_timer = 0

        elif is_climb_down:
            if right_orient:
                screen.blit(climb_down_right[climb_down_anim_count], (player_x, player_y))
            if not right_orient:
                screen.blit(climb_down_left[climb_down_anim_count], (player_x, player_y))
            climb_down_anim_timer += 1
            if climb_down_anim_count == 24 and climb_down_anim_timer == 1:
                player_y += 120
                climb_down_anim_count = 0
                climb_down_anim_timer = 0
                is_climb_down = False
                is_busy = False
            elif climb_down_anim_timer == 1:
                climb_down_anim_count += 1
                climb_down_anim_timer = 0

        elif is_sit_down:
            if right_orient:
                screen.blit(sit_down_right[sit_down_anim_count], (player_x, player_y))
            if not right_orient:
                screen.blit(sit_down_left[sit_down_anim_count], (player_x, player_y))
            sit_down_anim_timer += 1
            if sit_down_anim_count == 6 and sit_down_anim_timer == 2:
                sit_down_anim_count = 0
                sit_down_anim_timer = 0
                is_sit_down = False
                is_busy = False
                is_sit = True
                player_y += 40
            elif sit_down_anim_timer == 2:
                sit_down_anim_count += 1
                sit_down_anim_timer = 0

        elif is_sit_up:
            if right_orient:
                screen.blit(sit_down_right[len(sit_down_right) - sit_down_anim_count - 1], (player_x, player_y))
            if not right_orient:
                screen.blit(sit_down_left[len(sit_down_right) - sit_down_anim_count - 1], (player_x, player_y))
            sit_down_anim_timer += 1
            if sit_down_anim_count == 6 and sit_down_anim_timer == 2:
                sit_down_anim_count = 0
                sit_down_anim_timer = 0
                is_sit_up = False
                is_busy = False
                is_sit = False
            elif sit_down_anim_timer == 2:
                sit_down_anim_count += 1
                sit_down_anim_timer = 0

        elif is_jump:
            if right_orient:
                screen.blit(jump_right[jump_anim_count], (player_x + 5, player_y))
                if jump_anim_count > 3 and jump_anim_count < 16:
                    player_x += 5
            if not right_orient:
                screen.blit(jump_left[jump_anim_count], (player_x - 21, player_y))
                if jump_anim_count > 3 and jump_anim_count < 16:
                    player_x -= 5
            jump_anim_timer += 1
            if jump_anim_count == 18 and jump_anim_timer == 2:
                jump_anim_count = 0
                jump_anim_timer = 0
                is_jump = False
            elif jump_anim_timer == 2:
                jump_anim_count += 1
                jump_anim_timer = 0

        elif is_jump_up:
            if right_orient:
                screen.blit(jump_up_right[jump_up_anim_count], (player_x, player_y))
            if not right_orient:
                screen.blit(jump_up_left[jump_up_anim_count], (player_x, player_y))
            jump_up_anim_timer += 1
            if jump_up_anim_count == 16 and jump_up_anim_timer == 2:
                jump_up_anim_count = 0
                jump_up_anim_timer = 0
                is_jump_up = False
                if right_orient:
                    for ledge in ledges_left:
                        if player_x + 21 > ledge.rect.left + 10 and player_x + 21 < ledge.rect.right - 10 and player_y - ledge.rect.top < 50:
                            is_climb = True
                            is_busy = True
                            player_y += 42
                if not right_orient:
                    for ledge in ledges_right:
                        if player_x + 21 > ledge.rect.left + 10 and player_x + 21 < ledge.rect.right - 10 and player_y - ledge.rect.top < 50:
                            is_climb = True
                            is_busy = True
                            player_y += 42
                if not is_climb:
                    is_jump_down = True
            elif jump_up_anim_timer == 2:
                jump_up_anim_count += 1
                jump_up_anim_timer = 0

        elif is_jump_down:
            if right_orient:
                screen.blit(jump_up_right[len(jump_up_right) - jump_up_anim_count - 1], (player_x, player_y))
            if not right_orient:
                screen.blit(jump_up_left[len(jump_up_left) - jump_up_anim_count - 1], (player_x, player_y))
            jump_up_anim_timer += 1
            if jump_up_anim_count == 16 and jump_up_anim_timer == 2:
                jump_up_anim_count = 0
                jump_up_anim_timer = 0
                player_y += 42
                is_jump_down = False
                is_busy = False
            elif jump_up_anim_timer == 2:
                jump_up_anim_count += 1
                jump_up_anim_timer = 0

        elif is_arm and not is_armed:
            is_busy = True
            if right_orient:
                screen.blit(arm_right[arm_anim_count], (player_x, player_y))
            if not right_orient:
                screen.blit(arm_left[arm_anim_count], (player_x, player_y))
            arm_anim_timer += 1
            if arm_anim_count == 12 and arm_anim_timer == 1:
                arm_anim_count = 0
                arm_anim_timer = 0
                is_arm = False
                is_armed = True
                is_busy = False
            elif arm_anim_timer == 1:
                arm_anim_count += 1
                arm_anim_timer = 0

        elif is_arm and is_armed:
            is_busy = True
            if right_orient:
                screen.blit(arm_right[len(arm_right) - arm_anim_count - 1], (player_x, player_y))
            if not right_orient:
                screen.blit(arm_left[len(arm_right) - arm_anim_count - 1], (player_x, player_y))
            arm_anim_timer += 1
            if arm_anim_count == 12 and arm_anim_timer == 1:
                arm_anim_count = 0
                arm_anim_timer = 0
                is_arm = False
                is_armed = False
                is_busy = False
            elif arm_anim_timer == 1:
                arm_anim_count += 1
                arm_anim_timer = 0

        elif is_armed and is_shoot:
            is_busy = True
            if shoot_anim_count == 2:
                blaster_sound.play()
            if right_orient:
                screen.blit(shoot_right[shoot_anim_count], (player_x + 12, player_y))
            if not right_orient:
                screen.blit(shoot_left[shoot_anim_count], (player_x - 10, player_y))
            shoot_anim_timer += 1
            if shoot_anim_count == 8 and shoot_anim_timer == 2:
                shoot_anim_count = 0
                shoot_anim_timer = 0
                is_shoot = False
                is_busy = False
            elif shoot_anim_timer == 2:
                shoot_anim_count += 1
                shoot_anim_timer = 0

        elif keys[pygame.K_UP] and not is_jump_up and not is_busy and not is_armed:
            if is_sit:
                is_sit_up = True
                player_y -= 40
                is_sit = False
            else:
                is_jump_up = True
                player_y -= 42
            is_busy = True

        elif keys[pygame.K_DOWN] and not is_busy and not is_armed:
            if right_orient:
                for ledge in ledges_left:
                    if player_x + 21 > ledge.rect.left + 20 and player_x + 21 < ledge.rect.right + 10 and ledge.rect.top - player_y < 90 and ledge.rect.top - player_y > 35:
                        is_climb_down = True
                        is_busy = True
            if not right_orient:
                for ledge in ledges_right:
                    if player_x + 21 > ledge.rect.left and player_x + 21 < ledge.rect.right - 20 and ledge.rect.top - player_y < 90 and ledge.rect.top - player_y > 35:
                        is_climb_down = True
                        is_busy = True
            if not is_climb_down and not is_sit:
                is_sit_down = True
                is_busy = True

        elif keys[pygame.K_n] and not is_busy and not is_sit and not is_armed:
            is_busy = True
            is_jump = True

        elif keys[pygame.K_SPACE] and not is_busy and not is_armed:
            is_arm = True
            is_busy = True
            if right_orient:
                player = player_armed_right
            if not right_orient:
                player = player_armed_left
        elif keys[pygame.K_SPACE] and not is_busy and is_armed:
            is_arm = True
            if right_orient:
                player = player_stay_right
            if not right_orient:
                player = player_stay_left

        elif keys[pygame.K_b] and is_armed and not is_shoot and not is_busy:
            if right_orient:
                bullets_right.append(bullet.get_rect(topleft=(player_x + 30, player_y + 15)))
            else:
                bullets_left.append(bullet.get_rect(topleft=(player_x, player_y + 15)))
            is_shoot = True
            is_busy = True

        elif keys[pygame.K_LEFT] and not is_busy and not is_sit and not is_armed:
            screen.blit(walk_left[walk_anim_count], (player_x, player_y))
            right_orient = False
            player_x -= walk_speed
            walk_anim_timer += 1
            if walk_anim_count == 11 and walk_anim_timer == 3:
                walk_anim_count = 0
                walk_anim_timer = 0
            elif walk_anim_timer == 3:
                walk_anim_count += 1
                walk_anim_timer = 0

        elif keys[pygame.K_LEFT] and not is_busy and not is_sit and is_armed:
            screen.blit(walk_armed_left[walk_armed_anim_count], (player_x, player_y))
            right_orient = False
            player_x -= walk_armed_speed
            walk_armed_anim_timer += 1
            if walk_armed_anim_count == 14 and walk_armed_anim_timer == 2:
                walk_armed_anim_count = 0
                walk_armed_anim_timer = 0
            elif walk_armed_anim_timer == 2:
                walk_armed_anim_count += 1
                walk_armed_anim_timer = 0

        elif keys[pygame.K_RIGHT] and not is_busy and not is_sit and not is_armed:
            screen.blit(walk_right[walk_anim_count], (player_x, player_y))
            right_orient = True
            player_x += walk_speed
            walk_anim_timer += 1
            if walk_anim_count == 11 and walk_anim_timer == 3:
                walk_anim_count = 0
                walk_anim_timer = 0
            elif walk_anim_timer == 3:
                walk_anim_count += 1
                walk_anim_timer = 0

        elif keys[pygame.K_RIGHT] and not is_busy and not is_sit and is_armed:
            screen.blit(walk_armed_right[walk_armed_anim_count], (player_x, player_y))
            right_orient = True
            player_x += walk_armed_speed
            walk_armed_anim_timer += 1
            if walk_armed_anim_count == 14 and walk_armed_anim_timer == 2:
                walk_armed_anim_count = 0
                walk_armed_anim_timer = 0
            elif walk_armed_anim_timer == 2:
                walk_armed_anim_count += 1
                walk_armed_anim_timer = 0

        else:
            screen.blit(player, (player_x, player_y))

        if right_orient and not is_armed and not is_sit:
            player = player_stay_right
        if not right_orient and not is_armed and not is_sit:
            player = player_stay_left
        if right_orient and is_armed and not is_sit:
            player = player_armed_right
            # screen.blit(player, (player_x + 12, player_y))
        if not right_orient and is_armed and not is_sit:
            player = player_armed_left
        if right_orient and is_sit:
            player = player_sit_right
        if not right_orient and is_sit:
            player = player_sit_left

        if player_x > screen_width-1:
            bg_x += 1
            player_x = 10
            scene = True
            scene_count += 1
        if player_x < 0:
            bg_x -= 1
            player_x = screen_width - 10
        if player_y > screen_height:
            bg_y += 1
            player_y = player_y - screen_height
        if player_y < 0 and bg_y != 0:
            bg_y -= 1
            player_y = player_y + screen_height

        ghost_anim_timer += 1
        if ghost_anim_count == 0 and ghost_anim_timer == 10:
            ghost_anim_count = 1
            ghost_anim_timer = 0
        elif ghost_anim_timer == 10:
            ghost_anim_count = 0
            ghost_anim_timer = 0

        if bullets_right:
            for (i, el) in enumerate(bullets_right):
                screen.blit(bullet, (el.x, el.y))
                el.x += 15

                if el.x < 0 or el.x > screen_width:
                    try:
                        bullets_right.pop(i)
                    except:
                        print("no bullets!")

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            try:
                                bullets_right.pop(i)
                            except:
                                print("no bullets!")

        if bullets_left:
            for (i, el) in enumerate(bullets_left):
                screen.blit(bullet, (el.x, el.y))
                el.x -= 15
                if el.x < 0 or el.x > screen_width:
                    try:
                        bullets_left.pop(i)
                    except:
                        print("no bullets!")

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            try:
                                bullets_left.pop(i)
                            except:
                                print("no bullets!")

    else:
        screen.fill((95, 165, 179))
        screen.blit(lose_label, (260, 20))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 30
            player_y = 142
            bg_x = 0
            bg_y = 0
            hp = 3
            ghost_list_in_game.clear()
            bullets_right.clear()
            bullets_left.clear()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost_rect)

    clock.tick(30)
    # elif event.type == pygame.KEYDOWN:
    #     if event.key == pygame.K_a:
    #         screen.fill((132, 3, 252))
