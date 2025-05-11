import pygame as pg
import random
import math

vec2, vec3 = pg.math.Vector2, pg.math.Vector3

from config import WIDTH, HEIGHT, Z_DISTANCE

Z_DISTANCE = 90  # расстояние по оси z  с которого начнут двигаться звезды
ALPHA = 350
NUM_STARS = 1000

RES = WIDTH, HEIGHT
CENTER = vec2(WIDTH // 2, HEIGHT // 2)



class Star:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.pos3d = self.get_initial_pos3d(config['scale_pos'])
        self.vel = random.uniform(config['vel_min'], config['vel_max'])
        self.color = random.choice(config['colors'])
        self.screen_pos = vec2(0, 0)
        self.size = 5

    def get_initial_pos3d(self, scale_pos):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * scale_pos
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = random.uniform(1, Z_DISTANCE)
        return vec3(x, y, z)

    def get_pos3d(self, scale_pos):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * scale_pos
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = Z_DISTANCE
        return vec3(x, y, z)

    def update(self, speed_multiplier, rotation_speed):
        self.pos3d.z -= self.vel * speed_multiplier
        if self.pos3d.z < 1:
            self.pos3d = self.get_pos3d(self.config['scale_pos'])
        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.15 * self.pos3d.z)
        self.pos3d.xy = self.pos3d.xy.rotate(rotation_speed)

    def draw(self, alpha):
        s = self.size
        if (-s < self.screen_pos.x < WIDTH + s) and (-s < self.screen_pos.y < HEIGHT + s):
            color = pg.Color(self.color)
            color.a = int(alpha * 255)
            pg.draw.rect(self.screen, color, (*self.screen_pos, self.size, self.size))

class Starfield:
    def __init__(self, screen, config):
        self.screen = screen
        self.stars = [Star(screen, config) for _ in range(config['num_stars'])]
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(config['alpha'])

    def update(self, speed_multiplier, rotation_speed):
        for star in self.stars:
            star.update(speed_multiplier, rotation_speed)
        self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)

    def draw(self, alpha):
        self.screen.blit(self.alpha_surface, (0, 0))
        for star in self.stars:
            star.draw(alpha)