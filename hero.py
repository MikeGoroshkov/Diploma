import pygame

spritesheet = pygame.image.load('images/flash_new.png')

player_stay_right = spritesheet.subsurface(pygame.Rect((0,6), (43, 78)))
player_stay_left = pygame.transform.flip(spritesheet.subsurface(pygame.Rect((0,6), (43, 78))), True, False)
player_armed_right = spritesheet.subsurface(pygame.Rect((10,3802), (43, 78)))
player_armed_left = pygame.transform.flip(spritesheet.subsurface(pygame.Rect((10,3802), (43, 78))), True, False)
player_sit_right = spritesheet.subsurface(pygame.Rect((274,1189), (43, 50)))
player_sit_left = pygame.transform.flip(spritesheet.subsurface(pygame.Rect((274,1189), (43, 50))), True, False)
player_sit_armed_right = spritesheet.subsurface(pygame.Rect((10, 4618), (50, 50)))
player_sit_armed_left = pygame.transform.flip(spritesheet.subsurface(pygame.Rect((10, 4618), (50, 50))), True, False)

bullet = pygame.image.load('images/bullet.png')
bullets_right = []
bullets_left = []

walk_speed = 3
walk_armed_speed = 2
player_x = 200
player_y = 22
hp = 3

player_anim_count = 0
player_anim_timer = 0
walk_anim_count = 0
walk_anim_timer = 0
walk_armed_anim_count = 0
walk_armed_anim_timer = 0
jump_anim_count = 0
jump_anim_timer = 0
jump_up_anim_count = 0
jump_up_anim_timer = 0
shoot_anim_count = 0
shoot_anim_timer = 0
arm_anim_count = 0
arm_anim_timer = 0
falling_anim_count = 0
falling_anim_timer = 0
wound_anim_count = 0
wound_anim_timer = 0
falling_high = 0
getup_anim_count = 0
getup_anim_timer = 0
climb_anim_count = 0
climb_anim_timer = 0
climb_down_anim_count = 0
climb_down_anim_timer = 0
sit_down_anim_count = 0
sit_down_anim_timer = 0
somersault_anim_count = 0
somersault_anim_timer = 0
sit_turn_anim_count = 0
sit_turn_anim_timer = 0
is_fall = True
is_jump = False
is_jump_up = False
is_jump_down = False
is_busy = False
is_arm = False
is_armed = False
is_shoot = False
on_platform = False
is_climb = False
is_climb_down = False
is_wounded = False
is_getup = False
is_sit_down = False
is_sit_up = False
is_sit = False
is_somersault = False
is_sit_turn = False
player = player_stay_right
right_orient = True

walk_armed_frame_width = 43
walk_armed_frame_height = 78
walk_armed_frame_count = 15
walk_armed_pos = [(10 + i * (walk_armed_frame_width+1), 3802) for i in range(walk_armed_frame_count)]
walk_armed_right = [spritesheet.subsurface(pygame.Rect(pos, (walk_armed_frame_width, walk_armed_frame_height))) for pos in walk_armed_pos]
walk_armed_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (walk_armed_frame_width, walk_armed_frame_height))), True, False) for pos in walk_armed_pos]

climb_frame_width = 42
climb_frame_height = 78 + 120
climb_frame_count = 25
climb_pos = [(1066 - i * (climb_frame_width+2), 2803) for i in range(climb_frame_count)]
climb_right = [spritesheet.subsurface(pygame.Rect(pos, (climb_frame_width, climb_frame_height))) for pos in climb_pos]
climb_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (climb_frame_width, climb_frame_height))), True, False) for pos in climb_pos]

climb_down_frame_width = 42
climb_down_frame_height = 78 + 120
climb_down_frame_count = 25
climb_down_pos = [(10 + i * (climb_down_frame_width+2), 2803) for i in range(climb_down_frame_count)]
climb_down_right = [spritesheet.subsurface(pygame.Rect(pos, (climb_down_frame_width, climb_down_frame_height))) for pos in climb_down_pos]
climb_down_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (climb_down_frame_width, climb_down_frame_height))), True, False) for pos in climb_down_pos]

getup_frame_width = 54
getup_frame_height = 78
getup_frame_count = 19
getup_pos = [(10 + 54 * 8 + i * (getup_frame_width+1), 1782) for i in range(getup_frame_count)]
getup_right = [spritesheet.subsurface(pygame.Rect(pos, (getup_frame_width, getup_frame_height))) for pos in getup_pos]
getup_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (getup_frame_width, getup_frame_height))), True, False) for pos in getup_pos]

wound_frame_width = 54
wound_frame_height = 78
wound_frame_count = 27
wound_pos = [(10 + i * (wound_frame_width + 1), 1782) for i in range(wound_frame_count)]
wound_right = [spritesheet.subsurface(pygame.Rect(pos, (wound_frame_width, wound_frame_height))) for pos in wound_pos]
wound_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (wound_frame_width, wound_frame_height))), True, False) for pos in wound_pos]

