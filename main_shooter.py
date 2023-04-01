from pygame import *
import pygame
from time import time as timer
from random import randint
pygame.init()
info = display.Info()

HEIGHT = info.current_h
WIDTH = info.current_w

clock = time.Clock()
fps = 60

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Space Shooter")
"""
Change title
"""
display.set_icon(image.load("image/asteroid.png"))

background = transform.scale(image.load("image/galaxy.jpg"), (WIDTH, HEIGHT))
mixer.music.load("sounds/Endless Space.wav")
mixer.music.set_volume(0.1)
mixer.music.play()

shoot = mixer.Sound("sounds/fire.ogg")
shoot.set_volume(0.1)

game = True

start_reload = 0

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, x, y):
        super().__init__("image/rocket.png", x, y, HEIGHT // 6, HEIGHT // 5, HEIGHT // 50)

    def update_pos(self):
        global num_fire
        global reload
        global wait
        global start_reload
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < WIDTH - HEIGHT // 6 - 5:
            self.rect.x += self.speed
        if (keys_pressed[K_SPACE] and wait <= 0) and (num_fire <= 10 and not reload):
            self.fire()
            num_fire += 1
            wait = 7
        else:
            wait -= 1

        if num_fire == 10 and not reload:
            start_reload = timer()
            reload = True

        if reload:
            current_time = timer()
            reload_time = current_time - start_reload
            if reload_time < 2:
                text_reload = font_reload.render("Wait! Reload..." + str(int(reload_time)), True, (250, 55, 55))
                window.blit(text_reload, (WIDTH // 3, HEIGHT - WIDTH // 10))
            else:
                reload = False
                num_fire = 0

    def fire(self):
        bullet = Bullet(self.rect.centerx - HEIGHT // 60, ship.rect.top)
        bullets.add(bullet)
        shoot.play()

class Enemy(GameSprite):
    def __init__(self, x, y):
        super().__init__("image/ufo.png", x, y, HEIGHT // 6, HEIGHT // 10, HEIGHT // 300)

    def update(self):
        global text_lost
        global lost
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT:
            lost += 1
            self.rect.x = randint(0, WIDTH - HEIGHT // 4)
            self.rect.y = -HEIGHT // 5
            text_lost = font1.render("Пропущено: " + str(lost), True, (255, 255, 255))


class Bullet(GameSprite):
    def __init__(self, x, y):
        super().__init__("image/bullet.png", x, y, HEIGHT // 30, HEIGHT // 20, HEIGHT // 50)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -HEIGHT // 25:
            self.kill()

class Asteroid(GameSprite):
    def __init__(self, x, y):
        super().__init__("image/asteroid.png", x, y, HEIGHT // 8, HEIGHT // 8, HEIGHT // 600)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y >= HEIGHT:
            self.rect.x = randint(0, WIDTH - HEIGHT // 4)
            self.rect.y = - HEIGHT // 5

ship = Player((WIDTH - HEIGHT // 5) // 2, HEIGHT - HEIGHT // 4)

monsters = sprite.Group()
for i in range(10):
    monster = Enemy(randint(0, WIDTH - HEIGHT // 4), randint(- HEIGHT, - HEIGHT // 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid(randint(0, WIDTH - HEIGHT // 4), randint(- HEIGHT, - HEIGHT // 5))
    asteroids.add(asteroid)

bullets = sprite.Group()


font.init()
font1 = font.Font(None, HEIGHT // 30)
font_finish = font.Font(None, HEIGHT // 5)
font_reload = font.Font(None, HEIGHT // 15)

text_win = font_finish.render("You win!", True, (50, 255, 55))
text_lose = font_finish.render("You lose!", True, (250, 55, 55))

score = 0
text_score = font1.render("Рахунок: " + str(score), True, (255, 255, 255))

lost = 0
text_lost = font1.render("Пропущено: " + str(lost), True, (255, 255, 255))

finish = False
wait = 0
num_fire = 0
reload = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False

    if not finish:

        window.blit(background, (0, 0))
        ship.reset()
        ship.update_pos()

        monsters.draw(window)
        monsters.update()

        crush_list = sprite.spritecollide(ship, monsters, False)
        crush_asteroids_list = sprite.spritecollide(ship, asteroids, False)

        dead_monsters = sprite.groupcollide(monsters, bullets, False, True)

        for monster in dead_monsters:
            monster.rect.x = randint(0, WIDTH - HEIGHT // 4)
            monster.rect.y = randint(- HEIGHT // 2, - HEIGHT // 5)
            score += 1
            text_score = font1.render("Рахунок: " + str(score), True, (255, 255, 255))

        if len(crush_list) != 0 or lost >= 10 or len(crush_asteroids_list) != 0:
            finish = True
            window.blit(text_lose, (WIDTH // 3.2, HEIGHT // 2.5))

        if score >= 50:
            finish = True
            window.blit(text_win, (WIDTH // 3.2, HEIGHT // 2.5))

        asteroids.update()
        asteroids.draw(window)

        bullets.update()
        bullets.draw(window)

        window.blit(text_score, (WIDTH // 20, HEIGHT // 10))
        window.blit(text_lost, (WIDTH // 20, HEIGHT // 15))

    display.update()
    clock.tick(fps)

    display.update()
    clock.tick(60)