import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 750, 750
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Shalini's Space!!!!!")
# load_images
red_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
blue_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
green_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))

# main_player
yellow_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# laser
red_laser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
blue_laser = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
green_laser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
yellow_laser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# background_image
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_Down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = yellow_space_ship
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class Enemy(Ship):
    Color_Map = {
        "red": (red_space_ship, red_laser),
        "blue": (blue_space_ship, blue_laser),
        "green": (green_space_ship, green_laser)

    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.Color_Map[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def main():
    run = True
    FPS = 60

    level = 0
    lives = 5
    mafont = pygame.font.SysFont("comicsans", 50)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    player = Player(250, 650)

    clock = pygame.time.Clock()

    def redraw_window():
        win.blit(BG, (0, 0))

        # draw_text
        lives_label = mafont.render(f"Lives:{lives}", 1, (255, 255, 255))
        level_label = mafont.render(f"Level:{level}", 1, (255, 255, 255))

        win.blit(lives_label, (10, 10))
        win.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for e in enemies:
            e.draw(win)

        player.draw(win)

        pygame.display.update()

    while run:
        clock.tick(FPS)

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                print("OK")
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1200, -100),
                          random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + 90 < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + 90 < HEIGHT:
            player.y += player_vel

        for e in enemies:
            e.move(enemy_vel)
            if e.y > HEIGHT:
                lives -= 1
                enemies.remove(e)

        redraw_window()


main()
