import pygame
import neat
import random
import gzip
import os

from pygame.rect import Rect

WIN_WIDTH = 1920
WIN_HEIGHT = 800
FLOOR = 670

GAME_SPEED = 20

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
prev = FLOOR - 120


class Player:
    IMGS = RUN_IMG

    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y + 30
        self.vel = 0
        self.height = 120
        self.img = SLIDE_IMG
        self.isDuck = False
        self.tick_count = 0
        self.img_count = 0
        self.onGround = False
        self.rect = Rect(self.x, self.y, self.img.get_height(), self.img.get_width())
        self.duckTimer = 0

    def jump(self):

        if self.onGround:
            self.duckTimer = 0
            self.vel = -13.5
            self.isDuck = False
            self.tick_count = 0

    def move(self):
        if self.y >= FLOOR - self.height:
            self.y = FLOOR - self.height
            self.onGround = True

        if self.y < FLOOR - self.height:
            self.onGround = False
        else:
            self.onGround = True

        self.tick_count += 1
        disp = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if disp >= 16:
            disp = 16
        if disp <= 0:
            disp -= 2

        self.y += disp

    def draw(self, win):

        # Cycling through images
        self.rect.y = self.y
        self.img_count += 1
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

        if self.isDuck:
            self.img = SLIDE_IMG

        new_rect = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(self.img, new_rect.topleft)

    def duck(self):

        if self.onGround:
            self.duckTimer += 0.1
            self.isDuck = True
            self.height = 90

    def unduck(self):
        self.duckTimer = 0
        self.height = 120
        self.isDuck = False

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Saw:
    VEL = GAME_SPEED

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = FLOOR - 120
        self.img = SAW_IMG
        self.passed = False
        self.rect = Rect(self.x, self.y, 120, 120)

        self.saw_height()

    def saw_height(self):
        # choice = random.choice([FLOOR - 120, FLOOR - 210])
        global prev
        if prev == FLOOR - 210:
            choice = FLOOR - 120
            prev = choice
        else:
            choice = FLOOR - 210
            prev = FLOOR - 210
        # choice = FLOOR - 210
        self.y = choice
        self.rect.y = choice

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        self.rect.x = self.x
        win.blit(self.img, (self.x, self.y))

    def collide(self, player):
        # player_mask = player.get_mask()
        #
        # saw_mask = pygame.mask.from_surface(self.img)
        # offset = (self.x - player.x, self.y - round(player.y))
        # point = player_mask.overlap(saw_mask, offset)
        # if point:
        #     return True
        # return False
        if pygame.sprite.collide_rect(self, player):
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


def draw_window(win, players, saws, base, score):
    win.blit(BG_IMG, (0, 0))
    for player in players:
        player.draw(win)

    for saw in saws:
        saw.draw(win)
    base.draw(win)

    text = STAT_FONT.render("SCORE  " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("GEN  " + str(gen - 1), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    text = STAT_FONT.render("ALIVE  " + str(len(players)), 1, (255, 255, 255))
    win.blit(text, (10, 50))

    pygame.display.update()


#
def eval_genomes(genomes, config):
    nets = []  # Neural nets for all the birds
    ge = []  # The bird neat variable with all the fitness and shit
    players = []  # The bird object
    global WIN, gen
    win = WIN
    gen += 1

    for _, g in genomes:
        g.fitness = 0
        # For each bird/Genome, create a new network
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(Player(200, FLOOR - 400))
        ge.append(g)

    score = 0

    # players.append(Player(200, 200))

    base = Base(800 - 120)

    saws = []
    saw = Saw(1000, FLOOR - 120)
    saws.append(saw)

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        # Spawn second saw
        if len(saws) < 2:
            saws.append(Saw(2000, FLOOR - 120))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

            # Single Player controls
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_DOWN:
            #         player.duck()
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_DOWN:
            #         player.unduck()
            #
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP:
            #         player.jump()

        if len(players) <= 0:
            run = False
            break
        saw_ind = 0
        if saws[0].x < players[0].x:
            saw_ind = 1

        for x, player in enumerate(players):
            ge[x].fitness += 0.1
            if player.isDuck:
                ge[x].fitness -= player.duckTimer

            if saws[saw_ind].y == FLOOR - 120:
                choice = 100
            else:
                choice = -100

            # Output = net.activate(inputs)
            output = nets[x].activate(
                (choice, abs(saws[saw_ind].x - players[0].x)))

            if output[0] > 0.5 and output[1] > 0.5:
                if output[0] > output[1]:
                    player.jump()
                else:
                    player.duck()
            elif output[0] > 0.5:
                player.jump()
            elif output[1] > 0.5:
                player.duck()
            if output[1] < 0.5:
                player.unduck()

        for y, saw in enumerate(saws):
            for x, player in enumerate(players):

                if saw.collide(player) or player.y < 0:
                    players.pop(x)
                    ge[x].fitness -= 7
                    nets.pop(x)
                    ge.pop(x)

            if not saw.passed and saw.x < player.x:
                saw.passed = True
                score += 1
                for g in ge:
                    g.fitness += 5

            if saw.x < 0:
                saws.remove(saw)

        draw_window(WIN, players, saws, base, score)

        base.move()
        for player in players:
            player.move()
        for saw in saws:
            saw.move()


#
#
# eval_genomes()


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
