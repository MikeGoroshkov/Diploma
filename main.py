import pygame
from hero import *
from levels import *
from enemies import *
from interface import *
from inventory import *
from sounds import *

# image_path = '/data/data/org.petuhondriy.myapp/files/app/'

clock = pygame.time.Clock()

gameplay = False
running = False
intro = True
scene = False
controls_menu = False

intro_sound.play(loops=-1)
while intro:
    if not controls_menu:
        screen.blit(start_bg, (0, 0))
        start_label_rect = start_label[start_label_count].get_rect(topleft=(240, 90))
        screen.blit(start_label[start_label_count], start_label_rect)
        start_label_count += 1
        if start_label_count == 5:
            start_label_count = 0
        screen.blit(name_label, (120, 10))
        controls_label_rect = controls_label.get_rect(topleft=(240, 140))
        screen.blit(controls_label, controls_label_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        mouse = pygame.mouse.get_pos()
        if start_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            intro = False
            running = True
            scene = True
        if controls_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            controls_menu = True

        clock.tick(30)
    if controls_menu:
        screen.blit(start_bg, (0, 0))
        screen.blit(name_label, (120, 10))
        back_start_menu_label_rect = back_start_menu_label.get_rect(topleft=(210, 300))
        screen.blit(back_start_menu_label, back_start_menu_label_rect)
        for i, text in enumerate(controls_text):
            text_label = label_2.render(text, False, (235, 0, 4))
            screen.blit(text_label, (200, 70 + i * 25))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        mouse = pygame.mouse.get_pos()
        if back_start_menu_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            controls_menu = False

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
        if hp <= 0:
            gameplay = False
        if experience >= (level**2) * 100:
            experience -= (level**2) * 100
            level += 1
            player_damage *= 1.2
            hp_max *= 1.1
            hp *= 1.1

        screen.blit(bg[bg_y][bg_x], (0, 0))
        # platforms = eval(f'platforms_{bg_x + 1}_{bg_y + 1}')
        # # platforms.draw(screen)

        screen.blit(hp_icon, (25, 5))
        for i in range(int(hp/10)):
            screen.blit(hp_line_icon, (45 + i * 5, 5))
        level_label = label_3.render(f"Level: {level}", False, (175, 50, 50))
        screen.blit(level_label, (200, 5))
        screen.blit(exp_line_icon, (270, 9))
        for i in range(int((experience/((level**2) * 100))*10)):
            screen.blit(exp_icon, (270 + i * 10, 9))
        for i, item in enumerate(inventory_list):
            screen.blit(item.image, (590 - i * 20, 5))
        screen.blit(border, (border_x, border_y))

        player_rect = player.get_rect(topleft=(player_x, player_y))
        ghost_rect = ghost[0].get_rect(topleft=(screen_width, player_y))
        # archer_rect = archer.get_rect(topleft=(archer_x, archer_y))
        # if ghost_list_in_game:
        #     for (i, el) in enumerate(ghost_list_in_game):
        #         screen.blit(ghost[ghost_anim_count], el)
        #         el.x -= 5
        #         if el.x < -10:
        #             ghost_list_in_game.pop(i)
        #         if not is_wounded and player_rect.colliderect(el):
        #             is_wounded = True
        #             hp -= 1

        keys = pygame.key.get_pressed()

        on_platform = False
        for platform in platforms[bg_x][bg_y]:
            for i in range(platform.width // 30):
                screen.blit(tile_1, (platform.rect.x + i * 30, platform.rect.y))
            if player_rect.colliderect(platform.rect) and not is_jump_up and not is_jump_down:
                if falling_high > 8:
                    is_getup = True
                    hp -= 25
                    falling_high = 0
                if is_fall:
                    if right_orient:
                        player_x += 25
                    if not right_orient:
                        player_x -= 25
                    is_fall = False
                    falling_high = 0
                    is_busy = False
                if not is_sit:
                    player_y = platform.rect.top - 77
                else:
                    player_y = platform.rect.top - 49
                falling_anim_count = 0
                on_platform = True


        for wall in walls[bg_x][bg_y]:
            for i in range(wall.height // 30):
                screen.blit(tile_2, (wall.rect.x, wall.rect.y + i * 30))
            if player_rect.colliderect(wall.rect):
                if right_orient and not is_wounded or not right_orient and is_wounded:
                    player_x -= 15
                else:
                    player_x += 15

        for door in doors[bg_x][bg_y]:
            screen.blit(tile_door, (door.rect.x, door.rect.y))

        for ledge in ledges_right[bg_x][bg_y]:
            for i in range(ledge.width // 30):
                screen.blit(tile_3, (ledge.rect.x + i * 30, ledge.rect.y))
        for ledge in ledges_left[bg_x][bg_y]:
            for i in range(ledge.width // 30):
                screen.blit(tile_3, (ledge.rect.x + i * 30, ledge.rect.y))

        for i, item in enumerate(items_list):
            if item.bg_x == bg_x and item.bg_y == bg_y:
                screen.blit(item.image, (item.x, item.y))
                if item.rect.colliderect(player_rect) and is_sit:
                    inventory_list.append(item)
                    items_list.pop(i)

        for archer in archers_list_in_game:
            for i in range(int(archer.hp/archer.hp_max*10)):
                screen.blit(enemy_hp_line_icon, (archer.x + 15 + i * 5, archer.y - 10))
            if archer.y - player_y < 50 and archer.y - player_y > -50:
                screen.blit(archer_shoot_left[archer_shoot_anim_count], (archer.x-48, archer.y-28))
                archer_shoot_anim_timer += 1
                if archer_shoot_anim_count == 5 and archer_shoot_anim_timer == 5:
                    archer_shoot_anim_timer = 0
                    archer_shoot_anim_count = 0
                    arrows_left.append(arrow.get_rect(topleft=(archer.x, archer.y + 6)))
                    arrow_sound.play()
                elif archer_shoot_anim_timer == 5:
                    archer_shoot_anim_count += 1
                    archer_shoot_anim_timer = 0
            else:
                screen.blit(archer.archer_stay_left, (archer.x, archer.y))

        if not on_platform and not is_jump_up and not is_jump_down and not is_jump:
            is_fall = True
            is_busy = True
            is_somersault = False
            if is_sit:
                if right_orient:
                    screen.blit(falling_right[falling_anim_count], (player_x, player_y - 28))
                if not right_orient:
                    screen.blit(falling_left[falling_anim_count], (player_x - 15, player_y - 28))
            else:
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
                if is_sit:
                    screen.blit(getup_right[getup_anim_count], (player_x, player_y-28))
                else:
                    screen.blit(getup_right[getup_anim_count], (player_x, player_y))
            if not right_orient:
                if getup_anim_count > 8 and getup_anim_count < 13:
                    player_x -= 1
                if is_sit:
                    screen.blit(getup_left[getup_anim_count], (player_x, player_y-28))
                else:
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
                if is_sit:
                    screen.blit(wound_right[wound_anim_count], (player_x, player_y - 40))
                else:
                    screen.blit(wound_right[wound_anim_count], (player_x, player_y))
            if not right_orient:
                if wound_anim_count < 6:
                    player_x += 5
                if wound_anim_count > 16 and wound_anim_count < 21:
                    player_x -= 1
                if is_sit:
                    screen.blit(wound_left[wound_anim_count], (player_x, player_y - 40))
                else:
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
            if right_orient:
                screen.blit(climb_right[climb_anim_count], (player_x, player_y-120))
            if not right_orient:
                screen.blit(climb_left[climb_anim_count], (player_x, player_y-120))
            climb_anim_timer += 1
            if climb_anim_count == 24 and climb_anim_timer == 2:
                climb_anim_count = 0
                climb_anim_timer = 0
                if right_orient:
                    player_x += 10
                else:
                    player_x -= 10
                is_climb = False
                is_busy = False
                player_y -= 120
            elif climb_anim_timer == 2:
                climb_anim_count += 1
                climb_anim_timer = 0

        elif is_climb_down:
            if right_orient:
                screen.blit(climb_down_right[climb_down_anim_count], (player_x, player_y))
            if not right_orient:
                screen.blit(climb_down_left[climb_down_anim_count], (player_x, player_y))
            climb_down_anim_timer += 1
            if climb_down_anim_count == 24 and climb_down_anim_timer == 2:
                player_y += 120
                climb_down_anim_count = 0
                climb_down_anim_timer = 0
                is_climb_down = False
                is_busy = False
            elif climb_down_anim_timer == 2:
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
                player_y += 28
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

        elif is_sit_turn:
            if right_orient:
                screen.blit(sit_turn_right[sit_turn_anim_count], (player_x, player_y + 4))
            if not right_orient:
                screen.blit(sit_turn_left[sit_turn_anim_count], (player_x, player_y + 4))
            sit_turn_anim_timer += 1
            if sit_turn_anim_count == 8 and sit_turn_anim_timer == 2:
                sit_turn_anim_count = 0
                sit_turn_anim_timer = 0
                is_sit_turn = False
                is_busy = False
                if right_orient:
                    right_orient = False
                else:
                    right_orient = True
            elif sit_turn_anim_timer == 2:
                sit_turn_anim_count += 1
                sit_turn_anim_timer = 0

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
                is_busy = False
            elif jump_anim_timer == 2:
                jump_anim_count += 1
                jump_anim_timer = 0

        elif is_somersault:
            if right_orient:
                screen.blit(somersault_right[somersault_anim_count], (player_x + 15, player_y+4))
                player_x += 5
            if not right_orient:
                screen.blit(somersault_left[somersault_anim_count], (player_x - 15, player_y+4))
                player_x -= 5
            somersault_anim_timer += 1
            if somersault_anim_count == 8 and somersault_anim_timer == 2:
                somersault_anim_count = 0
                somersault_anim_timer = 0
                is_somersault = False
                is_busy = False
            elif somersault_anim_timer == 2:
                somersault_anim_count += 1
                somersault_anim_timer = 0

        elif is_jump_up:
            if right_orient:
                screen.blit(jump_up_right[jump_up_anim_count], (player_x, player_y-42))
            if not right_orient:
                screen.blit(jump_up_left[jump_up_anim_count], (player_x, player_y-42))
            jump_up_anim_timer += 1
            if jump_up_anim_count == 16 and jump_up_anim_timer == 2:
                jump_up_anim_count = 0
                jump_up_anim_timer = 0
                is_jump_up = False
                if right_orient:
                    for ledge in ledges_left[bg_x][bg_y]:
                        if player_x + 21 > ledge.rect.left and player_x + 21 < ledge.rect.right - 10 and player_y - ledge.rect.top < 50:
                            is_climb = True
                            is_busy = True
                if not right_orient:
                    for ledge in ledges_right[bg_x][bg_y]:
                        if player_x + 21 > ledge.rect.left and player_x + 21 < ledge.rect.right - 10 and player_y - ledge.rect.top < 50:
                            is_climb = True
                            is_busy = True
                if not is_climb:
                    is_jump_down = True
            elif jump_up_anim_timer == 2:
                jump_up_anim_count += 1
                jump_up_anim_timer = 0

        elif is_jump_down:
            if right_orient:
                screen.blit(jump_up_right[len(jump_up_right) - jump_up_anim_count - 1], (player_x, player_y-42))
            if not right_orient:
                screen.blit(jump_up_left[len(jump_up_left) - jump_up_anim_count - 1], (player_x, player_y-42))
            jump_up_anim_timer += 1
            if jump_up_anim_count == 16 and jump_up_anim_timer == 2:
                jump_up_anim_count = 0
                jump_up_anim_timer = 0
                is_jump_down = False
                is_busy = False
            elif jump_up_anim_timer == 2:
                jump_up_anim_count += 1
                jump_up_anim_timer = 0

        elif is_arm and not is_armed:
            is_busy = True
            if not is_sit:
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
            else:
                if right_orient:
                    screen.blit(sit_arm_right[arm_anim_count], (player_x+8, player_y))
                if not right_orient:
                    screen.blit(sit_arm_left[arm_anim_count], (player_x-8, player_y))
                arm_anim_timer += 1
                if arm_anim_count == 9 and arm_anim_timer == 1:
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
            if not is_sit:
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
            else:
                if right_orient:
                    screen.blit(sit_arm_right[len(sit_arm_right) - arm_anim_count - 1], (player_x+8, player_y))
                if not right_orient:
                    screen.blit(sit_arm_left[len(sit_arm_left) - arm_anim_count - 1], (player_x-8, player_y))
                arm_anim_timer += 1
                if arm_anim_count == 9 and arm_anim_timer == 1:
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
            if is_sit:
                if right_orient:
                    screen.blit(sit_shoot_right[shoot_anim_count], (player_x + 12, player_y))
                if not right_orient:
                    screen.blit(sit_shoot_left[shoot_anim_count], (player_x - 10, player_y))
                shoot_anim_timer += 1
                if shoot_anim_count == 5 and shoot_anim_timer == 2:
                    shoot_anim_count = 0
                    shoot_anim_timer = 0
                    is_shoot = False
                    is_busy = False
                elif shoot_anim_timer == 2:
                    shoot_anim_count += 1
                    shoot_anim_timer = 0
            else:
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

        elif keys[pygame.K_UP] and not is_jump_up and not is_busy:
            if not is_sit and not is_armed:
                is_jump_up = True
                is_busy = True
            if is_sit:
                is_sit_up = True
                player_y -= 28
                is_sit = False
                is_busy = True
            else:
                screen.blit(player, (player_x, player_y))

        elif keys[pygame.K_DOWN] and not is_busy:
            if not is_armed:
                if right_orient:
                    for ledge in ledges_left[bg_x][bg_y]:
                        if player_x + 21 > ledge.rect.left and player_x + 21 < ledge.rect.right and ledge.rect.top - player_y < 90 and ledge.rect.top - player_y > 35:
                            is_climb_down = True
                            is_busy = True
                if not right_orient:
                    for ledge in ledges_right[bg_x][bg_y]:
                        if player_x + 21 > ledge.rect.left and player_x + 21 < ledge.rect.right and ledge.rect.top - player_y < 90 and ledge.rect.top - player_y > 35:
                            is_climb_down = True
                            is_busy = True
            if not is_climb_down and not is_sit:
                is_sit_down = True
                is_busy = True
            else:
                screen.blit(player, (player_x, player_y))

        elif keys[pygame.K_n] and not is_busy and not is_sit and not is_armed:
            is_busy = True
            is_jump = True

        elif keys[pygame.K_SPACE] and not is_busy and not is_armed:
            is_arm = True
            is_busy = True
            if not is_sit:
                if right_orient:
                    player = player_armed_right
                if not right_orient:
                    player = player_armed_left
            else:
                if right_orient:
                    player = player_sit_armed_right
                if not right_orient:
                    player = player_sit_armed_left

        elif keys[pygame.K_SPACE] and not is_busy and is_armed:
            is_arm = True
            is_busy = True
            if not is_sit:
                if right_orient:
                    player = player_stay_right
                if not right_orient:
                    player = player_stay_left
            else:
                if right_orient:
                    player = player_sit_right
                if not right_orient:
                    player = player_sit_left


        elif keys[pygame.K_b] and is_armed and not is_busy:
            if is_sit:
                if right_orient:
                    bullets_right.append(bullet.get_rect(topleft=(player_x + 30, player_y + 6)))
                else:
                    bullets_left.append(bullet.get_rect(topleft=(player_x, player_y + 6)))
            else:
                if right_orient:
                    bullets_right.append(bullet.get_rect(topleft=(player_x + 30, player_y + 14)))
                else:
                    bullets_left.append(bullet.get_rect(topleft=(player_x, player_y + 14)))
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

        elif keys[pygame.K_LEFT] and not is_busy and is_sit and not is_sit_turn:
            if right_orient:
                is_busy = True
                is_sit_turn = True
            else:
                is_busy = True
                is_somersault = True

        elif keys[pygame.K_RIGHT] and not is_busy and is_sit and not is_sit_turn:
            if not right_orient:
                is_busy = True
                is_sit_turn = True
            else:
                is_busy = True
                is_somersault = True

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

        if keys[pygame.K_COMMA] and not is_delay:
            is_delay = True
            if len(inventory_list) > 1:
                if border_x == 588 - (len(inventory_list)-1) * 20:
                    border_x = 588
                    border_pos = 0
                else:
                    border_x -= 20
                    border_pos += 1

        if keys[pygame.K_v] and not is_delay:
            is_delay = True
            for i, item in enumerate(inventory_list):
                if border_pos == i:
                    if item.name == 'drug':
                        hp += 50
                        if hp > hp_max:
                            hp = hp_max
                        sip_sound.play()
                        if border_x == 588 - (len(inventory_list)-1) * 20 and (len(inventory_list) > 1):
                            border_x += 20
                            border_pos -= 1
                        inventory_list.pop(i)
                    else:
                        if item.name == 'key':
                            for door in doors[bg_x][bg_y]:
                                if player_rect.colliderect(door.rect):
                                    bg_x += 1
                                    scene = True
                                    scene_count += 1
                                    key_card_sound.play()
                                    player_x = 30
                                    if border_x == 588 - (len(inventory_list) - 1) * 20 and (len(inventory_list) > 1):
                                        border_x += 20
                                        border_pos -= 1
                                    inventory_list.pop(i)

        if is_delay:
            delay_timer += 1
            if delay_timer == 10:
                is_delay = False
                delay_timer = 0

        if right_orient and is_sit and ((is_arm and not is_armed) or is_armed):
            player = player_sit_armed_right
        if not right_orient and is_sit and ((is_arm and not is_armed) or is_armed):
            player = player_sit_armed_left
        if right_orient and not is_armed and not is_sit:
            player = player_stay_right
        if not right_orient and not is_armed and not is_sit:
            player = player_stay_left
        if right_orient and is_armed and not is_sit:
            player = player_armed_right
        if not right_orient and is_armed and not is_sit:
            player = player_armed_left
        if right_orient and is_sit and not is_arm and not is_armed:
            player = player_sit_right
        if not right_orient and is_sit and not is_arm and not is_armed:
            player = player_sit_left

        if player_x > screen_width-1:
            bg_x += 1
            player_x = 10
            if bg_x == 2 or bg_x == 4 or bg_x == 6:
                scene = True
                scene_count += 1
            for i, archer in enumerate(archers_list_in_game):
                if archer.bg_x == bg_x - 1 and archer.bg_y == bg_y:
                    archer.decrease_hp(-1000)
                    archers_list_in_game.pop(i)
            for archer in archers_full_list:
                if archer.bg_x == bg_x and archer.bg_y == bg_y:
                    if archer not in archers_list_in_game:
                        archers_list_in_game.append(archer)
            arrows_right.clear()
            arrows_left.clear()
            bullets_right.clear()
            bullets_left.clear()

        if player_x < 0 and bg_x != 0:
            bg_x -= 1
            player_x = screen_width - 10
            if bg_x == 1:
                scene_count -= 1
            for i, archer in enumerate(archers_list_in_game):
                if archer.bg_x == bg_x + 1 and archer.bg_y == bg_y:
                    archer.decrease_hp(-1000)
                    archers_list_in_game.pop(i)
            for archer in archers_full_list:
                if archer.bg_x == bg_x and archer.bg_y == bg_y:
                    if archer not in archers_list_in_game:
                        archers_list_in_game.append(archer)
            arrows_right.clear()
            arrows_left.clear()
            bullets_right.clear()
            bullets_left.clear()

        if player_y > screen_height:
            bg_y += 1
            player_y = player_y - screen_height
            for i, archer in enumerate(archers_list_in_game):
                if archer.bg_x == bg_x and archer.bg_y == bg_y - 1:
                    archer.decrease_hp(-1000)
                    archers_list_in_game.pop(i)
            for archer in archers_full_list:
                if archer.bg_x == bg_x and archer.bg_y == bg_y:
                    if archer not in archers_list_in_game:
                        archers_list_in_game.append(archer)
            arrows_right.clear()
            arrows_left.clear()
            bullets_right.clear()
            bullets_left.clear()

        if player_y < 0 and bg_y != 0:
            bg_y -= 1
            player_y = player_y + screen_height
            for i, archer in enumerate(archers_list_in_game):
                if archer.bg_x == bg_x and archer.bg_y == bg_y + 1:
                    archer.decrease_hp(-1000)
                    archers_list_in_game.pop(i)
            for archer in archers_full_list:
                if archer.bg_x == bg_x and archer.bg_y == bg_y:
                    if archer not in archers_list_in_game:
                        archers_list_in_game.append(archer)
            arrows_right.clear()
            arrows_left.clear()
            bullets_right.clear()
            bullets_left.clear()

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

                for wall in walls[bg_x][bg_y]:
                    if el.colliderect(wall.rect):
                        try:
                            bullets_right.pop(i)
                        except:
                            pass
                if el.x < 0 or el.x > screen_width:
                    try:
                        bullets_right.pop(i)
                    except:
                        pass

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            try:
                                bullets_right.pop(i)
                            except:
                                print("no bullets!")
                if archers_list_in_game:
                    for (index, archer_el) in enumerate(archers_list_in_game):
                        if el.colliderect(archer_el.archer_stay_left.get_rect(topleft=(archer_el.x, archer_el.y))):
                            archer_el.decrease_hp(player_damage)
                            if archer_el.hp <= 0:
                                archer_el.decrease_hp(-1000)
                                experience += archer_el.exp
                                archers_list_in_game.pop(index)
                            try:
                                bullets_right.pop(i)
                            except:
                                print("no bullets!")

        if arrows_right:
            for (i, el) in enumerate(arrows_right):
                screen.blit(arrow, (el.x, el.y))
                el.x += 15

                for wall in walls[bg_x][bg_y]:
                    if el.colliderect(wall.rect):
                        try:
                            arrows_right.pop(i)
                        except:
                            pass
                if el.x < 0 or el.x > screen_width:
                    try:
                        arrows_right.pop(i)
                    except:
                        pass

                if el.colliderect(player_rect):
                    hp -= archer_1.damage
                    try:
                        arrows_right.pop(i)
                    except:
                        print("ops!")

        if bullets_left:
            for (i, el) in enumerate(bullets_left):
                screen.blit(bullet, (el.x, el.y))
                el.x -= 15

                for wall in walls[bg_x][bg_y]:
                    if el.colliderect(wall.rect):
                        try:
                            bullets_left.pop(i)
                        except:
                            pass
                if el.x < 0 or el.x > screen_width:
                    try:
                        bullets_left.pop(i)
                    except:
                        pass

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            try:
                                bullets_left.pop(i)
                            except:
                                print("no bullets!")

                if archers_list_in_game:
                    for (index, archer_el) in enumerate(archers_list_in_game):
                        if el.colliderect(archer_el.archer_stay_left.get_rect(topleft=(archer_el.x, archer_el.y))):
                            archer_el.decrease_hp(player_damage)
                            if archer_el.hp <= 0:
                                archer_el.decrease_hp(-1000)
                                experience += archer_el.exp
                                archers_list_in_game.pop(index)
                            try:
                                bullets_left.pop(i)
                            except:
                                print("no bullets!")

        if arrows_left:
            for (i, el) in enumerate(arrows_left):
                screen.blit(arrow, (el.x, el.y))
                el.x -= 15

                for wall in walls[bg_x][bg_y]:
                    if el.colliderect(wall.rect):
                        try:
                            arrows_left.pop(i)
                        except:
                            pass
                if el.x < 0 or el.x > screen_width:
                    try:
                        arrows_left.pop(i)
                    except:
                        print("ops!")

                if el.colliderect(player_rect):
                    hp -= archer_1.damage
                    try:
                        arrows_left.pop(i)
                    except:
                        print("ops!")

    else:
        screen.fill((95, 165, 179))
        screen.blit(lose_label, (260, 20))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 50
            player_y = 142
            bg_x = 0
            bg_y = 0
            hp = 100
            ghost_list_in_game.clear()
            archers_list_in_game = [archer_1]
            bullets_right.clear()
            bullets_left.clear()
            arrows_right.clear()
            arrows_left.clear()
            inventory_list = []
            items_list = items_list_start[:]

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
