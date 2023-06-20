import pygame

pygame.init()

screen_width = 630
screen_height = 360
screen = pygame.display.set_mode((screen_width, screen_height)) #, flags=pygame.NOFRAME
pygame.display.set_caption("Escape from Zefira")
icon = pygame.image.load('images/icon.png') # https://www.iconfinder.com/
pygame.display.set_icon(icon)

start_bg = pygame.image.load('images/start_screen.png').convert_alpha()
bg = [[pygame.image.load(f'images/back_{i}_{j}.png').convert_alpha() for i in range(1,3)] for j in range(1,3)]
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
platforms_1_1 = pygame.sprite.Group()
platforms_1_1.add(Platform(120, 340, 510, 20, 'red'))
platforms_1_1.add(Platform(0, 220, 210, 20, 'red'))
platforms_1_1.add(Platform(120, 100, 300, 20, 'red'))
platforms_1_1.add(Platform(540, 100, 90, 20, 'red'))
platforms_2_1 = pygame.sprite.Group()
platforms_2_1.add(Platform(0, 340, 630, 20, 'red'))
platforms_2_1.add(Platform(0, 220, 210, 20, 'red'))
platforms_2_1.add(Platform(0, 100, 420, 20, 'red'))
platforms_2_1.add(Platform(540, 100, 90, 20, 'red'))
platforms_1_2 = pygame.sprite.Group()
platforms_1_2.add(Platform(0, 340, 630, 20, 'red'))
platforms_1_2.add(Platform(0, 100, 270, 20, 'red'))
platforms_1_2.add(Platform(240, 220, 390, 20, 'red'))
platforms_2_2 = pygame.sprite.Group()
platforms_2_2.add(Platform(0, 340, 630, 20, 'red'))
platforms_2_2.add(Platform(0, 100, 270, 20, 'red'))
platforms_2_2.add(Platform(240, 220, 390, 20, 'red'))

walls_1_1 = pygame.sprite.Group()
walls_1_1.add(Platform(0, 0, 20, 360, 'blue'))
walls_2_1 = pygame.sprite.Group()
walls_2_1.add(Platform(611, 0, 20, 360, 'blue'))
walls_1_2 = pygame.sprite.Group()
walls_1_2.add(Platform(0, 0, 20, 360, 'blue'))
walls_2_2 = pygame.sprite.Group()
walls_2_2.add(Platform(611, 0, 20, 360, 'blue'))

ledges_left_1_1 = pygame.sprite.Group()
ledges_right_1_1 = pygame.sprite.Group()
ledges_left_1_1.add(Platform(90, 340, 30, 20, 'green'))
ledges_right_1_1.add(Platform(210, 220, 30, 20, 'green'))
ledges_left_1_1.add(Platform(90, 100, 30, 20, 'green'))
ledges_right_1_1.add(Platform(420, 100, 30, 20, 'green'))
ledges_left_1_2 = pygame.sprite.Group()
ledges_right_1_2 = pygame.sprite.Group()
ledges_left_1_2.add(Platform(210, 220, 30, 20, 'green'))
ledges_right_1_2.add(Platform(270, 100, 30, 20, 'green'))
ledges_left_1_2.add(Platform(90, -20, 30, 20, 'green'))

ledges_left_2_1 = pygame.sprite.Group()
ledges_right_2_1 = pygame.sprite.Group()
ledges_left_2_1.add(Platform(90, 340, 30, 20, 'green'))
ledges_right_2_1.add(Platform(210, 220, 30, 20, 'green'))
ledges_left_2_1.add(Platform(90, 100, 30, 20, 'green'))
ledges_right_2_1.add(Platform(420, 100, 30, 20, 'green'))
ledges_left_2_2 = pygame.sprite.Group()
ledges_right_2_2 = pygame.sprite.Group()
ledges_left_2_2.add(Platform(210, 220, 30, 20, 'green'))
ledges_right_2_2.add(Platform(270, 100, 30, 20, 'green'))
