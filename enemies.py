import pygame

enemy_hp_line_icon = pygame.image.load('images/enemy_hp_line.png')

archer_sheet = pygame.image.load('images/archer.png')
arrow = archer_sheet.subsurface(pygame.Rect((662,710), (46, 17)))
arrows_right = []
arrows_left = []

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, bg_x, bg_y, lev):
        super().__init__()
        self.lev = lev
        self.x = x
        self.y = y
        self.bg_x = bg_x
        self.bg_y = bg_y
        self.alive = True
        self.damage = 30 * self.lev
        self.hp_max = 100 * self.lev
        self.hp = 100 * self.lev
        self.exp = 30 * self.lev

    def decrease_hp(self, player_damage):
        self.hp -= player_damage
        if self.hp < 0:
            self.hp = 0
        if self.hp > self.hp_max:
            self.hp = self.hp_max

class Archer(Enemy):
    def __init__(self, x, y, bg_x, bg_y, lev):
        super().__init__(x, y, bg_x, bg_y, lev)
        self.archer_stay_right = archer_sheet.subsurface(pygame.Rect((3,4), (57, 78)))
        self.archer_stay_left = pygame.transform.flip(archer_sheet.subsurface(pygame.Rect((3,4), (57, 78))), True, False)
        self.damage = 30 * self.lev
        self.hp_max = 100 * self.lev
        self.hp = 100 * self.lev
        self.exp = 30 * self.lev


archer_1 = Archer(520, 22, 0, 0, 1)
archer_2 = Archer(500, 262, 1, 0, 1)
archer_3 = Archer(500, 262, 0, 1, 1)
archer_4 = Archer(480, 142, 2, 1, 1.5)
archer_5 = Archer(360, 22, 2, 0, 1.5)
archer_6 = Archer(480, 22, 3, 0, 1.5)

archers_full_list = [archer_1, archer_2, archer_3, archer_4, archer_5, archer_6]
archers_list_in_game = [archer_1]

archer_shoot_anim_count = 0
archer_shoot_anim_timer = 0
archer_died_anim_count = 0
archer_died_anim_timer = 0

archer_shoot_frame_height = 106
archer_shoot_frame_width = 105
archer_shoot_frame_count = 6
archer_shoot_pos = [(10 + i * (archer_shoot_frame_width + 1), 673) for i in range(archer_shoot_frame_count)]
archer_shoot_right = [archer_sheet.subsurface(pygame.Rect(pos, (archer_shoot_frame_width, archer_shoot_frame_height))) for pos in archer_shoot_pos]
archer_shoot_left = [pygame.transform.flip(archer_sheet.subsurface(pygame.Rect(pos, (archer_shoot_frame_width, archer_shoot_frame_height))), True, False) for pos in archer_shoot_pos]

archer_died_frame_height = 106
archer_died_frame_width = 105
archer_died_frame_count = 6
archer_died_pos = [(10 + i * (archer_died_frame_width + 1), 893-107) for i in range(archer_died_frame_count)]
archer_died_right = [archer_sheet.subsurface(pygame.Rect(pos, (archer_died_frame_width, archer_died_frame_height))) for pos in archer_died_pos]
archer_died_left = [pygame.transform.flip(archer_sheet.subsurface(pygame.Rect(pos, (archer_died_frame_width, archer_died_frame_height))), True, False) for pos in archer_died_pos]

fly_sheet = pygame.image.load('images/fly.png')
class Fly(Enemy):
    def __init__(self, x_0, y_0, bg_x, bg_y, width, lev):
        super().__init__(x_0, y_0, bg_x, bg_y, lev)
        self.x_0 = x_0
        self.y_0 = y_0
        self.x = self.x_0
        self.y = self.y_0
        self.right = False
        self.width = width
        self.damage = 30 * self.lev
        self.hp_max = 60 * self.lev
        self.hp = 60 * self.lev
        self.exp = 20 * self.lev
        self.fly_stay_right = fly_sheet.subsurface(pygame.Rect((10,0), (52, 47)))
        self.fly_stay_left = pygame.transform.flip(fly_sheet.subsurface(pygame.Rect((10,0), (52, 47))), True, False)


fly_frame_height = 47
fly_frame_width = 52
fly_frame_count = 4
fly_pos = [(10 + i * (fly_frame_width + 1), 0) for i in range(fly_frame_count)]
fly_left = [fly_sheet.subsurface(pygame.Rect(pos, (fly_frame_width, fly_frame_height))) for pos in fly_pos]
fly_right = [pygame.transform.flip(fly_sheet.subsurface(pygame.Rect(pos, (fly_frame_width, fly_frame_height))), True, False) for pos in fly_pos]

fly_died_frame_height = 47
fly_died_frame_width = 52
fly_died_frame_count = 3
fly_died_pos = [(10 + i * (fly_died_frame_width + 1), 75) for i in range(fly_died_frame_count)]
fly_died_left = [fly_sheet.subsurface(pygame.Rect(pos, (fly_died_frame_width, fly_died_frame_height))) for pos in fly_died_pos]
fly_died_right = [pygame.transform.flip(fly_sheet.subsurface(pygame.Rect(pos, (fly_died_frame_width, fly_died_frame_height))), True, False) for pos in fly_died_pos]

fly_1 = Fly(580, 250, 0, 0, 500, 1)
fly_2 = Fly(580, 130, 0, 1, 400, 1)
fly_3 = Fly(580, 10, 1, 1, 500, 1)
fly_4 = Fly(580, 250, 2, 0, 500, 1.5)
fly_5 = Fly(580, 250, 3, 0, 500, 1.5)
fly_6 = Fly(580, 250, 3, 1, 500, 1.5)
fly_full_list = [fly_1, fly_2, fly_3, fly_4, fly_5, fly_6]
fly_list_in_game = [fly_1]

