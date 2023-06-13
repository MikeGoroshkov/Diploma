import pygame

pygame.init()

screen_width = 630
screen_height = 384
screen = pygame.display.set_mode((screen_width, screen_height)) #, flags=pygame.NOFRAME
pygame.display.set_caption("Escape from Zefira")
icon = pygame.image.load('images/icon.png') # https://www.iconfinder.com/
pygame.display.set_icon(icon)

bg = [pygame.image.load('images/back_1.png').convert_alpha(),
      pygame.image.load('images/back_2.png').convert_alpha(),
      pygame.image.load('images/back_3.png').convert_alpha()]