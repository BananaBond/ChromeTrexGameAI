import pygame
import neat
import random
import os


WIN_WIDTH = 1000
WIN_HEIGHT = 800
FLOOR = 730

GAME_SPEED = 5


WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

BG_IMG = (pygame.image.load(os.path.join("imgs", "BG.png")))
RUN_IMG = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Run__001.png")), (120, 120)), pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Run__004.png")), (120, 120)), pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Run__008.png")), (120, 120))]
SLIDE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Slide__000.png")), (120, 120))
DEAD_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Dead__009.png")), (120, 120))
JUMP_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Jump__001.png")), (120, 120))



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
        self.height = self. y
        self.img = self.IMGS[0]
        self.tick_count = 0
        self.img_count = 0

    def jump(self):
        self.vel = -10.5
        self.height = self.y
        self.tick_count = 0

    def move(self):
        self.tick_count += 1
        disp = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if disp >=16:
            disp = 16
        if disp <=0:
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




def draw_window(win, player):
    win.blit(BG_IMG, (0, 0))
    player.draw(win)
    pygame.display.update()

def main():
    player = Player(200, 200)

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False
        draw_window(WIN, player)

    pygame.quit()
    quit()

main()


