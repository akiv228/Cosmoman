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
from sprite_config import SPRITE_SETS
from states.config_state import used_explore_finals
from test_gradient_for_labirints import Fon2_2

class Level:
    @staticmethod
    def get_explore_size(min_cell_size=40, screen_width=1100, screen_height=800, max_attempts=10):
        max_cols = screen_width // min_cell_size
        max_rows = screen_height // min_cell_size
        default_size = (18, 12)  # Размер по умолчанию

        for _ in range(max_attempts):
            cols = random.randint(12, max_cols)
            rows = random.randint(8, max_rows)

            if (cols <= max_cols and
                    rows <= max_rows and
                    cols / rows >= 1.0 and
                    cols * rows <= 330):
                return cols, rows

        print(
            f"Не удалось сгенерировать размер за {max_attempts} попыток. Используется размер по умолчанию {default_size}")
        return default_size

    def __init__(self, difficulty, debug_mode=True, load_from_file=False, filename="maze_data.pkl"):
        self.difficulty = difficulty
        self.sprite_set = SPRITE_SETS[difficulty]
        self.debug_mode = debug_mode
        self.grid_sizes = {
            # 'EASY': (16, 12),
            # 'MEDIUM': (16, 12),
            # 'HARD': (20, 15),
            # 'EXPLORE': (random.randint(18, 22), random.randint(13, 17))
            # 'EASY': (12, 9),
            'EASY': (14, 11),
            'MEDIUM': (16, 12),
            # 'MEDIUM': (24, 18),
            # 'HARD': (24, 15),
            # 'HARD': (19, 15),
            'HARD': (18, 12),
            # 'EXPLORE': (random.randint(18, 22), random.randint(13, 17))
            # 'EXPLORE': Level.get_explore_size(min_cell_size=35)
            'EXPLORE': Level.get_explore_size2()
        }
        # Ширина: 22 Высота: 15
        # Ширина: 20 Высота: 13
        # (18, 11) (15, 14) (22, 13) (19, 14), (19, 12)
        explore_size = self.grid_sizes['EXPLORE']
        print("Ширина:", explore_size[0], "Высота:", explore_size[1])

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
        self.grid_width = self.maze_info['grid_width']
        self.grid_height = self.maze_info['grid_height']

        # Загрузка спрайтов из конфигурации
        start_pos, final_pos, self.path = path_utils.calculate_positions(self.maze_info, self.grid, self.debug_mode)
        self.init_sprites(start_pos, final_pos)

        # Инициализация системы "тумана войны"
        # self.init_fog_of_war()
        
        self.background = self.get_background()
        self.enemy_manager = EnemyManager(self)
        self.enemy_manager.spawn_enemies()

    @staticmethod
    def get_explore_size2():
        while True:
            width = random.randint(16, 21)
            height = random.randint(12, 16)

            # Проверяем пропорции (ширина должна быть заметно больше высоты)
            if width / height >= 1.25:  # Соотношение не менее 5:4
                return width, height

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

        player_size = self.sprite_set['player_size']
        self.player = Player(
            self.sprite_set['player'],
            start_pos[0], start_pos[1],
            player_size[0], player_size[1],
            0, 0, False, False, 5
        )
        self.player.walls = self.walls
        self.player.bullets = pg.sprite.Group()
        self.player.limit = {
            'EASY': 20, 'MEDIUM': 15,
            'HARD': 10, 'EXPLORE': 15
        }[self.difficulty]



        # Выбор финального спрайта
        if self.difficulty == 'EXPLORE':
            final_image = self.select_explore_final()  # Returns a string (path)
        else:
            final_config = self.sprite_set['final']
            if isinstance(final_config, dict):
                final_image = final_config['image']
                width = final_config.get('width', 50)  # Default size if not specified
                height = final_config.get('height', 50)
            else:
                final_image = final_config
                width = 50
                height = 50

        # Проверка формата файла
        if final_image.endswith('.gif'):
            if self.difficulty == 'EXPLORE':
                self.final = FinalGifSprite(end_pos[0], end_pos[1], final_image, scale=0.15, rotation_speed=1)
            else:
                self.final = FinalGifSprite(end_pos[0], end_pos[1], final_image, scale=0.17, rotation_speed=1)

        else:
            self.final = GameSprite(final_image, end_pos[0], end_pos[1], width, height)
        self.all_sprites.add(self.walls, self.player, self.final)

    def select_explore_final(self):
        available_finals = [path for key, path in self.sprite_set['finals'].items() if path not in used_explore_finals]
        if not available_finals:  # Если все использованы, сбрасываем
            used_explore_finals.clear()
            available_finals = list(self.sprite_set['finals'].values())
        selected_final = random.choice(available_finals)
        used_explore_finals.add(selected_final)
        return selected_final

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
        # self.clock = time.Clock()
        # delta_time = self.clock.tick(60) / 1000.0
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
            # self.background.update(window)
            window.fill((0, 0, 0))
        elif self.difficulty in ('HARD'):
            # self.background.update(window)
            window.fill((0, 0, 0))
        elif self.difficulty in ('EXPLORE'):
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