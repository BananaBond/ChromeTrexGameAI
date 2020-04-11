import pygame
import neat
import random
import os

WIN_WIDTH = 1920
WIN_HEIGHT = 800
FLOOR = 730

GAME_SPEED = 5

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

BG_IMG = (pygame.image.load(os.path.join("imgs", "BG.png")))
RUN_IMG = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Run__001.png")), (120, 120)),
           pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Run__004.png")), (120, 120)),
           pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Run__008.png")), (120, 120))]
SLIDE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Slide__000.png")), (120, 120))
DEAD_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Dead__009.png")), (120, 120))
JUMP_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Jump__001.png")), (120, 120))
SAW_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Saw.png")), (120, 120))
TILE_IMG = pygame.image.load(os.path.join("imgs", "Tilemap.png"))

pygame.font.init()
STAT_FONT = pygame.font.SysFont("roboto", 30)

gen = 0


class Player:
    IMGS = RUN_IMG
    ANIMATION_TIME = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.height = self.y
        self.img = self.IMGS[0]
        self.tick_count = 0
        self.img_count = 0

    def jump(self):
        self.vel = -10.5
        self.height = self.y
        self.tick_count = 0

    def move(self):
        self.tick_count += 2
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
        choice = random.choice([FLOOR + 120, FLOOR + 180])
        self.y = choice

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def collide(self, player):
        player_mask = player.get_mask()

        saw_mask = pygame.mask.from_surface(self.img)
        offset = (self.x - player.x, self.y - round(player.y))

        if offset:
            return True
        return False


class Base:
    VEL = GAME_SPEED
    IMG = TILE_IMG
    WIDTH = 1920

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


def draw_window(win, players, saws,  base):
    win.blit(BG_IMG, (0, 0))
    for player in players:
        player.draw(win)
    for saw in saws:
        saw.draw(win)
    pygame.display.update()
    base.draw(win)


def main():
    player = Player(200, 200)
    players = [player]

    base = Base(800-128)
    saw = Saw(100, 100)
    saws = [saw]

    saw.move()
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(WIN, players, saws, base)

        base.move()
        player.move()

    pygame.quit()
    quit()


main()
