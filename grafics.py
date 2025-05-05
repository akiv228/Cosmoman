import pygame as pg
import random

class Star:
    def __init__(self, w, h):
        self.x = random.randint(0, w)
        self.y = random.randint(0, h)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 2)

class Starfield:
    def __init__(self, w, h, star_count):
        self.w = w
        self.h = h
        self.stars = [Star(w, h) for _ in range(star_count)]
        self.alpha_surface = pg.Surface((w, h), pg.SRCALPHA)

    def run(self):
        self.alpha_surface.fill((0, 0, 0, 255))
        for star in self.stars:
            star.y += star.speed
            if star.y > self.h:
                star.y = 0
                star.x = random.randint(0, self.w)
            pg.draw.circle(self.alpha_surface, (255, 255, 255), (int(star.x), int(star.y)), star.size)

starfield = Starfield(710, 540, 300)
