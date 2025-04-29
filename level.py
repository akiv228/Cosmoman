import pygame as pg
from maze_generation import generate_maze
from player import Player
from game_classes import Wall, Prize, GameSprite
from constants import WIDTH, HEIGHT
from grafics_classes import Backgrounds, Fon
from grafics import starfield
import random


class Level:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.grid_sizes = {'EASY': (16, 12), 'MEDIUM': (16, 12), 'HARD': (20, 15),
                           'EXPLORE': (random.randint(18, 22), random.randint(13, 17))}
        gw, gh = self.grid_sizes[difficulty]
        wall_rects = generate_maze(gw, gh, difficulty)
        self.walls = pg.sprite.Group()
        for rect in wall_rects:
            self.walls.add(Wall(rect.x, rect.y, rect.width, rect.height))
        self.all_sprites, self.player, self.final = self.place_objects(gw, gh)
        self.background = self.get_background()

    def place_objects(self, gw, gh):
        all_sprites = pg.sprite.Group()

        player = Player('images\\astronaut.png', , , 30, 35, 0,
                        0, False, False, 3)
        final = GameSprite('images\\planet.png', , , 40, 70,
                           False)


        player.walls = self.walls

        player.bullets = pg.sprite.Group()
        player.limit = {'EASY': 20, 'MEDIUM': 15, 'HARD': 10, 'EXPLORE': 15}[self.difficulty]
        all_sprites.add(self.walls, player, final)
        return all_sprites, player, final

    def get_background(self):
        if self.difficulty == 'EASY':
            return Backgrounds('images\\back.jpg', WIDTH, HEIGHT, 0, 0)
        elif self.difficulty == 'MEDIUM':
            return Fon(w=5000, h=900, stars_count=2000)
        else:
            return starfield

    def update(self):
        self.player.update()
        self.player.bullets.update()
        pg.sprite.groupcollide(self.player.bullets, self.walls, True, False)

    def render(self, window):
        if self.difficulty == 'EASY':
            self.background.reset(window)
        elif self.difficulty == 'MEDIUM':
            self.background.update(window)
        else:
            window.blit(self.background.alpha_surface, (0, 0))
            self.background.run()
        self.all_sprites.draw(window)
        self.player.bullets.draw(window)