fly_anim_count = 0
fly_anim_timer = 0
fly_died_anim_count = 0
fly_died_anim_timer = 0


soldier_sheet = pygame.image.load('images/soldier.png')
pellet = pygame.image.load('images/pellet.png')
pellets_right = []
pellets_left = []
class Soldier(Enemy):
    def __init__(self, x, y, bg_x, bg_y, lev):
        super().__init__(x, y, bg_x, bg_y, lev)
        self.damage = 20 * self.lev
        self.hp_max = 120 * self.lev
        self.hp = 120 * self.lev
        self.exp = 50 * self.lev
        self.soldier_stay_right = soldier_sheet.subsurface(pygame.Rect((10,2), (76, 78)))
        self.soldier_stay_left = pygame.transform.flip(soldier_sheet.subsurface(pygame.Rect((3,2), (57, 78))), True, False)


soldier_1 = Soldier(400, 22, 4, 1, 1)
soldier_2 = Soldier(100, 142, 5, 1, 1)
soldier_3 = Soldier(500, 262, 4, 0, 1)
soldier_4 = Soldier(200, 22, 4, 0, 1.5)
soldier_5 = Soldier(550, 262, 5, 0, 1)
soldier_6 = Soldier(260, 142, 5, 0, 1)
soldier_7 = Soldier(500, 262, 6, 1, 1.5)
soldier_8 = Soldier(570, 22, 6, 0, 1.5)
# soldier_9 = Soldier(140, 22, 7, 0, 1.5)
soldier_10 = Soldier(80, 262, 7, 1, 1.5)

soldiers_full_list = [soldier_1, soldier_2, soldier_3, soldier_4, soldier_5, soldier_6, soldier_7, soldier_8, soldier_10]
soldiers_list_in_game = []

soldier_shoot_anim_count = 0
soldier_shoot_anim_timer = 0
soldier_died_anim_count = 0
soldier_died_anim_timer = 0

soldier_shoot_frame_height = 78
soldier_shoot_frame_width = 76
soldier_shoot_frame_count = 3
soldier_shoot_pos = [(87 + i * (soldier_shoot_frame_width + 1), 0) for i in range(soldier_shoot_frame_count)]
soldier_shoot_right = [soldier_sheet.subsurface(pygame.Rect(pos, (soldier_shoot_frame_width, soldier_shoot_frame_height))) for pos in soldier_shoot_pos]
soldier_shoot_left = [pygame.transform.flip(soldier_sheet.subsurface(pygame.Rect(pos, (soldier_shoot_frame_width, soldier_shoot_frame_height))), True, False) for pos in soldier_shoot_pos]

soldier_died_frame_height = 78
soldier_died_frame_width = 76
soldier_died_frame_count = 4
soldier_died_pos = [(10 + i * (soldier_died_frame_width + 1), 87) for i in range(soldier_died_frame_count)]
soldier_died_right = [soldier_sheet.subsurface(pygame.Rect(pos, (soldier_died_frame_width, soldier_died_frame_height))) for pos in soldier_died_pos]
soldier_died_left = [pygame.transform.flip(soldier_sheet.subsurface(pygame.Rect(pos, (soldier_died_frame_width, soldier_died_frame_height))), True, False) for pos in soldier_died_pos]


alien_sheet = pygame.image.load('images/alien.png')
class Alien(Enemy):
    def __init__(self, x_0, y_0, bg_x, bg_y, width, lev):
        super().__init__(x_0, y_0, bg_x, bg_y, lev)
        self.x_0 = x_0
        self.y_0 = y_0
        self.x = self.x_0
        self.y = self.y_0
        self.width = width
        self.right = False
        self.shock = False
        self.damage = 40 * self.lev
        self.hp_max = 140 * self.lev
        self.hp = 140 * self.lev
        self.exp = 70 * self.lev
        self.alien_stay_right = alien_sheet.subsurface(pygame.Rect((10,2), (76, 78)))
        self.alien_stay_left = pygame.transform.flip(alien_sheet.subsurface(pygame.Rect((3,2), (57, 78))), True, False)

alien_walk_frame_height = 92
alien_walk_frame_width = 58
alien_walk_frame_count = 10
alien_walk_pos = [(i * (alien_walk_frame_width + 1), 0) for i in range(alien_walk_frame_count)]
alien_walk_left = [alien_sheet.subsurface(pygame.Rect(pos, (alien_walk_frame_width, alien_walk_frame_height))) for pos in alien_walk_pos]
alien_walk_right = [pygame.transform.flip(alien_sheet.subsurface(pygame.Rect(pos, (alien_walk_frame_width, alien_walk_frame_height))), True, False) for pos in alien_walk_pos]

alien_died_frame_height = 92
alien_died_frame_width = 58
alien_died_frame_count = 5
alien_died_pos = [(i * (alien_died_frame_width + 1), 100) for i in range(alien_died_frame_count)]
alien_died_left = [alien_sheet.subsurface(pygame.Rect(pos, (alien_died_frame_width, alien_died_frame_height))) for pos in alien_died_pos]
alien_died_right = [pygame.transform.flip(alien_sheet.subsurface(pygame.Rect(pos, (alien_died_frame_width, alien_died_frame_height))), True, False) for pos in alien_died_pos]

alien_1 = Alien(330, 8, 7, 0, 330, 1)
alien_2 = Alien(500, 248, 7, 1, 400, 1)

aliens_full_list = [alien_1, alien_2]
aliens_list_in_game = []

alien_walk_anim_count = 0
alien_walk_anim_timer = 0
alien_died_anim_count = 0
alien_died_anim_timer = 0

