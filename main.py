import pyxel
from random import randint, choice

frame_width = 128
frame_height = 128
frame_title = "Space Shooter"

pyxel.init(frame_width, frame_height, title=frame_title, quit_key=pyxel.KEY_ESCAPE)
pyxel.load("ressources.pyxres")

player_x = 64
player_y = 100
direction = 1
vies = 1
speed = 2
shoot_delay = 20
shoot_speed = 3
nb_shoots = 1
last_shoot = 0
shoots = []
score = 0
power_ups = []
power_ups_speed = 2
pu_choices = [1, 2, 3, 4]
enemy_to_spawn = 0
enemies = []
enemy_shoot_delay = 60
enemy_bullets = []

level = 1
levels = {
    1: {"enemy1": 5},
    2: {"enemy1": 5, "enemy2": 3},
    3: {"enemy1": 4, "enemy2": 8, "enemy3": 8},
    4: {"enemy1": 10, "enemy2": 10, "enemy3": 10},
    5: {"enemy1": 14, "enemy2": 12, "enemy3": 8},
    6: {"enemy1": 20, "enemy2": 15, "enemy3": 10, "enemy4": 6},
    7: {"enemy1": 20, "enemy2": 15, "enemy3": 10, "enemy4": 14},
    8: {"enemy1": 30, "enemy2": 20, "enemy3": 20, "enemy4": 20},
    9: {"enemy1": 35, "enemy2": 25, "enemy3": 20, "enemy4": 20, "enemy5": 20},
    10: {"enemy1": 40, "enemy2": 30, "enemy3": 25, "enemy4": 27, "enemy5": 25}

}


class Enemy1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie = 1
        self.speed = 2
        self.pts_on_death = 10

    def update(self):
        self.y += self.speed

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 8, 8, 8, 0)


class Enemy2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie = 1
        self.speed = 2
        self.last_shoot = 0
        self.pts_on_death = 15

    def update(self):
        self.y += self.speed
        if pyxel.frame_count - enemy_shoot_delay >= self.last_shoot:
            enemy_shoot(self)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 40, 8, 8, 8, 0)


class Enemy3:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie = 2
        self.speed = 2
        self.pts_on_death = 20

    def update(self):
        self.y += self.speed

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 56, 8, 8, 8, 0)


class Enemy4:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie = 2
        self.speed = 1
        self.last_shoot = 0
        self.pts_on_death = 25

    def update(self):
        self.y += self.speed
        if pyxel.frame_count - enemy_shoot_delay >= self.last_shoot:
            enemy_shoot(self)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 48, 8, 8, 8, 0)


class Enemy5:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie = 3
        self.speed = 1
        self.last_shoot = 0
        self.pts_on_death = 30

    def update(self):
        self.y += self.speed
        if pyxel.frame_count - enemy_shoot_delay >= self.last_shoot:
            enemy_shoot(self)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 72, 8, 8, 8, 0)


class Bullet:
    def __init__(self, x, y, bullet_speed):
        self.x = x
        self.y = y
        self.speed = bullet_speed


def enemy_shoot(enemy):
    enemy.last_shoot = pyxel.frame_count
    global enemy_bullets
    enemy_bullets.append(Bullet(enemy.x, enemy.y+8, enemy.speed+2))
    return enemy_bullets


def player_move(player_x, player_y):
    direction = 1
    if pyxel.btn(pyxel.KEY_RIGHT):
        if player_x <= 118:
            player_x += speed
            direction = 2
    if pyxel.btn(pyxel.KEY_LEFT):
        if player_x >= 2:
            player_x -= speed
            direction = 0
    if pyxel.btn(pyxel.KEY_UP):
        if player_y >= 2:
            player_y -= speed
    if pyxel.btn(pyxel.KEY_DOWN):
        if player_y <= 118:
            player_y += speed
    return player_x, player_y, direction


def new_shoot(shoots):
    global last_shoot
    if pyxel.frame_count - shoot_delay >= last_shoot and pyxel.btn(pyxel.KEY_SPACE):
        pyxel.playm(2)
        shoots.append([player_x + 3, player_y - 8])
        last_shoot = pyxel.frame_count
    return shoots


def move_shoots(shoots):
    for shoot in shoots:
        shoot[1] -= shoot_speed
    return shoots


def draw_shoots():
    for shoot in shoots:
        if nb_shoots == 1:
            pyxel.blt(shoot[0], shoot[1], 0, 3, 25, 2, 6, 0)
        if nb_shoots == 2:
            pyxel.blt(shoot[0], shoot[1], 0, 1, 33, 6, 6, 0)


def enemy_spawn(liste):
    global levels, level
    u = choice(list(levels[level].keys()))
    levels[level][u] -= 1
    if levels[level][u] <= 0:
        del levels[level][u]

    x = randint(3, frame_width-3-8)
    y = randint(3, 10)

    if u == 'enemy1':
        mob = Enemy1(x, y)
    elif u == 'enemy2':
        mob = Enemy2(x, y)
    elif u == 'enemy3':
        mob = Enemy3(x, y)
    elif u == 'enemy4':
        mob = Enemy4(x, y)
    else:
        mob = Enemy5(x, y)
    liste.append(mob)
    return liste


