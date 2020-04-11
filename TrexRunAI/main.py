import pygame
import neat
import random
import os

WIN_WIDTH = 1920
WIN_HEIGHT = 800
FLOOR = 680

GAME_SPEED = 15

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

BG_IMG = (pygame.image.load(os.path.join("imgs", "BG.png")))
RUN_IMG = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Run__001.png")), (120, 120)),
           pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Run__004.png")), (120, 120)),
           pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Run__008.png")), (120, 120))]
SLIDE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Slide__000.png")), (90, 90))
DEAD_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Dead__009.png")), (120, 120))
JUMP_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Jump__001.png")), (80, 80))
SAW_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Saw.png")), (120, 120))
TILE_IMG = pygame.image.load(os.path.join("imgs", "Tilemap.png"))

pygame.font.init()
STAT_FONT = pygame.font.SysFont("roboto", 30)

gen = 0


class Player:
    IMGS = RUN_IMG

    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y + 30
        self.vel = 0
        self.height = 120
        self.img = SLIDE_IMG

        self.tick_count = 0
        self.img_count = 0

    def jump(self):
        self.vel = -19.5

        self.tick_count = 0

    def move(self):
        self.tick_count += 1
        disp = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if disp >= 16:
            disp = 16
        if disp <= 0:
            disp -= 2

        self.y += disp

    def draw(self, win):
        self.img_count += 1

        # Cycling through images
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        new_rect = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(self.img, new_rect.topleft)

    def duck(self):
        self.img = SLIDE_IMG
        self.height = 90

    def unduck(self):
        self.height = 120


    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Saw:
    VEL = GAME_SPEED

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 0
        self.img = SAW_IMG
        self.passed = False
        self.saw_height()

    def saw_height(self):
        choice = random.choice([FLOOR - 120, FLOOR - 210])
        self.y = choice

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def collide(self, player):
        player_mask = player.get_mask()

        saw_mask = pygame.mask.from_surface(self.img)
        offset = (self.x - player.x, self.y - round(player.y))
        point = player_mask.overlap(saw_mask, offset)
        if point:
            return True
        return False


class Base:
    VEL = GAME_SPEED
    WIDTH = TILE_IMG.get_width()
    IMG = TILE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, players, saws, base):
    win.blit(BG_IMG, (0, 0))
    for player in players:
        player.draw(win)
    for saw in saws:
        saw.draw(win)
    base.draw(win)
    pygame.display.update()


def main():
    player = Player(200, FLOOR - 400)

    players = [player]

    base = Base(800 - 120)

    saws = []
    saw = Saw(1000, FLOOR - 120)
    saws.append(saw)

    run = True

    while run:
        if len(saws) < 2:
            saws.append(Saw(2000, FLOOR-120))
        




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player.duck()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.unduck()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.jump()

        for player in players:
            if player.y > FLOOR - player.height:
                player.y = FLOOR - player.height

        for y, saw in enumerate(saws):
            for x, player in enumerate(players):
                if saw.collide(player):
                    players.pop(x)
                if saw.x < player.x:
                    saw.passed = True
                if saw.x < 0:
                    saws.pop(y)

        draw_window(WIN, players, saws, base)

        base.move()
        for player in players:
            player.move()
        for saw in saws:
            saw.move()

    pygame.quit()
    quit()


main()
