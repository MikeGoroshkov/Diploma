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

drug_1 = Item('drug', drug, 150, 84, 0, 0)
drug_2 = Item('drug', drug, 90, 84, 1, 1)
drug_3 = Item('drug', drug, 430, 204, 2, 0)
drug_4 = Item('drug', drug, 70, 204, 4, 1)
drug_5 = Item('drug', drug, 540, 204, 6, 1)
key_1 = Item('key', key, 590, 84, 1, 0)
key_2 = Item('key', key, 70, 84, 3, 1)
key_3 = Item('key', key, 70, 84, 4, 0)
key_4 = Item('key', key, 530, 84, 6, 0)

items_list_start = [drug_1, drug_2, drug_3, drug_4, drug_5,key_1, key_2, key_3, key_4]
items_list = items_list_start[:]
inventory_list = []