def life_update(lives):
    global pu_choices, score
    for enemy in enemies:
        if enemy.x <= player_x+8 and enemy.y <= player_y+8 and enemy.x+8 >= player_x and enemy.y+8 >= player_y:
            enemies.remove(enemy)
            score += enemy.pts_on_death
            lives -= 1
            pu_choices.append(4)
            if lives == 0:
                pyxel.playm(3)
    return lives


def kill_enemies():
    for enemy in enemies:
        for shoot in shoots:
            if enemy.x <= shoot[0]+2 and enemy.y <= shoot[1]+6 and enemy.x+8 >= shoot[0] and enemy.y+8 >= shoot[1]:
                enemy_x = enemy.x
                enemy_y = enemy.y
                enemy.vie -= 1
                if enemy.vie == 0:
                    enemies.remove(enemy)
                    global score
                    score += enemy.pts_on_death
                    if randint(1, 10) == 10:
                        spawn_power_up(enemy_x, enemy_y)
                shoots.remove(shoot)
    return shoots, enemies


def spawn_power_up(x, y):
    global power_ups
    nb_pu = choice(pu_choices)
    power_ups.append([x, y, nb_pu])


def draw_pu():
    for pu in power_ups:
        pyxel.blt(pu[0], pu[1], 0, pu[2]*8, 80, 8, 8, 0)


def move_pu():
    for pu in power_ups:
        pu[1] += power_ups_speed
    return power_ups


def use_pu(power_ups, speed, shoot_delay, nb_shoots, vies):
    global pu_choices
    for pu in power_ups:
        if pu[0] <= player_x+8 and pu[1] <= player_y+8 and pu[0]+8 >= player_x and pu[1]+8 >= player_y:
            pyxel.playm(0)
            if pu[2] == 0:
                speed += 1
                power_ups.remove(pu)
                pu_choices.remove(1)
            if pu[2] == 1:
                shoot_delay /= 2
                power_ups.remove(pu)
                if shoot_delay <= 5:
                    pu_choices.remove(2)
            if pu[2] == 2:
                nb_shoots += 1
                power_ups.remove(pu)
                pu_choices.remove(3)
            if pu[2] == 3:
                vies += 1
                power_ups.remove(pu)
                if vies == 3:
                    pu_choices.remove(4)
    return power_ups, speed, shoot_delay, nb_shoots, vies
     

def update():
    global vies
    if vies > 0:
        global player_x, player_y, shoots, score, enemies, enemy_to_spawn, direction, power_ups, speed, shoot_delay, nb_shoots, level
        player_x, player_y, direction = player_move(player_x, player_y)
        shoots = new_shoot(shoots)
        shoots = move_shoots(shoots)
        shoots, enemies = kill_enemies()
        power_ups = move_pu()
        power_ups, speed, shoot_delay, nb_shoots, vies = use_pu(power_ups, speed, shoot_delay, nb_shoots, vies)
        try:
            enemy_to_spawn = sum(levels[level].values())
        except KeyError:
            enemy_to_spawn = 0
        if pyxel.frame_count % 30 == 0 and enemy_to_spawn > 0:
            enemies = enemy_spawn(enemies)
            enemy_to_spawn -= 1

        for enemy in enemies:
            enemy.update()
            if enemy.y >= 128:
                enemy.y = 0
                enemy.x = randint(3, 128-3-8)
        
        for bullet in enemy_bullets:
                bullet.y += bullet.speed
                if bullet.y >= frame_height:
                    enemy_bullets.remove(bullet)
                elif player_x + 8 >= bullet.x and bullet.x + 8 >= player_x and player_y + 8 >= bullet.y and bullet.y + 8 >= player_y:
                    enemy_bullets.remove(bullet)
                    vies -= 1

        vies = life_update(vies)
        if len(enemies) == 0 and enemy_to_spawn == 0:
                level += 1


def draw():
    pyxel.cls(0)
    if vies >= 1:
        if level > len(levels):
            pyxel.blt(33, 60, 0, 0, 97, 61, 7)
        else:
            pyxel.bltm(0, 0, 0, 0, (-(pyxel.frame_count // 2) % 256), 128, 256)
            if direction == 1:
                pyxel.blt(player_x, player_y, 0, 0, 8, 8, 8, 0)
            elif direction == 0:
                pyxel.blt(player_x, player_y, 0, 8, 8, 8, 8, 0)
            elif direction == 2:
                pyxel.blt(player_x, player_y, 0, 16, 8, 8, 8, 0)
            for enemy in enemies:
                enemy.draw()
            pyxel.text(5, 5, f"VIES : {vies}", 7)
            pyxel.text(70, 5, f"SCORE : {score}", 7)
            draw_shoots()
            for bullet in enemy_bullets:
                pyxel.blt(bullet.x, bullet.y, 0, 0, 16, 8, 8, 0)
            draw_pu()
    else:
        pyxel.blt(33, 60, 0, 0, 137, 61, 7)
        pyxel.text(37, 70, f"SCORE : {score}", 7)
        

pyxel.run(update, draw)
