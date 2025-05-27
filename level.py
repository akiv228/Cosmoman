

import pygame as pg
from pygame import time
import random
from maze_generation import generate_maze
from grafics.maze_fons import Starfield_white, Starfield_palette
import createwalls
import path_utils
import upload_maze
from planet import FinalGifSprite
from player import Player
from game_sprites import Wall, GameSprite
from enemy_manager import EnemyManager
# from grafics_classes import Backgrounds, Starfield_white, Starfield_palette
from grafics import *
from test_gradient_for_labirints import Fon2_2

class Level:
    def __init__(self, difficulty, debug_mode=True, load_from_file=False, filename="maze_data.pkl"):
        self.difficulty = difficulty
        self.debug_mode = debug_mode
        self.grid_sizes = {
            'EASY': (16, 12),
            'MEDIUM': (16, 12),
            'HARD': (20, 15),
            'EXPLORE': (random.randint(18, 22), random.randint(13, 17))
        }

        if load_from_file:
            self.maze_info = upload_maze.load_maze(filename)
            gw, gh = self.maze_info['grid_width'], self.maze_info['grid_height']
        else:
            gw, gh = self.grid_sizes[difficulty]
            self.maze_info = generate_maze(gw, gh, difficulty)
            upload_maze.save_maze(filename, self.maze_info)

        self.walls = pg.sprite.Group()
        wall_rects = createwalls.reconstruct_wall_rects(self.maze_info)
        for rect in wall_rects:
            self.walls.add(Wall(rect.x, rect.y, rect.width, rect.height))

        self.grid = (gw, gh)
        self.path = []

        start_pos, final_pos, self.path = path_utils.calculate_positions(self.maze_info, self.grid, self.debug_mode)
        self.init_sprites(start_pos, final_pos)

        # Инициализация системы "тумана войны"
        # self.init_fog_of_war()
        
        self.background = self.get_background()
        self.enemy_manager = EnemyManager(self)
        self.enemy_manager.spawn_enemies()

    def init_fog_of_war(self):
        """Инициализирует систему тумана войны с облаками"""
        # Загружаем изображение облака
        try:
            self.cloud_image = pg.image.load('images/cloud.png').convert_alpha()
            self.cloud_image = pg.transform.scale(self.cloud_image, 
                                            (self.maze_info['cell_size'], self.maze_info['cell_size']))
        except:
            # Создаем временное изображение, если файл не найден
            self.cloud_image = pg.Surface((self.maze_info['cell_size'], self.maze_info['cell_size']), pg.SRCALPHA)
            self.cloud_image.fill((100, 100, 100, 200))
        
        self.cloud_group = pg.sprite.Group()
        
        # Создаем облака для каждой клетки
        for row in range(self.grid[1]):
            for col in range(self.grid[0]):
                x = self.maze_info['maze_x'] + col * self.maze_info['cell_size'] + self.maze_info['cell_size']//2
                y = self.maze_info['maze_y'] + row * self.maze_info['cell_size'] + self.maze_info['cell_size']//2
                
                # Создаем спрайт облака с правильными параметрами
                cloud = GameSprite(
                    player_image='images/cloud.png',
                    player_x=x,
                    player_y=y,
                    size_x=self.maze_info['cell_size'],
                    size_y=self.maze_info['cell_size']
                )
                # Добавляем свойство видимости
                cloud.visible = True
                self.cloud_group.add(cloud)

    def update_fog_of_war(self):
        """Обновляет видимость облаков в зависимости от позиции игрока"""
        reveal_distance = 150  # Дистанция раскрытия
        
        for cloud in self.cloud_group:
            if hasattr(cloud, 'visible'):
                # Вычисляем расстояние между центрами
                distance = ((cloud.rect.centerx - self.player.rect.centerx)**2 + 
                        (cloud.rect.centery - self.player.rect.centery)**2)**0.5
                cloud.visible = distance > reveal_distance

    def init_sprites(self, start_pos, end_pos):
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

        self.player = Player(
            'images/astronaut.png',
            start_pos[0], start_pos[1],
            30, 35, 0, 0, False, False, 5
        )
        self.player.walls = self.walls
        self.player.bullets = pg.sprite.Group()
        self.player.limit = {
            'EASY': 20, 'MEDIUM': 15,
            'HARD': 10, 'EXPLORE': 15
        }[self.difficulty]

        # self.final = GameSprite(
        #     'images/planet.png',
        #     end_pos[0], end_pos[1],
        #     40, 40, False
        # )


        # self.final = FinalGifSprite(
        #     x=400,
        #     y=300,
        #     gif_path="images/2537512610.gif",
        #     scale=0.5,
        #     rotation_speed=2
        # )
        self.final = FinalGifSprite(end_pos[0], end_pos[1], "images/2537512610.gif", scale=0.17, rotation_speed=1)
        self.all_sprites.add(self.walls, self.player, self.final)

    def get_background(self):
        if self.difficulty == 'EASY':
            return Starfield_white(w=5000, h=900, stars_count=2000)
            # return Backgrounds('images/back.jpg', WIDTH, HEIGHT, 0, 0)
        elif self.difficulty in ('MEDIUM', 'HARD', 'EXPLORE'):
            return Starfield_palette(w=5000, h=900, stars_count=2000)

    def draw_debug_path(self, surface):
        if not self.debug_mode:
            return

        path_pixels = []
        for (row, col) in self.path:
            x = self.maze_info['maze_x'] + col * self.maze_info['cell_size'] + self.maze_info['cell_size']//2
            y = self.maze_info['maze_y'] + row * self.maze_info['cell_size'] + self.maze_info['cell_size']//2
            path_pixels.append((x, y))

        if len(path_pixels) >= 2:
            pg.draw.lines(surface, (255,0,0), False, path_pixels, 3)

    def update(self):
        self.clock = time.Clock()
        delta_time = self.clock.tick(60) / 1000.0
        self.player.update()
        self.player.bullets.update()
        self.enemy_manager.enemies.update()
        # self.final.update(delta_time)
        self.all_sprites.update()
        # self.update_fog_of_war()  # Обновляем видимость облаков

        pg.sprite.groupcollide(self.player.bullets, self.walls, True, False)
        pg.sprite.groupcollide(self.player.bullets, self.enemy_manager.enemies, True, True)

        if pg.sprite.spritecollideany(self.player, self.enemy_manager.enemies):
            self.player.lives -= 1

    def render(self, window):
        if self.difficulty == 'EASY':
            # self.background.reset(window)
            self.background.update(window)
        elif self.difficulty in ('MEDIUM'):
            self.background.update(window)
        elif self.difficulty in ('HARD'):
            self.background.update(window)
        else:
            window.fill((0, 0, 0))

        self.draw_debug_path(window)
        self.enemy_manager.enemies.draw(window)
        self.all_sprites.draw(window)
        self.player.bullets.draw(window)
        
        # # Рисуем только видимые облака
        # for cloud in self.cloud_group:
        #     if hasattr(cloud, 'visible') and cloud.visible:
        #         window.blit(cloud.image, cloud.rect)