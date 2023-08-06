import pygame
from hero import *
from levels import *
from enemies import *
from interface import *
from inventory import *
from sounds import *
from client import *



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
        load_game_label_rect = load_game_label.get_rect(topleft=(240, 140))
        controls_label_rect = controls_label.get_rect(topleft=(240, 190))
        screen.blit(load_game_label, load_game_label_rect)
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
        if load_game_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            # load_save_thread = threading.Thread(target=request_save(player.nickname))
            # load_save_thread.start()
            try:
                game_loaded, player.nickname, player.x, player.y, player.hp, player.hp_max, player.damage, player.experience, player.level, bg_x, bg_y, scene_count = request_save(player.nickname)
                if game_loaded:
                    intro = False
                    running = True
                    gameplay = True
            except:
                pass
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
        screen.blit(scene_label, (25, scene_y))
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
        if scene_count == 5:
            gameplay = False

        clock.tick(15)


    if gameplay and not scene:
        if player.hp <= 0:
            gameplay = False
        if player.experience >= (player.level**2) * 100:
            player.experience -= (player.level**2) * 100
            player.level += 1
            player.damage = int(player.damage*1.2)
            player.hp_max = int(player.hp_max*1.1)
            player.hp = int(player.hp*1.1)

        screen.blit(bg[player.bg_y][player.bg_x], (0, 0))
        # platforms = eval(f'platforms_{bg_x + 1}_{bg_y + 1}')
        # # platforms.draw(screen)

        screen.blit(player.hp_icon, (25, 5))
        for i in range(int(player.hp/10)):
            screen.blit(player.hp_line_icon, (45 + i * 5, 5))
        player.level_label = label_3.render(f"level: {player.level}", False, (175, 50, 50))
        screen.blit(player.level_label, (200, 5))
        screen.blit(player.exp_line_icon, (270, 9))
        for i in range(int((player.experience/((player.level**2) * 100))*10)):
            screen.blit(player.exp_icon, (270 + i * 10, 9))
        for i, item in enumerate(inventory_list):
            screen.blit(item.image, (590 - i * 20, 5))
        screen.blit(border, (border_x, border_y))

        player.rect = hero.get_rect(topleft=(player.x, player.y))
        keys = pygame.key.get_pressed()

        player.on_platform = False
        for platform in platforms[player.bg_x][player.bg_y]:
            for i in range(platform.width // 30):
                screen.blit(tile_1, (platform.rect.x + i * 30, platform.rect.y))
            if player.rect.colliderect(platform.rect) and not player.is_jump_up and not player.is_jump_down:
                if player.falling_high > 8:
                    player.is_getup = True
                    player.hp -= 25
                    player.falling_high = 0
                if player.is_fall:
                    if player.right_orient:
                        player.x += 25
                    if not player.right_orient:
                        player.x -= 25
                    player.is_fall = False
                    player.falling_high = 0
                    player.is_busy = False
                if not player.is_sit:
                    player.y = platform.rect.top - 77
                else:
                    player.y = platform.rect.top - 49
                falling_anim_count = 0
                player.on_platform = True

        for wall in walls[player.bg_x][player.bg_y]:
            for i in range(wall.height // 30):
                screen.blit(tile_2, (wall.rect.x, wall.rect.y + i * 30))
            if player.rect.colliderect(wall.rect):
                if player.right_orient and not player.is_wounded or not player.right_orient and player.is_wounded:
                    player.x -= 15
                else:
                    player.x += 15

        for door in doors[player.bg_x][player.bg_y]:
            if player.bg_x == 7 and player.bg_y == 1:
                screen.blit(spaceship, (door.rect.x, door.rect.y))
            else:
                screen.blit(tile_door, (door.rect.x, door.rect.y))

        for ledge in ledges_right[player.bg_x][player.bg_y]:
            for i in range(ledge.width // 30):
                screen.blit(tile_3, (ledge.rect.x + i * 30, ledge.rect.y))
        for ledge in ledges_left[player.bg_x][player.bg_y]:
            for i in range(ledge.width // 30):
                screen.blit(tile_3, (ledge.rect.x + i * 30, ledge.rect.y))

        for i, item in enumerate(items_list):
            if item.bg_x == player.bg_x and item.bg_y == player.bg_y:
                screen.blit(item.image, (item.x, item.y))
                if item.rect.colliderect(player.rect) and player.is_sit:
                    inventory_list.append(item)
                    items_list.pop(i)

        for index, archer in enumerate(archers_list_in_game):
            if archer.alive:
                for i in range(int(archer.hp/archer.hp_max*10)):
                    screen.blit(enemy_hp_line_icon, (archer.x + 15 + i * 5, archer.y - 10))
                if archer.y - player.y < 50 and archer.y - player.y > -50:
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
            else:
                screen.blit(archer_died_left[archer_died_anim_count], (archer.x - 30 + archer_died_anim_count * 10, archer.y - 28))
                archer_died_anim_timer += 1
                if archer_died_anim_count == 5 and archer_died_anim_timer == 4:
                    archer_died_anim_timer = 0
                    archer_died_anim_count = 0
                    archer.alive = True
                    archers_list_in_game.pop(index)
                elif archer_died_anim_timer == 4:
                    archer_died_anim_count += 1
                    archer_died_anim_timer = 0

        for index, soldier in enumerate(soldiers_list_in_game):
            if soldier.alive:
                for i in range(int(soldier.hp/soldier.hp_max*10)):
                    screen.blit(enemy_hp_line_icon, (soldier.x + 10 + i * 5, soldier.y + 5))
                if soldier.y - player.y < 50 and soldier.y - player.y > -50:
                    if player.x >= soldier.x:
                        screen.blit(soldier_shoot_right[soldier_shoot_anim_count], (soldier.x, soldier.y))
                    if player.x < soldier.x:
                        screen.blit(soldier_shoot_left[soldier_shoot_anim_count], (soldier.x, soldier.y))
                    soldier_shoot_anim_timer += 1
                    if soldier_shoot_anim_count == 2 and soldier_shoot_anim_timer == 5:
                        soldier_shoot_anim_timer = 0
                        soldier_shoot_anim_count = 0
                        if player.x >= soldier.x:
                            pellets_right.append(pellet.get_rect(topleft=(soldier.x + 56, soldier.y + 24)))
                        if player.x < soldier.x:
                            pellets_left.append(pellet.get_rect(topleft=(soldier.x + 17, soldier.y + 24)))
                        shoot_sound.play()
                    elif soldier_shoot_anim_timer == 5:
                        soldier_shoot_anim_count += 1
                        soldier_shoot_anim_timer = 0
                else:
                    screen.blit(soldier.soldier_stay_left, (soldier.x, soldier.y))
            else:
                if player.x >= soldier.x:
                    screen.blit(soldier_died_right[soldier_died_anim_count], (soldier.x - soldier_died_anim_count * 10, soldier.y))
                if player.x < soldier.x:
                    screen.blit(soldier_died_left[soldier_died_anim_count], (soldier.x + soldier_died_anim_count * 10, soldier.y))
                soldier_died_anim_timer += 1
                if soldier_died_anim_count == 3 and soldier_died_anim_timer == 4:
                    soldier_died_anim_timer = 0
                    soldier_died_anim_count = 0
                    soldier.alive = True
                    soldiers_list_in_game.pop(index)
                elif soldier_died_anim_timer == 4:
                    soldier_died_anim_count += 1
                    soldier_died_anim_timer = 0

        for index, fly in enumerate(fly_list_in_game):
            if fly.alive:
                if fly.fly_stay_left.get_rect(topleft=(fly.x, fly.y)).colliderect(player.rect) and not player.is_wounded and not player.is_somersault and not player.is_climb and not player.is_climb_down:
                    player.is_wounded = True
                    player.hp -= fly.damage
                for i in range(int(fly.hp/fly.hp_max*10)):
                    screen.blit(enemy_hp_line_icon, (fly.x + i * 5, fly.y - 5))
                if fly.x_0 - fly.x > fly.width:
                    fly.right =True
                if fly.x_0 - fly.x < 0:
                    fly.right = False
                if fly.right:
                    screen.blit(fly_right[fly_anim_count], (fly.x, fly.y))
                    fly.x += 5
                if not fly.right:
                    screen.blit(fly_left[fly_anim_count], (fly.x, fly.y))
                    fly.x -= 5
                fly_anim_timer += 1
                if fly_anim_count == 0:
                    flap_sound.play()
                if fly_anim_count == 3 and fly_anim_timer == 5:
                    fly_anim_timer = 0
                    fly_anim_count = 0
                elif fly_anim_timer == 5:
                    fly_anim_count += 1
                    fly_anim_timer = 0
            else:
                if fly.right:
                    screen.blit(fly_died_right[fly_died_anim_count], (fly.x, fly.y))
                if not fly.right:
                    screen.blit(fly_died_left[fly_died_anim_count], (fly.x, fly.y))
                fly_died_anim_timer += 1
                if fly_died_anim_count == 2 and fly_died_anim_timer == 5:
                    fly_died_anim_timer = 0
                    fly_died_anim_count = 0
                    fly.alive = True
                    fly.x = fly.x_0
                    fly.y = fly.y_0
                    fly_list_in_game.pop(index)
                elif fly_died_anim_timer == 5:
                    fly_died_anim_count += 1
                    fly_died_anim_timer = 0

        for index, alien in enumerate(aliens_list_in_game):
            if alien.alive:
                if alien_walk_anim_count < 3:
                    alien.shock = True
                else:
                    alien.shock = False
                if alien.alien_stay_left.get_rect(topleft=(alien.x, alien.y)).colliderect(player.rect) and player.alien.shock and not player.is_wounded and not player.is_somersault and not player.is_climb and not player.is_climb_down:
                    player.is_wounded = True
                    player.hp -= alien.damage
                for i in range(int(alien.hp/alien.hp_max*10)):
                    screen.blit(enemy_hp_line_icon, (alien.x + i * 5, alien.y + 5))
                if alien.x_0 - alien.x > alien.width:
                    alien.right = True
                if alien.x_0 - alien.x < 0:
                    alien.right = False
                if alien.right:
                    screen.blit(alien_walk_right[alien_walk_anim_count], (alien.x, alien.y))
                    alien.x += 3
                if not alien.right:
                    screen.blit(alien_walk_left[alien_walk_anim_count], (alien.x, alien.y))
                    alien.x -= 3
                alien_walk_anim_timer += 1
                if alien_walk_anim_count == 0:
                    shock_sound.play()
                if alien_walk_anim_count == 9 and alien_walk_anim_timer == 5:
                    alien_walk_anim_timer = 0
                    alien_walk_anim_count = 0
                elif alien_walk_anim_timer == 5:
                    alien_walk_anim_count += 1
                    alien_walk_anim_timer = 0
            else:
                if alien.right:
                    screen.blit(alien_died_right[alien_died_anim_count], (alien.x, alien.y))
                if not alien.right:
                    screen.blit(alien_died_left[alien_died_anim_count], (alien.x, alien.y))
                alien_died_anim_timer += 1
                if alien_died_anim_count == 4 and alien_died_anim_timer == 5:
                    alien_died_anim_timer = 0
                    alien_died_anim_count = 0
                    alien.alive = True
                    alien.x = alien.x_0
                    alien.y = alien.y_0
                    aliens_list_in_game.pop(index)
                elif alien_died_anim_timer == 5:
                    alien_died_anim_count += 1
                    alien_died_anim_timer = 0

        if not player.on_platform and not player.is_jump_up and not player.is_jump_down and not player.is_jump:
            player.is_fall = True
            player.is_busy = True
            player.is_somersault = False
            if player.is_sit:
                if player.right_orient:
                    screen.blit(falling_right[falling_anim_count], (player.x, player.y - 28))
                if not player.right_orient:
                    screen.blit(falling_left[falling_anim_count], (player.x - 15, player.y - 28))
            else:
                if player.right_orient:
                    screen.blit(falling_right[falling_anim_count], (player.x, player.y))
                if not player.right_orient:
                    screen.blit(falling_left[falling_anim_count], (player.x - 15, player.y))
            falling_anim_timer += 1
            if falling_anim_count == 7 and falling_anim_timer == 3:
                player.falling_high += 1
                falling_anim_timer = 0
                player.y += 52
            elif falling_anim_timer == 3:
                player.falling_high += 1
                falling_anim_count += 1
                falling_anim_timer = 0
                player.y += 0.5 * falling_anim_count ** 2

        elif player.is_getup:
            player.is_busy = True
            if player.right_orient:
                if getup_anim_count > 8 and getup_anim_count < 13:
                    player.x += 1
                if player.is_sit:
                    screen.blit(getup_right[getup_anim_count], (player.x, player.y-28))
                else:
                    screen.blit(getup_right[getup_anim_count], (player.x, player.y))
            if not player.right_orient:
                if getup_anim_count > 8 and getup_anim_count < 13:
                    player.x -= 1
                if player.is_sit:
                    screen.blit(getup_left[getup_anim_count], (player.x, player.y-28))
                else:
                    screen.blit(getup_left[getup_anim_count], (player.x, player.y))
            getup_anim_timer += 1
            if getup_anim_count == 18 and getup_anim_timer == 3:
                getup_anim_timer = 0
                getup_anim_count = 0
                player.x -= 18
                player.is_getup = False
                player.is_busy = False
            elif getup_anim_timer == 3:
                getup_anim_count += 1
                getup_anim_timer = 0

        elif player.is_wounded:
            player.is_busy = True
            if player.right_orient:
                if wound_anim_count < 6:
                    player.x -= 5
                if wound_anim_count > 16 and wound_anim_count < 21:
                    player.x += 1
                if player.is_sit:
                    screen.blit(wound_right[wound_anim_count], (player.x, player.y - 28))
                else:
                    screen.blit(wound_right[wound_anim_count], (player.x, player.y))
            if not player.right_orient:
                if wound_anim_count < 6:
                    player.x += 5
                if wound_anim_count > 16 and wound_anim_count < 21:
                    player.x -= 1
                if player.is_sit:
                    screen.blit(wound_left[wound_anim_count], (player.x, player.y - 28))
                else:
                    screen.blit(wound_left[wound_anim_count], (player.x, player.y))
            wound_anim_timer += 1
            if wound_anim_count == 26 and wound_anim_timer == 3:
                wound_anim_timer = 0
                wound_anim_count = 0
                player.x -= 18
                player.is_wounded = False
                player.is_busy = False
            elif wound_anim_timer == 3:
                wound_anim_count += 1
                wound_anim_timer = 0

        elif player.is_climb:
            if player.right_orient:
                screen.blit(climb_right[climb_anim_count], (player.x, player.y-120))
            if not player.right_orient:
                screen.blit(climb_left[climb_anim_count], (player.x, player.y-120))
            climb_anim_timer += 1
            if climb_anim_count == 24 and climb_anim_timer == 2:
                climb_anim_count = 0
                climb_anim_timer = 0
                if player.right_orient:
                    player.x += 10
                else:
                    player.x -= 10
                player.is_climb = False
                player.is_busy = False
                player.y -= 120
            elif climb_anim_timer == 2:
                climb_anim_count += 1
                climb_anim_timer = 0

        elif player.is_climb_down:
            if player.right_orient:
                screen.blit(climb_down_right[climb_down_anim_count], (player.x, player.y))
            if not player.right_orient:
                screen.blit(climb_down_left[climb_down_anim_count], (player.x, player.y))
            climb_down_anim_timer += 1
            if climb_down_anim_count == 24 and climb_down_anim_timer == 2:
                player.y += 120
                climb_down_anim_count = 0
                climb_down_anim_timer = 0
                player.is_climb_down = False
                player.is_busy = False
            elif climb_down_anim_timer == 2:
                climb_down_anim_count += 1
                climb_down_anim_timer = 0

        elif player.is_sit_down:
            if player.right_orient:
                screen.blit(sit_down_right[sit_down_anim_count], (player.x, player.y))
            if not player.right_orient:
                screen.blit(sit_down_left[sit_down_anim_count], (player.x, player.y))
            sit_down_anim_timer += 1
            if sit_down_anim_count == 6 and sit_down_anim_timer == 2:
                sit_down_anim_count = 0
                sit_down_anim_timer = 0
                player.is_sit_down = False
                player.is_busy = False
                player.is_sit = True
                player.y += 28
            elif sit_down_anim_timer == 2:
                sit_down_anim_count += 1
                sit_down_anim_timer = 0

        elif player.is_sit_up:
            if player.right_orient:
                screen.blit(sit_down_right[len(sit_down_right) - sit_down_anim_count - 1], (player.x, player.y))
            if not player.right_orient:
                screen.blit(sit_down_left[len(sit_down_right) - sit_down_anim_count - 1], (player.x, player.y))
            sit_down_anim_timer += 1
            if sit_down_anim_count == 6 and sit_down_anim_timer == 2:
                sit_down_anim_count = 0
                sit_down_anim_timer = 0
                player.is_sit_up = False
                player.is_busy = False
                player.is_sit = False
            elif sit_down_anim_timer == 2:
                sit_down_anim_count += 1
                sit_down_anim_timer = 0

        elif player.is_sit_turn:
            if player.right_orient:
                screen.blit(sit_turn_right[sit_turn_anim_count], (player.x, player.y + 4))
            if not player.right_orient:
                screen.blit(sit_turn_left[sit_turn_anim_count], (player.x, player.y + 4))
            sit_turn_anim_timer += 1
            if sit_turn_anim_count == 8 and sit_turn_anim_timer == 2:
                sit_turn_anim_count = 0
                sit_turn_anim_timer = 0
                player.is_sit_turn = False
                player.is_busy = False
                if player.right_orient:
                    player.right_orient = False
                else:
                    player.right_orient = True
            elif sit_turn_anim_timer == 2:
                sit_turn_anim_count += 1
                sit_turn_anim_timer = 0

        elif player.is_jump:
            if player.right_orient:
                screen.blit(jump_right[jump_anim_count], (player.x + 5, player.y))
                if jump_anim_count > 3 and jump_anim_count < 16:
                    player.x += 5
            if not player.right_orient:
                screen.blit(jump_left[jump_anim_count], (player.x - 21, player.y))
                if jump_anim_count > 3 and jump_anim_count < 16:
                    player.x -= 5
            jump_anim_timer += 1
            if jump_anim_count == 18 and jump_anim_timer == 2:
                jump_anim_count = 0
                jump_anim_timer = 0
                player.is_jump = False
                player.is_busy = False
            elif jump_anim_timer == 2:
                jump_anim_count += 1
                jump_anim_timer = 0

        elif player.is_somersault:
            if player.right_orient:
                screen.blit(somersault_right[somersault_anim_count], (player.x + 15, player.y+4))
                player.x += 5
            if not player.right_orient:
                screen.blit(somersault_left[somersault_anim_count], (player.x - 15, player.y+4))
                player.x -= 5
            somersault_anim_timer += 1
            if somersault_anim_count == 8 and somersault_anim_timer == 2:
                somersault_anim_count = 0
                somersault_anim_timer = 0
                player.is_somersault = False
                player.is_busy = False
            elif somersault_anim_timer == 2:
                somersault_anim_count += 1
                somersault_anim_timer = 0

        elif player.is_jump_up:
            if player.right_orient:
                screen.blit(jump_up_right[jump_up_anim_count], (player.x, player.y-42))
            if not player.right_orient:
                screen.blit(jump_up_left[jump_up_anim_count], (player.x, player.y-42))
            jump_up_anim_timer += 1
            if jump_up_anim_count == 16 and jump_up_anim_timer == 2:
                jump_up_anim_count = 0
                jump_up_anim_timer = 0
                player.is_jump_up = False
                if player.right_orient:
                    for ledge in ledges_left[player.bg_x][player.bg_y]:
                        if player.x + 21 > ledge.rect.left and player.x + 21 < ledge.rect.right - 10 and player.y - ledge.rect.top < 50:
                            player.is_climb = True
                            player.is_busy = True
                if not player.right_orient:
                    for ledge in ledges_right[player.bg_x][player.bg_y]:
                        if player.x + 21 > ledge.rect.left and player.x + 21 < ledge.rect.right - 10 and player.y - ledge.rect.top < 50:
                            player.is_climb = True
                            player.is_busy = True
                if not player.is_climb:
                    player.is_jump_down = True
            elif jump_up_anim_timer == 2:
                jump_up_anim_count += 1
                jump_up_anim_timer = 0

        elif player.is_jump_down:
            if player.right_orient:
                screen.blit(jump_up_right[len(jump_up_right) - jump_up_anim_count - 1], (player.x, player.y-42))
            if not player.right_orient:
                screen.blit(jump_up_left[len(jump_up_left) - jump_up_anim_count - 1], (player.x, player.y-42))
            jump_up_anim_timer += 1
            if jump_up_anim_count == 16 and jump_up_anim_timer == 2:
                jump_up_anim_count = 0
                jump_up_anim_timer = 0
                player.is_jump_down = False
                player.is_busy = False
            elif jump_up_anim_timer == 2:
                jump_up_anim_count += 1
                jump_up_anim_timer = 0

        elif player.is_arm and not player.is_armed:
            player.is_busy = True
            if not player.is_sit:
                if player.right_orient:
                    screen.blit(arm_right[arm_anim_count], (player.x, player.y))
                if not player.right_orient:
                    screen.blit(arm_left[arm_anim_count], (player.x, player.y))
                arm_anim_timer += 1
                if arm_anim_count == 12 and arm_anim_timer == 1:
                    arm_anim_count = 0
                    arm_anim_timer = 0
                    player.is_arm = False
                    player.is_armed = True
                    player.is_busy = False
                elif arm_anim_timer == 1:
                    arm_anim_count += 1
                    arm_anim_timer = 0
            else:
                if player.right_orient:
                    screen.blit(sit_arm_right[arm_anim_count], (player.x+8, player.y))
                if not player.right_orient:
                    screen.blit(sit_arm_left[arm_anim_count], (player.x-8, player.y))
                arm_anim_timer += 1
                if arm_anim_count == 9 and arm_anim_timer == 1:
                    arm_anim_count = 0
                    arm_anim_timer = 0
                    player.is_arm = False
                    player.is_armed = True
                    player.is_busy = False
                elif arm_anim_timer == 1:
                    arm_anim_count += 1
                    arm_anim_timer = 0

        elif player.is_arm and player.is_armed:
            player.is_busy = True
            if not player.is_sit:
                if player.right_orient:
                    screen.blit(arm_right[len(arm_right) - arm_anim_count - 1], (player.x, player.y))
                if not player.right_orient:
                    screen.blit(arm_left[len(arm_right) - arm_anim_count - 1], (player.x, player.y))
                arm_anim_timer += 1
                if arm_anim_count == 12 and arm_anim_timer == 1:
                    arm_anim_count = 0
                    arm_anim_timer = 0
                    player.is_arm = False
                    player.is_armed = False
                    player.is_busy = False
                elif arm_anim_timer == 1:
                    arm_anim_count += 1
                    arm_anim_timer = 0
            else:
                if player.right_orient:
                    screen.blit(sit_arm_right[len(sit_arm_right) - arm_anim_count - 1], (player.x+8, player.y))
                if not player.right_orient:
                    screen.blit(sit_arm_left[len(sit_arm_left) - arm_anim_count - 1], (player.x-8, player.y))
                arm_anim_timer += 1
                if arm_anim_count == 9 and arm_anim_timer == 1:
                    arm_anim_count = 0
                    arm_anim_timer = 0
                    player.is_arm = False
                    player.is_armed = False
                    player.is_busy = False
                elif arm_anim_timer == 1:
                    arm_anim_count += 1
                    arm_anim_timer = 0

        elif player.is_armed and player.is_shoot:
            player.is_busy = True
            if shoot_anim_count == 2:
                blaster_sound.play()
            if player.is_sit:
                if player.right_orient:
                    screen.blit(sit_shoot_right[shoot_anim_count], (player.x + 12, player.y))
                if not player.right_orient:
                    screen.blit(sit_shoot_left[shoot_anim_count], (player.x - 10, player.y))
                shoot_anim_timer += 1
                if shoot_anim_count == 5 and shoot_anim_timer == 2:
                    shoot_anim_count = 0
                    shoot_anim_timer = 0
                    player.is_shoot = False
                    player.is_busy = False
                elif shoot_anim_timer == 2:
                    shoot_anim_count += 1
                    shoot_anim_timer = 0
            else:
                if player.right_orient:
                    screen.blit(shoot_right[shoot_anim_count], (player.x + 12, player.y))
                if not player.right_orient:
                    screen.blit(shoot_left[shoot_anim_count], (player.x - 10, player.y))
                shoot_anim_timer += 1
                if shoot_anim_count == 8 and shoot_anim_timer == 2:
                    shoot_anim_count = 0
                    shoot_anim_timer = 0
                    player.is_shoot = False
                    player.is_busy = False
                elif shoot_anim_timer == 2:
                    shoot_anim_count += 1
                    shoot_anim_timer = 0

        elif keys[pygame.K_UP] and not player.is_jump_up and not player.is_busy:
            if not player.is_sit and not player.is_armed:
                player.is_jump_up = True
                player.is_busy = True
            if player.is_sit:
                player.is_sit_up = True
                player.y -= 28
                player.is_sit = False
                player.is_busy = True
            else:
                screen.blit(hero, (player.x, player.y))

        elif keys[pygame.K_DOWN] and not player.is_busy:
            if not player.is_armed:
                if player.right_orient:
                    for ledge in ledges_left[player.bg_x][player.bg_y]:
                        if player.x + 21 > ledge.rect.left and player.x + 21 < ledge.rect.right and ledge.rect.top - player.y < 90 and ledge.rect.top - player.y > 35:
                            player.is_climb_down = True
                            player.is_busy = True
                if not player.right_orient:
                    for ledge in ledges_right[player.bg_x][player.bg_y]:
                        if player.x + 21 > ledge.rect.left and player.x + 21 < ledge.rect.right and ledge.rect.top - player.y < 90 and ledge.rect.top - player.y > 35:
                            player.is_climb_down = True
                            player.is_busy = True
            if not player.is_climb_down and not player.is_sit:
                player.is_sit_down = True
                player.is_busy = True
            else:
                screen.blit(hero, (player.x, player.y))

        elif keys[pygame.K_n] and not player.is_busy and not player.is_sit and not player.is_armed:
            player.is_busy = True
            player.is_jump = True

        elif keys[pygame.K_SPACE] and not player.is_busy and not player.is_armed:
            player.is_arm = True
            player.is_busy = True
            if not player.is_sit:
                if player.right_orient:
                    hero = player.armed_right
                if not player.right_orient:
                    hero = player.armed_left
            else:
                if player.right_orient:
                    hero = player.sit_armed_right
                if not player.right_orient:
                    hero = player.sit_armed_left

        elif keys[pygame.K_SPACE] and not player.is_busy and player.is_armed:
            player.is_arm = True
            player.is_busy = True
            if not player.is_sit:
                if player.right_orient:
                    hero = player.stay_right
                if not player.right_orient:
                    hero = player.stay_left
            else:
                if player.right_orient:
                    hero = player.sit_right
                if not player.right_orient:
                    hero = player.sit_left

        elif keys[pygame.K_b] and player.is_armed and not player.is_busy:
            if player.is_sit:
                if player.right_orient:
                    bullets_right.append(bullet.get_rect(topleft=(player.x + 30, player.y + 6)))
                else:
                    bullets_left.append(bullet.get_rect(topleft=(player.x, player.y + 6)))
            else:
                if player.right_orient:
                    bullets_right.append(bullet.get_rect(topleft=(player.x + 30, player.y + 14)))
                else:
                    bullets_left.append(bullet.get_rect(topleft=(player.x, player.y + 14)))
            player.is_shoot = True
            player.is_busy = True

        elif keys[pygame.K_LEFT] and not player.is_busy and not player.is_sit and not player.is_armed:
            screen.blit(walk_left[walk_anim_count], (player.x, player.y))
            player.right_orient = False
            player.x -= player.walk_speed
            walk_anim_timer += 1
            if walk_anim_count == 11 and walk_anim_timer == 3:
                walk_anim_count = 0
                walk_anim_timer = 0
            elif walk_anim_timer == 3:
                walk_anim_count += 1
                walk_anim_timer = 0

        elif keys[pygame.K_LEFT] and not player.is_busy and not player.is_sit and player.is_armed:
            screen.blit(walk_armed_left[walk_armed_anim_count], (player.x, player.y))
            player.right_orient = False
            player.x -= player.walk_armed_speed
            walk_armed_anim_timer += 1
            if walk_armed_anim_count == 14 and walk_armed_anim_timer == 2:
                walk_armed_anim_count = 0
                walk_armed_anim_timer = 0
            elif walk_armed_anim_timer == 2:
                walk_armed_anim_count += 1
                walk_armed_anim_timer = 0

        elif keys[pygame.K_LEFT] and not player.is_busy and player.is_sit and not player.is_sit_turn:
            if player.right_orient:
                player.is_busy = True
                player.is_sit_turn = True
            else:
                player.is_busy = True
                player.is_somersault = True

        elif keys[pygame.K_RIGHT] and not player.is_busy and player.is_sit and not player.is_sit_turn:
            if not player.right_orient:
                player.is_busy = True
                player.is_sit_turn = True
            else:
                player.is_busy = True
                player.is_somersault = True

        elif keys[pygame.K_RIGHT] and not player.is_busy and not player.is_sit and not player.is_armed:
            screen.blit(walk_right[walk_anim_count], (player.x, player.y))
            player.right_orient = True
            player.x += player.walk_speed
            walk_anim_timer += 1
            if walk_anim_count == 11 and walk_anim_timer == 3:
                walk_anim_count = 0
                walk_anim_timer = 0
            elif walk_anim_timer == 3:
                walk_anim_count += 1
                walk_anim_timer = 0

        elif keys[pygame.K_RIGHT] and not player.is_busy and not player.is_sit and player.is_armed:
            screen.blit(walk_armed_right[walk_armed_anim_count], (player.x, player.y))
            player.right_orient = True
            player.x += player.walk_armed_speed
            walk_armed_anim_timer += 1
            if walk_armed_anim_count == 14 and walk_armed_anim_timer == 2:
                walk_armed_anim_count = 0
                walk_armed_anim_timer = 0
            elif walk_armed_anim_timer == 2:
                walk_armed_anim_count += 1
                walk_armed_anim_timer = 0

        else:
            screen.blit(hero, (player.x, player.y))

        if keys[pygame.K_s] and not is_delay:
            is_delay = True
            send_save_thread = threading.Thread(target=send_save(player.nickname, player.x, player.y, player.hp, player.hp_max, player.damage, player.experience, player.level, player.bg_x, player.bg_y, scene_count))
            send_save_thread.start()

        if keys[pygame.K_l] and not is_delay:
            is_delay = True
            try:
                game_loaded, player.nickname, player.x, player.y, player.hp, player.hp_max, player.damage, player.experience, player.level, player.bg_x, player.bg_y, scene_count = request_save(player.nickname)
            except:
                pass

        if keys[pygame.K_m] and not is_delay:
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
                        player.hp += 50
                        if player.hp > player.hp_max:
                            player.hp = player.hp_max
                        sip_sound.play()
                        if border_x == 588 - (len(inventory_list)-1) * 20 and (len(inventory_list) > 1):
                            border_x += 20
                            border_pos -= 1
                        inventory_list.pop(i)
                    else:
                        if item.name == 'key':
                            for door in doors[player.bg_x][player.bg_y]:
                                if player.rect.colliderect(door.rect):
                                    if scene_count < 4:
                                        player.bg_x += 1
                                    scene = True
                                    scene_count += 1
                                    key_card_sound.play()
                                    player.x = 30
                                    if border_x == 588 - (len(inventory_list) - 1) * 20 and (len(inventory_list) > 1):
                                        border_x += 20
                                        border_pos -= 1
                                    inventory_list.pop(i)
                                    for i, archer in enumerate(archers_list_in_game):
                                        if archer.bg_x == player.bg_x - 1 and archer.bg_y == player.bg_y:
                                            archer.hp = archer.hp_max
                                            archers_list_in_game.pop(i)
                                    for i, soldier in enumerate(soldiers_list_in_game):
                                        if soldier.bg_x == player.bg_x - 1 and soldier.bg_y == player.bg_y:
                                            soldier.hp = soldier.hp_max
                                            soldiers_list_in_game.pop(i)
                                    for i, fly in enumerate(fly_list_in_game):
                                        if fly.bg_x == player.bg_x - 1 and fly.bg_y == player.bg_y:
                                            fly.hp = fly.hp_max
                                            fly.x = fly.x_0
                                            fly.y = fly.y_0
                                            fly_list_in_game.pop(i)
                                    for i, alien in enumerate(aliens_list_in_game):
                                        if alien.bg_x == player.bg_x - 1 and alien.bg_y == player.bg_y:
                                            alien.hp = alien.hp_max
                                            alien.x = alien.x_0
                                            alien.y = alien.y_0
                                            aliens_list_in_game.pop(i)
                                    for archer in archers_full_list:
                                        if archer.bg_x == player.bg_x and archer.bg_y == player.bg_y:
                                            if archer not in archers_list_in_game:
                                                archers_list_in_game.append(archer)
                                    for soldier in soldiers_full_list:
                                        if soldier.bg_x == player.bg_x and soldier.bg_y == player.bg_y:
                                            if soldier not in soldiers_list_in_game:
                                                soldiers_list_in_game.append(soldier)
                                    for fly in fly_full_list:
                                        if fly.bg_x == player.bg_x and fly.bg_y == player.bg_y:
                                            if fly not in fly_list_in_game:
                                                fly_list_in_game.append(fly)
                                    for alien in aliens_full_list:
                                        if alien.bg_x == player.bg_x and alien.bg_y == player.bg_y:
                                            if alien not in aliens_list_in_game:
                                                aliens_list_in_game.append(alien)

        if is_delay:
            delay_timer += 1
            if delay_timer == 10:
                is_delay = False
                delay_timer = 0

        if player.right_orient and player.is_sit and ((player.is_arm and not player.is_armed) or player.is_armed):
            hero = player.sit_armed_right
        if not player.right_orient and player.is_sit and ((player.is_arm and not player.is_armed) or player.is_armed):
            hero = player.sit_armed_left
        if player.right_orient and not player.is_armed and not player.is_sit:
            hero = player.stay_right
        if not player.right_orient and not player.is_armed and not player.is_sit:
            hero = player.stay_left
        if player.right_orient and player.is_armed and not player.is_sit:
            hero = player.armed_right
        if not player.right_orient and player.is_armed and not player.is_sit:
            hero = player.armed_left
        if player.right_orient and player.is_sit and not player.is_arm and not player.is_armed:
            hero = player.sit_right
        if not player.right_orient and player.is_sit and not player.is_arm and not player.is_armed:
            hero = player.sit_left

        if player.x > screen_width-1:
            player.bg_x += 1
            player.x = 10
            for i, archer in enumerate(archers_list_in_game):
                if archer.bg_x == player.bg_x - 1 and archer.bg_y == player.bg_y:
                    archer.hp = archer.hp_max
                    archers_list_in_game.pop(i)
            for i, soldier in enumerate(soldiers_list_in_game):
                if soldier.bg_x == player.bg_x - 1 and soldier.bg_y == player.bg_y:
                    soldier.hp = soldier.hp_max
                    soldiers_list_in_game.pop(i)
            for i, fly in enumerate(fly_list_in_game):
                if fly.bg_x == player.bg_x - 1 and fly.bg_y == player.bg_y:
                    fly.hp = fly.hp_max
                    fly_list_in_game.pop(i)
            for i, alien in enumerate(aliens_list_in_game):
                if alien.bg_x == player.bg_x - 1 and alien.bg_y == player.bg_y:
                    alien.hp = alien.hp_max
                    aliens_list_in_game.pop(i)
            for archer in archers_full_list:
                if archer.bg_x == player.bg_x and archer.bg_y == player.bg_y:
                    if archer not in archers_list_in_game:
                        archers_list_in_game.append(archer)
            for soldier in soldiers_full_list:
                if soldier.bg_x == player.bg_x and soldier.bg_y == player.bg_y:
                    if soldier not in soldiers_list_in_game:
                        soldiers_list_in_game.append(soldier)
            for fly in fly_full_list:
                if fly.bg_x == player.bg_x and fly.bg_y == player.bg_y:
                    if fly not in fly_list_in_game:
                        fly_list_in_game.append(fly)
            for alien in aliens_full_list:
                if alien.bg_x == player.bg_x and alien.bg_y == player.bg_y:
                    if alien not in aliens_list_in_game:
                        aliens_list_in_game.append(alien)
            arrows_right.clear()
            arrows_left.clear()
            bullets_right.clear()
            bullets_left.clear()
            pellets_right.clear()
            pellets_left.clear()

        if player.x < 0 and player.bg_x != 0:
            player.bg_x -= 1
            player.x = screen_width - 10
            for i, archer in enumerate(archers_list_in_game):
                if archer.bg_x == player.bg_x + 1 and archer.bg_y == player.bg_y:
                    archer.hp = archer.hp_max
                    archers_list_in_game.pop(i)
            for i, soldier in enumerate(soldiers_list_in_game):
                if soldier.bg_x == player.bg_x + 1 and soldier.bg_y == player.bg_y:
                    soldier.hp = soldier.hp_max
                    soldiers_list_in_game.pop(i)
            for i, fly in enumerate(fly_list_in_game):
                if fly.bg_x == player.bg_x + 1 and fly.bg_y == player.bg_y:
                    fly.hp = fly.hp_max
                    fly_list_in_game.pop(i)
            for i, alien in enumerate(aliens_list_in_game):
                if alien.bg_x == player.bg_x + 1 and alien.bg_y == player.bg_y:
                    alien.hp = alien.hp_max
                    aliens_list_in_game.pop(i)
            for archer in archers_full_list:
                if archer.bg_x == player.bg_x and archer.bg_y == player.bg_y:
                    if archer not in archers_list_in_game:
                        archers_list_in_game.append(archer)
            for soldier in soldiers_full_list:
                if soldier.bg_x == player.bg_x and soldier.bg_y == player.bg_y:
                    if soldier not in soldiers_list_in_game:
                        soldiers_list_in_game.append(soldier)
            for fly in fly_full_list:
                if fly.bg_x == player.bg_x and fly.bg_y == player.bg_y:
                    if fly not in fly_list_in_game:
                        fly_list_in_game.append(fly)
            for alien in aliens_full_list:
                if alien.bg_x == player.bg_x and alien.bg_y == player.bg_y:
                    if alien not in aliens_list_in_game:
                        aliens_list_in_game.append(alien)
            arrows_right.clear()
            arrows_left.clear()
            bullets_right.clear()
            bullets_left.clear()
            pellets_right.clear()
            pellets_left.clear()

        if player.y > screen_height:
            player.bg_y += 1
            player.y = player.y - screen_height
            for i, archer in enumerate(archers_list_in_game):
                if archer.bg_x == player.bg_x and archer.bg_y == player.bg_y - 1:
                    archer.hp = archer.hp_max
                    archers_list_in_game.pop(i)
            for i, soldier in enumerate(soldiers_list_in_game):
                if soldier.bg_x == player.bg_x and soldier.bg_y == player.bg_y - 1:
                    soldier.hp = soldier.hp_max
                    soldiers_list_in_game.pop(i)
            for i, fly in enumerate(fly_list_in_game):
                if fly.bg_x == player.bg_x and fly.bg_y == player.bg_y - 1:
                    fly.hp = fly.hp_max
                    fly_list_in_game.pop(i)
            for i, alien in enumerate(aliens_list_in_game):
                if alien.bg_x == player.bg_x and alien.bg_y == player.bg_y - 1:
                    alien.hp = alien.hp_max
                    aliens_list_in_game.pop(i)
            for archer in archers_full_list:
                if archer.bg_x == player.bg_x and archer.bg_y == player.bg_y:
                    if archer not in archers_list_in_game:
                        archers_list_in_game.append(archer)
            for soldier in soldiers_full_list:
                if soldier.bg_x == player.bg_x and soldier.bg_y == player.bg_y:
                    if soldier not in soldiers_list_in_game:
                        soldiers_list_in_game.append(soldier)
            for fly in fly_full_list:
                if fly.bg_x == player.bg_x and fly.bg_y == player.bg_y:
                    if fly not in fly_list_in_game:
                        fly_list_in_game.append(fly)
            for alien in aliens_full_list:
                if alien.bg_x == player.bg_x and alien.bg_y == player.bg_y:
                    if alien not in aliens_list_in_game:
                        aliens_list_in_game.append(alien)
            arrows_right.clear()
            arrows_left.clear()
            bullets_right.clear()
            bullets_left.clear()
            pellets_right.clear()
            pellets_left.clear()

        if player.y < 0 and player.bg_y != 0:
            player.bg_y -= 1
            player.y = player.y + screen_height
            for i, archer in enumerate(archers_list_in_game):
                if archer.bg_x == player.bg_x and archer.bg_y == player.bg_y + 1:
                    archer.hp = archer.hp_max
                    archers_list_in_game.pop(i)
            for i, soldier in enumerate(soldiers_list_in_game):
                if soldier.bg_x == player.bg_x and soldier.bg_y == player.bg_y + 1:
                    soldier.hp = soldier.hp_max
                    soldiers_list_in_game.pop(i)
            for i, fly in enumerate(fly_list_in_game):
                if fly.bg_x == player.bg_x and fly.bg_y == player.bg_y + 1:
                    fly.hp = fly.hp_max
                    fly_list_in_game.pop(i)
            for i, alien in enumerate(aliens_list_in_game):
                if alien.bg_x == player.bg_x and alien.bg_y == player.bg_y + 1:
                    alien.hp = alien.hp_max
                    aliens_list_in_game.pop(i)
            for archer in archers_full_list:
                if archer.bg_x == player.bg_x and archer.bg_y == player.bg_y:
                    if archer not in archers_list_in_game:
                        archers_list_in_game.append(archer)
            for soldier in soldiers_full_list:
                if soldier.bg_x == player.bg_x and soldier.bg_y == player.bg_y:
                    if soldier not in soldiers_list_in_game:
                        soldiers_list_in_game.append(soldier)
            for fly in fly_full_list:
                if fly.bg_x == player.bg_x and fly.bg_y == player.bg_y:
                    if fly not in fly_list_in_game:
                        fly_list_in_game.append(fly)
            for alien in aliens_full_list:
                if alien.bg_x == player.bg_x and alien.bg_y == player.bg_y:
                    if alien not in aliens_list_in_game:
                        aliens_list_in_game.append(alien)
            arrows_right.clear()
            arrows_left.clear()
            bullets_right.clear()
            bullets_left.clear()
            pellets_right.clear()
            pellets_left.clear()

        if bullets_right:
            for (i, el) in enumerate(bullets_right):
                screen.blit(bullet, (el.x, el.y))
                el.x += 15

                for wall in walls[player.bg_x][player.bg_y]:
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

                if archers_list_in_game:
                    for (index, archer) in enumerate(archers_list_in_game):
                        if archer.alive and el.colliderect(archer.archer_stay_left.get_rect(topleft=(archer.x, archer.y))):
                            archer.decrease_hp(player.damage)
                            if archer.hp <= 0:
                                archer.hp = archer.hp_max
                                player.experience += archer.exp
                                archer.alive = False
                            try:
                                bullets_right.pop(i)
                            except:
                                pass

                if soldiers_list_in_game:
                    for (index, soldier) in enumerate(soldiers_list_in_game):
                        if soldier.alive and el.colliderect(soldier.soldier_stay_left.get_rect(topleft=(soldier.x, soldier.y))):
                            soldier.decrease_hp(player.damage)
                            if soldier.hp <= 0:
                                soldier.hp = soldier.hp_max
                                player.experience += soldier.exp
                                soldier.alive = False
                            try:
                                bullets_right.pop(i)
                            except:
                                pass

                if fly_list_in_game:
                    for (index, fly) in enumerate(fly_list_in_game):
                        if fly.alive and el.colliderect(fly.fly_stay_left.get_rect(topleft=(fly.x, fly.y))):
                            fly.decrease_hp(player.damage)
                            if fly.hp <= 0:
                                fly.hp = fly.hp_max
                                player.experience += fly.exp
                                fly.alive = False
                            try:
                                bullets_right.pop(i)
                            except:
                                pass

                if aliens_list_in_game:
                    for (index, alien) in enumerate(aliens_list_in_game):
                        if alien.alive and el.colliderect(alien.alien_stay_left.get_rect(topleft=(alien.x, alien.y))):
                            alien.decrease_hp(player.damage)
                            if alien.hp <= 0:
                                alien.hp = alien.hp_max
                                player.experience += alien.exp
                                alien.alive = False
                            try:
                                bullets_right.pop(i)
                            except:
                                pass

        if arrows_right:
            for (i, el) in enumerate(arrows_right):
                screen.blit(arrow, (el.x, el.y))
                el.x += 15

                for wall in walls[player.bg_x][player.bg_y]:
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

                if el.colliderect(player.rect):
                    player.hp -= archer_1.damage
                    try:
                        arrows_right.pop(i)
                    except:
                        pass

        if pellets_right:
            for (i, el) in enumerate(pellets_right):
                screen.blit(pellet, (el.x, el.y))
                el.x += 15

                for wall in walls[player.bg_x][player.bg_y]:
                    if el.colliderect(wall.rect):
                        try:
                            pellets_right.pop(i)
                        except:
                            pass
                if el.x < 0 or el.x > screen_width:
                    try:
                        pellets_right.pop(i)
                    except:
                        pass

                if el.colliderect(player.rect):
                    player.hp -= soldier_1.damage
                    try:
                        pellets_right.pop(i)
                    except:
                        pass

        if bullets_left:
            for (i, el) in enumerate(bullets_left):
                screen.blit(bullet, (el.x, el.y))
                el.x -= 15

                for wall in walls[player.bg_x][player.bg_y]:
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

                if archers_list_in_game:
                    for (index, archer) in enumerate(archers_list_in_game):
                        if archer.alive and el.colliderect(archer.archer_stay_left.get_rect(topleft=(archer.x, archer.y))):
                            archer.decrease_hp(player.damage)
                            if archer.hp <= 0:
                                archer.hp = archer.hp_max
                                player.experience += archer.exp
                                archer.alive = False
                            try:
                                bullets_left.pop(i)
                            except:
                                pass

                if soldiers_list_in_game:
                    for (index, soldier) in enumerate(soldiers_list_in_game):
                        if soldier.alive and el.colliderect(soldier.soldier_stay_left.get_rect(topleft=(soldier.x, soldier.y))):
                            soldier.decrease_hp(player.damage)
                            if soldier.hp <= 0:
                                soldier.hp = soldier.hp_max
                                player.experience += soldier.exp
                                soldier.alive = False
                            try:
                                bullets_left.pop(i)
                            except:
                                pass

                if fly_list_in_game:
                    for (index, fly) in enumerate(fly_list_in_game):
                        if fly.alive and el.colliderect(fly.fly_stay_right.get_rect(topleft=(fly.x, fly.y))):
                            fly.decrease_hp(player.damage)
                            if fly.hp <= 0:
                                fly.hp = fly.hp_max
                                player.experience += fly.exp
                                fly.alive = False
                            try:
                                bullets_left.pop(i)
                            except:
                                pass

                if aliens_list_in_game:
                    for (index, alien) in enumerate(aliens_list_in_game):
                        if alien.alive and el.colliderect(alien.alien_stay_right.get_rect(topleft=(alien.x, alien.y))):
                            alien.decrease_hp(player.damage)
                            if alien.hp <= 0:
                                alien.hp = alien.hp_max
                                player.experience += alien.exp
                                alien.alive = False
                            try:
                                bullets_left.pop(i)
                            except:
                                pass

        if arrows_left:
            for (i, el) in enumerate(arrows_left):
                screen.blit(arrow, (el.x, el.y))
                el.x -= 15

                for wall in walls[player.bg_x][player.bg_y]:
                    if el.colliderect(wall.rect):
                        try:
                            arrows_left.pop(i)
                        except:
                            pass
                if el.x < 0 or el.x > screen_width:
                    try:
                        arrows_left.pop(i)
                    except:
                        pass

                if el.colliderect(player.rect):
                    player.hp -= archer_1.damage
                    try:
                        arrows_left.pop(i)
                    except:
                        pass

        if pellets_left:
            for (i, el) in enumerate(pellets_left):
                screen.blit(pellet, (el.x, el.y))
                el.x -= 15

                for wall in walls[player.bg_x][player.bg_y]:
                    if el.colliderect(wall.rect):
                        try:
                            pellets_left.pop(i)
                        except:
                            pass
                if el.x < 0 or el.x > screen_width:
                    try:
                        pellets_left.pop(i)
                    except:
                        pass

                if el.colliderect(player.rect):
                    player.hp -= soldier_1.damage
                    try:
                        pellets_left.pop(i)
                    except:
                        pass

    else:
        if scene_count == 5:
            running = False
            pygame.quit()
        else:
            screen.fill((95, 165, 179))
            screen.blit(lose_label, (260, 20))
            screen.blit(restart_label, restart_label_rect)

            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameplay = True
                player.x = 50
                player.y = 142
                player.bg_x = 0
                player.bg_y = 0
                hp = 100
                player.hp_max = 100
                player.level = 1
                player.experience = 0
                scene_count = 1
                archers_list_in_game = [archer_1]
                fly_list_in_game = [fly_1]
                soldiers_list_in_game = []
                aliens_list_in_game = []
                bullets_right.clear()
                bullets_left.clear()
                arrows_right.clear()
                arrows_left.clear()
                pellets_right.clear()
                pellets_left.clear()
                inventory_list = []
                items_list = items_list_start[:]

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(30)
    # elif event.type == pygame.KEYDOWN:
    #     if event.key == pygame.K_a:
    #         screen.fill((132, 3, 252))