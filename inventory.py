import pygame

item_sheet = pygame.image.load('images/archer.png')
class Item(pygame.sprite.Sprite):
    def __init__(self, name, image, x, y, bg_x, bg_y):
        super().__init__()
        self.name = name
        self.image = image
        self.x = x
        self.y = y
        self.bg_x = bg_x
        self.bg_y = bg_y
        self.rect = self.image.get_rect(topleft=(x, y))

border = pygame.image.load('images/border.png').convert_alpha()
border_x = 588
border_y = 3
border_pos = 0
border_rect = border.get_rect(topleft=(border_x, border_y))
is_delay = False
delay_timer = 0

drug = pygame.image.load('images/drug.png').convert_alpha()
key = pygame.image.load('images/card-key.png').convert_alpha()

drug_1 = Item('drug', drug, 50, 204, 0, 0)
key_1 = Item('key', key, 590, 84, 1, 0)

items_list_start = [drug_1, key_1]
items_list = items_list_start
inventory_list = [drug_1, key_1]