falling_frame_width = 66
falling_frame_height = 90
falling_frame_count = 8
falling_pos = [(10 + i * (falling_frame_width + 1), 967) for i in range(falling_frame_count)]
falling_right = [spritesheet.subsurface(pygame.Rect(pos, (falling_frame_width, falling_frame_height))) for pos in falling_pos]
falling_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (falling_frame_width, falling_frame_height))), True, False) for pos in falling_pos]

sit_down_frame_width = 43
sit_down_frame_height = 78
sit_down_frame_count = 7
sit_down_pos = [(10 + i * (sit_down_frame_width + 1), 1161) for i in range(sit_down_frame_count)]
sit_down_right = [spritesheet.subsurface(pygame.Rect(pos, (sit_down_frame_width, sit_down_frame_height))) for pos in sit_down_pos]
sit_down_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (sit_down_frame_width, sit_down_frame_height))), True, False) for pos in sit_down_pos]

arm_frame_width = 43
arm_frame_height = 78
arm_frame_count = 13
arm_pos = [(10 + i * (arm_frame_width + 1), 4108) for i in range(arm_frame_count)]
arm_right = [spritesheet.subsurface(pygame.Rect(pos, (arm_frame_width, arm_frame_height))) for pos in arm_pos]
arm_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (arm_frame_width, arm_frame_height))), True, False) for pos in arm_pos]

sit_arm_frame_width = 43
sit_arm_frame_height = 50
sit_arm_frame_count = 10
sit_arm_pos = [(10 + i * (sit_arm_frame_width + 1), 4692) for i in range(sit_arm_frame_count)]
sit_arm_right = [spritesheet.subsurface(pygame.Rect(pos, (sit_arm_frame_width, sit_arm_frame_height))) for pos in sit_arm_pos]
sit_arm_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (sit_arm_frame_width, sit_arm_frame_height))), True, False) for pos in sit_arm_pos]

shoot_frame_width = 43
shoot_frame_height = 78
shoot_frame_count = 9
shoot_pos = [(10 + i * (shoot_frame_width + 1), 3712) for i in range(shoot_frame_count)]
shoot_right = [spritesheet.subsurface(pygame.Rect(pos, (shoot_frame_width, shoot_frame_height))) for pos in shoot_pos]
shoot_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (shoot_frame_width, shoot_frame_height))), True, False) for pos in shoot_pos]

sit_shoot_frame_width = 44
sit_shoot_frame_height = 48
sit_shoot_frame_count = 6
sit_shoot_pos = [(10 + i * (sit_shoot_frame_width), 4547) for i in range(sit_shoot_frame_count)]
sit_shoot_right = [spritesheet.subsurface(pygame.Rect(pos, (sit_shoot_frame_width, sit_shoot_frame_height))) for pos in sit_shoot_pos]
sit_shoot_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (sit_shoot_frame_width, sit_shoot_frame_height))), True, False) for pos in sit_shoot_pos]

somersault_frame_width = 44
somersault_frame_height = 46
somersault_frame_count = 9
somersault_pos = [(10 + i * (somersault_frame_width), 4398) for i in range(somersault_frame_count)]
somersault_right = [spritesheet.subsurface(pygame.Rect(pos, (somersault_frame_width, somersault_frame_height))) for pos in somersault_pos]
somersault_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (somersault_frame_width, somersault_frame_height))), True, False) for pos in somersault_pos]

sit_turn_frame_width = 44
sit_turn_frame_height = 46
sit_turn_frame_count = 9
sit_turn_pos = [(10 + i * (sit_turn_frame_width), 2322) for i in range(sit_turn_frame_count)]
sit_turn_right = [spritesheet.subsurface(pygame.Rect(pos, (sit_turn_frame_width, sit_turn_frame_height))) for pos in sit_turn_pos]
sit_turn_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (sit_turn_frame_width, sit_turn_frame_height))), True, False) for pos in sit_turn_pos]

walk_frame_width = 43
walk_frame_height = 78
walk_frame_count = 12
walk_pos = [(10 + i * (walk_frame_width + 1), 98) for i in range(walk_frame_count)]
walk_right = [spritesheet.subsurface(pygame.Rect(pos, (walk_frame_width, walk_frame_height))) for pos in walk_pos]
walk_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (walk_frame_width, walk_frame_height))), True, False) for pos in walk_pos]

jump_frame_width = 58
jump_frame_height = 78
jump_frame_count = 19
jump_pos = [(10 + i * (jump_frame_width + 1), 188) for i in range(jump_frame_count)]
jump_right = [spritesheet.subsurface(pygame.Rect(pos, (jump_frame_width, jump_frame_height))) for pos in jump_pos]
jump_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (jump_frame_width, jump_frame_height))), True, False) for pos in jump_pos]

jump_up_frame_width = 43
jump_up_frame_height = 120
jump_up_frame_count = 17
jump_up_pos = [(10 + i * (jump_up_frame_width + 1), 1241) for i in range(jump_up_frame_count)]
jump_up_right = [spritesheet.subsurface(pygame.Rect(pos, (jump_up_frame_width, jump_up_frame_height))) for pos in jump_up_pos]
jump_up_left = [pygame.transform.flip(spritesheet.subsurface(pygame.Rect(pos, (jump_up_frame_width, jump_up_frame_height))), True, False) for pos in jump_up_pos]
