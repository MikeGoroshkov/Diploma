import pygame

archer_sheet = pygame.image.load('images/archer.png')

ghost_timer = pygame.USEREVENT = 1
pygame.time.set_timer(ghost_timer, 2500)
ghost_anim_count = 0
ghost_anim_timer = 0

ghost = [
    pygame.image.load('images/ghost_1.png').convert_alpha(),
    pygame.image.load('images/ghost_2.png').convert_alpha()
    ]
ghost_list_in_game = []

arrow = archer_sheet.subsurface(pygame.Rect((662,710), (46, 17)))
arrows_right = []
arrows_left = []

class Archer(pygame.sprite.Sprite):
    def __init__(self, x, y, bg_x, bg_y, lev):
        super().__init__()
        self.lev = lev
        self.x = x
        self.y = y
        self.bg_x = bg_x
        self.bg_y = bg_y
        self.damage = 30 * self.lev
        self.hp_max = 100 * self.lev
        self.hp = 100 * self.lev
        self.exp = 30 * self.lev
        self.archer_stay_right = archer_sheet.subsurface(pygame.Rect((3,4), (57, 78)))
        self.archer_stay_left = pygame.transform.flip(archer_sheet.subsurface(pygame.Rect((3,4), (57, 78))), True, False)
    def decrease_hp(self, player_damage):
        self.hp -= player_damage
        if self.hp < 0:
            self.hp = 0
        if self.hp > self.hp_max:
            self.hp = self.hp_max


enemy_hp_line_icon = pygame.image.load('images/enemy_hp_line.png')

archer_1 = Archer(550, 22, 0, 0, 1)
archer_2 = Archer(550, 262, 1, 0, 1)
archer_3 = Archer(500, 262, 0, 1, 2)
archers_full_list = [archer_1, archer_2, archer_3]
archers_list_in_game = [archer_1]

archer_shoot_anim_count = 0
archer_shoot_anim_timer = 0

archer_shoot_frame_height = 106
archer_shoot_frame_width = 105
archer_shoot_frame_count = 6
archer_shoot_pos = [(10 + i * (archer_shoot_frame_width + 1), 673) for i in range(archer_shoot_frame_count)]
archer_shoot_right = [archer_sheet.subsurface(pygame.Rect(pos, (archer_shoot_frame_width, archer_shoot_frame_height))) for pos in archer_shoot_pos]
archer_shoot_left = [pygame.transform.flip(archer_sheet.subsurface(pygame.Rect(pos, (archer_shoot_frame_width, archer_shoot_frame_height))), True, False) for pos in archer_shoot_pos]