import pygame as pg

class GameSprite(pg.sprite.Sprite):
    def __init__(self, image_name, width, height, speed, x, y, *args):
        self.image_list = []
        for a in args:
            self.image_list.append(a)
        self.number = len(self.image_list)
        self.counter = 0
        self.isAnim = False
        self.image = pg.transform.scale(pg.image.load(image_name), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
    def animation(self):
        if self.isAnim:
            self.counter += 1
        else:
            self.counter = 0

class Hero(GameSprite):
    def move(self, keys_pressed):
        if keys_pressed[pg.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        elif keys_pressed[pg.K_d] and self.rect.x < w - w/10:
            self.rect.x += self.speed
        elif keys_pressed[pg.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        elif keys_pressed[pg.K_s] and self.rect.y < h - w/10:
            self.rect.y += self.speed
    def put_bomb(self, keys_pressed):
        if keys_pressed[pg.K_SPACE]:
            pass
            # bomb = Bomb('bomb.png', w/10, w/10, 0, self.rect.x, self.rect.y)
            # bombs.append(bomb)

class Enemy(GameSprite):
    def move(self, keys_pressed):
        self.rect.x += self.speed
        if self.rect.x > w - w/10:
            self.speed *= -1
        elif self.rect.x < w - w/4:
            self.speed *= -1

class Bomb(GameSprite):
    def boom(self):
        pass

class Wall(pg.sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        super().__init__()
        self.color = color
        self.image = pg.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

win = pg.display.set_mode((700,500), pg.FULLSCREEN)
w, h = pg.display.get_window_size()
#print(w, h)
pg.display.set_caption('Лабиринт')
icon = pg.image.load('hero.png')
pg.display.set_icon(icon)
#фоновая музыка
pg.mixer.init()
pg.mixer.music.load('jungles.ogg')
pg.mixer.music.play()

#игровые обьекты
bg = pg.transform.scale(pg.image.load('background.jpg'), (w, h))
hero = Hero('hero.png', w/10, w/10, 10, 25, h - 75)
enemy = Enemy('cyborg.png', w/10, w/10, 3, w - 75, h - 150)
gold = GameSprite('treasure.png', w/10, w/10, 10, w - 75, h - 75)
wall1 = Wall(25, h - w/10, 150, 75, (75,83,32))
wall2 = Wall(w-350, 25, w/5 + 6, w/10+3, (75,83,32))
wall3 = Wall(25, h - w/10, w-215, 75, (75,83,32))

#переменные
bombs = list()
finish = False
run = True
clock = pg.time.Clock()
win_sound = pg.mixer.Sound('money.ogg') #здесь
lose_sound = pg.mixer.Sound('kick.ogg') #здесь
#игровой цикл
while run:
    for e in pg.event.get():
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = e.pos
                x -= int(w/20)
                y -= int(w/20)
                hero.rect.x, hero.rect.y = x, y
        if e.type == pg.QUIT:
            run = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                win = pg.display.set_mode((700,500))
                w = 700
                h = 500
                bg = pg.transform.scale(pg.image.load('background.jpg'), (w, h))
                hero = Hero('hero.png', w/10, w/10, 10, 25, h - 75)
                enemy = Enemy('cyborg.png', w/10, w/10, 3, w - 75, h - 150)
                gold = GameSprite('treasure.png', w/10, w/10, 10, w - 75, h - 75)
    
    if not finish:
        keys_pressed = pg.key.get_pressed()

        win.blit(bg, (0,0))
        hero.move(keys_pressed)
        hero.put_bomb(keys_pressed)
        enemy.move(keys_pressed)
        enemy.reset()
        wall1.reset()
        wall2.reset()
        wall3.reset()
        gold.reset()
        for b in bombs:
            b.reset()
        hero.reset()
        if pg.sprite.collide_rect(hero, gold):
            win_sound.play()
            finish = True
            victory = True
        if pg.sprite.collide_rect(hero, wall1):
            lose_sound.play()
            finish = True
            victory = False
        if pg.sprite.collide_rect(hero, wall2):
            lose_sound.play()
            finish = True
            victory = False
        if pg.sprite.collide_rect(hero, wall3):
            lose_sound.play()
            finish = True
            victory = False
        if pg.sprite.collide_rect(hero, enemy):
            lose_sound.play()
            finish = True
            victory = False
    if finish:
        if victory:
            bg = pg.transform.scale(pg.image.load('victory.jpg'), (w, h))
            win.blit(bg, (0,0))
        else:
            bg = pg.transform.scale(pg.image.load('gameover.jpg'), (w, h))
            win.blit(bg, (0,0))

    pg.display.update()
    clock.tick(60)