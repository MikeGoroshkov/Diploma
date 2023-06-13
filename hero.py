import pygame

spritesheet = pygame.image.load('images/flash_new.png')
frame_width = 20
frame_height = 48
# frame_count = 4
# frame_pos = [(i * frame_width, 0) for i in range(frame_count)]

# x, y, w, h
frame_pos = [(1,1,16,46), (12,49,16,46), (32,49,16,46), (59,49,20,46), (87,49,20,46), (114,49,20,46), (12,49,20,46)]

frames = [spritesheet.subsurface(pygame.Rect((pos[0], pos[1]), (pos[2], pos[3]))) for pos in frame_pos]

player = frames[0]
#spritesheet
walk_left = [pygame.transform.flip(frames[i], True, False) for i in range(0,7)]
walk_right = [frames[i] for i in range(0,7)]