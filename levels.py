import pygame

pygame.init()

screen_width = 630
screen_height = 360
screen = pygame.display.set_mode((screen_width, screen_height)) #, flags=pygame.NOFRAME
pygame.display.set_caption("Escape from Zefira")
icon = pygame.image.load('images/icon.png') # https://www.iconfinder.com/
pygame.display.set_icon(icon)

start_bg = pygame.image.load('images/start_screen.png').convert_alpha()
bg_1 = pygame.image.load(f'images/back_1.png').convert_alpha()
bg_2 = pygame.image.load(f'images/back_2.png').convert_alpha()
bg_3 = pygame.image.load(f'images/back_3.png').convert_alpha()
bg_4 = pygame.image.load(f'images/back_4.png').convert_alpha()
bg_5 = pygame.image.load(f'images/back_5.png').convert_alpha()
bg_6 = pygame.image.load(f'images/back_6.png').convert_alpha()
bg_7 = pygame.image.load(f'images/back_7.png').convert_alpha()
bg_8 = pygame.image.load(f'images/back_8.png').convert_alpha()
bg = [[bg_1, bg_2, bg_3, bg_4, bg_5, bg_6, bg_7, bg_8], [bg_1, bg_2, bg_3, bg_4, bg_5, bg_6, bg_7, bg_8]]
bg_x = 0
bg_y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)  # Зеленый цвет платформы (можете изменить на свой)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height


tile_1 = pygame.image.load('images/tile_0000.png').convert_alpha()
tile_2 = pygame.image.load('images/tile_0018.png').convert_alpha()
tile_3 = pygame.image.load('images/tile_0001.png').convert_alpha()
tile_door = pygame.image.load('images/door.png').convert_alpha()
spaceship = pygame.image.load('images/spaceship.png').convert_alpha()

platforms = [[pygame.sprite.Group() for j in range(2)] for i in range(8)]

platforms[0][0].add(Platform(120, 340, 510, 20, 'red'))
platforms[0][0].add(Platform(0, 220, 210, 20, 'red'))
platforms[0][0].add(Platform(120, 100, 300, 20, 'red'))
platforms[0][0].add(Platform(540, 100, 90, 20, 'red'))

platforms[1][0].add(Platform(0, 340, 630, 20, 'red'))
platforms[1][0].add(Platform(0, 220, 210, 20, 'red'))
platforms[1][0].add(Platform(0, 100, 420, 20, 'red'))
platforms[1][0].add(Platform(540, 100, 90, 20, 'red'))

platforms[0][1].add(Platform(0, 340, 630, 20, 'red'))
platforms[0][1].add(Platform(0, 100, 270, 20, 'red'))
platforms[0][1].add(Platform(240, 220, 390, 20, 'red'))

platforms[1][1].add(Platform(0, 340, 630, 20, 'red'))
platforms[1][1].add(Platform(0, 100, 270, 20, 'red'))
platforms[1][1].add(Platform(240, 220, 390, 20, 'red'))

platforms[2][1].add(Platform(0, 340, 630, 20, 'red'))
platforms[2][1].add(Platform(0, 100, 180, 20, 'red'))
platforms[2][1].add(Platform(330, 100, 360, 20, 'red'))
platforms[2][1].add(Platform(270, 220, 390, 20, 'red'))

platforms[2][0].add(Platform(120, 340, 510, 20, 'red'))
platforms[2][0].add(Platform(420, 220, 210, 20, 'red'))
platforms[2][0].add(Platform(0, 220, 270, 20, 'red'))
platforms[2][0].add(Platform(180, 100, 270, 20, 'red'))

platforms[3][0].add(Platform(0, 220, 210, 20, 'red'))
platforms[3][0].add(Platform(90, 100, 270, 20, 'red'))
platforms[3][0].add(Platform(480, 100, 150, 20, 'red'))
platforms[3][0].add(Platform(330, 220, 300, 20, 'red'))
platforms[3][0].add(Platform(0, 340, 510, 20, 'red'))

platforms[3][1].add(Platform(0, 340, 630, 20, 'red'))
platforms[3][1].add(Platform(0, 100, 150, 20, 'red'))
platforms[3][1].add(Platform(330, 100, 300, 20, 'red'))
platforms[3][1].add(Platform(210, 220, 150, 20, 'red'))
platforms[3][1].add(Platform(510, 220, 120, 20, 'red'))

platforms[4][0].add(Platform(120, 340, 510, 20, 'red'))
platforms[4][0].add(Platform(0, 100, 630, 20, 'red'))

platforms[4][1].add(Platform(0, 340, 630, 20, 'red'))
platforms[4][1].add(Platform(0, 220, 210, 20, 'red'))
platforms[4][1].add(Platform(480, 220, 150, 20, 'red'))
platforms[4][1].add(Platform(0, 100, 270, 20, 'red'))
platforms[4][1].add(Platform(390, 100, 240, 20, 'red'))

platforms[5][0].add(Platform(0, 340, 630, 20, 'red'))
platforms[5][0].add(Platform(120, 220, 420, 20, 'red'))
platforms[5][0].add(Platform(0, 100, 150, 20, 'red'))
platforms[5][0].add(Platform(330, 100, 150, 20, 'red'))

platforms[5][1].add(Platform(0, 340, 630, 20, 'red'))
platforms[5][1].add(Platform(0, 220, 210, 20, 'red'))
platforms[5][1].add(Platform(480, 220, 150, 20, 'red'))
platforms[5][1].add(Platform(0, 100, 510, 20, 'red'))

platforms[6][0].add(Platform(120, 340, 510, 20, 'red'))
platforms[6][0].add(Platform(0, 220, 210, 20, 'red'))
platforms[6][0].add(Platform(300, 220, 150, 20, 'red'))
platforms[6][0].add(Platform(150, 100, 180, 20, 'red'))
platforms[6][0].add(Platform(510, 100, 120, 20, 'red'))

platforms[6][1].add(Platform(0, 340, 630, 20, 'red'))
platforms[6][1].add(Platform(0, 220, 240, 20, 'red'))
platforms[6][1].add(Platform(330, 220, 300, 20, 'red'))
platforms[6][1].add(Platform(0, 100, 180, 20, 'red'))
platforms[6][1].add(Platform(450, 100, 180, 20, 'red'))

platforms[7][0].add(Platform(0, 340, 240, 20, 'red'))
platforms[7][0].add(Platform(360, 340, 270, 20, 'red'))
platforms[7][0].add(Platform(330, 220, 180, 20, 'red'))
platforms[7][0].add(Platform(0, 100, 360, 20, 'red'))

platforms[7][1].add(Platform(0, 340, 630, 20, 'red'))
platforms[7][1].add(Platform(0, 220, 240, 20, 'red'))
platforms[7][1].add(Platform(0, 100, 90, 20, 'red'))
platforms[7][1].add(Platform(210, 100, 180, 20, 'red'))

walls = [[pygame.sprite.Group() for j in range(2)] for i in range(8)]

walls[0][0].add(Platform(-1, 0, 20, 360, 'blue'))

walls[1][0].add(Platform(611, 0, 20, 360, 'blue'))

walls[0][1].add(Platform(-1, 0, 20, 360, 'blue'))
walls[0][1].add(Platform(611, 0, 20, 240, 'blue'))

walls[1][1].add(Platform(611, 0, 20, 360, 'blue'))
walls[1][1].add(Platform(-1, 0, 20, 120, 'blue'))

walls[2][1].add(Platform(-1, 0, 20, 360, 'blue'))
walls[2][1].add(Platform(611, 120, 20, 240, 'blue'))

walls[2][0].add(Platform(-1, 0, 20, 360, 'blue'))
walls[2][0].add(Platform(611, 0, 20, 120, 'blue'))
walls[2][0].add(Platform(611, 240, 20, 140, 'blue'))
walls[2][0].add(Platform(390, 120, 20, 120, 'blue'))

walls[3][0].add(Platform(-1, 240, 20, 140, 'blue'))
walls[3][0].add(Platform(611, 0, 20, 360, 'blue'))

walls[3][0].add(Platform(-1, 240, 20, 120, 'blue'))
walls[3][0].add(Platform(120, 120, 20, 120, 'blue'))
walls[3][0].add(Platform(611, 0, 20, 360, 'blue'))

walls[3][1].add(Platform(150, 0, 20, 120, 'blue'))
walls[3][1].add(Platform(-1, 120, 20, 240, 'blue'))
walls[3][1].add(Platform(360, 120, 20, 120, 'blue'))
walls[3][1].add(Platform(611, 0, 20, 360, 'blue'))

walls[4][0].add(Platform(-1, 0, 20, 360, 'blue'))

walls[4][1].add(Platform(-1, 0, 20, 360, 'blue'))
walls[4][1].add(Platform(611, 120, 20, 120, 'blue'))

walls[5][0].add(Platform(100, 120, 20, 120, 'blue'))
walls[5][0].add(Platform(360, 120, 20, 120, 'blue'))
walls[5][0].add(Platform(611, 0, 20, 360, 'blue'))

walls[5][1].add(Platform(-1, 120, 20, 120, 'blue'))
walls[5][1].add(Platform(611, 0, 20, 360, 'blue'))

walls[6][0].add(Platform(-1, 0, 20, 360, 'blue'))
walls[6][0].add(Platform(300, 120, 20, 240, 'blue'))

walls[6][1].add(Platform(-1, 0, 20, 360, 'blue'))
walls[6][1].add(Platform(310, 0, 20, 240, 'blue'))
walls[6][1].add(Platform(611, 120, 20, 240, 'blue'))

walls[7][0].add(Platform(310, 120, 20, 120, 'blue'))
walls[7][0].add(Platform(611, 0, 20, 360, 'blue'))

walls[7][1].add(Platform(-1, 120, 20, 240, 'blue'))
walls[7][1].add(Platform(390, 0, 20, 120, 'blue'))
walls[7][1].add(Platform(611, 0, 20, 360, 'blue'))

ledges_right = [[pygame.sprite.Group() for j in range(2)] for i in range(8)]
ledges_left = [[pygame.sprite.Group() for j in range(2)] for i in range(8)]
for i in range(8):
    for j in range(2):
        for platform in platforms[i][j]:
            if platform.rect.x != 0:
                ledges_left[i][j].add(Platform(platform.rect.x-30, platform.rect.y, 30, 20, 'green'))
            if platform.rect.x + platform.width <= 580:
                ledges_right[i][j].add(Platform(platform.rect.x + platform.width, platform.rect.y, 30, 20, 'green'))
        try:
            for platform in platforms[i][j-1]:
                if platform.rect.x != 0 and platform.rect.y == 340:
                    ledges_left[i][j].add(Platform(platform.rect.x-30, -20, 30, 20, 'green'))
                if platform.rect.x + platform.width <= 580 and platform.rect.y == 340:
                    ledges_right[i][j].add(Platform(platform.rect.x + platform.width, -20, 30, 20, 'green'))
        except:
            pass


doors = [[pygame.sprite.Group() for j in range(2)] for i in range(8)]

doors[1][1].add(Platform(565, 240, 50, 100, 'green'))
doors[3][1].add(Platform(565, 120, 50, 100, 'green'))
doors[5][1].add(Platform(565, 240, 50, 100, 'green'))
doors[7][1].add(Platform(450, 110, 125, 227, 'green'))

