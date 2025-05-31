import pygame as pg
import random
import noise
import numpy as np

from fogofwar import FogOfWar
from maze_generation import generate_maze
from grafics.maze_fons import Starfield_white, Starfield_palette
from grafics.circle_hardbackground import CircleBackground
from grafics.motherboards import MotherboardBackground
from game_sprites import Wall, GameSprite
from enemy_manager import EnemyManager
from planet import FinalGifSprite
from player import Player
from sprite_config import SPRITE_SETS, planets, all_smoke_images
from states.config_state import used_explore_finals
import createwalls
import path_utils
import upload_maze

class Level:
    @staticmethod
    def get_explore_size2(min_cell_size=50, screen_width=1100, screen_height=800):
        base_width = random.randint(17, 19)
        base_height = random.randint(12, 14)

        width = base_width + random.randint(-1, 2)
        height = base_height + random.randint(-1, 1)

        ratio = width / height
        if ratio < 1.2:
            width = int(height * 1.3)
        elif ratio > 1.5:
            height = int(width / 1.4)

        cell_w = screen_width / width
        cell_h = screen_height / height
        if cell_w < min_cell_size or cell_h < min_cell_size:
            return 18, 14

        return width, height


    def __init__(self, difficulty, clock=None, debug_mode=True, load_from_file=False, filename="maze_data.pkl"):
        self.debug_mode = debug_mode
        self.clock = clock
        self.current_alpha = 255
        self.difficulty = difficulty
        self.sprite_set = SPRITE_SETS[difficulty]
        self.grid_sizes = {
            'EASY': (14, 11),
            'MEDIUM': (16, 12),
            'HARD': (18, 12),
            # 'EXPLORE': Level.get_explore_size(min_cell_size=35)
            'EXPLORE': Level.get_explore_size2()
        }

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
        self.cell_size = self.maze_info['cell_size']
        self.maze_x = self.maze_info['maze_x']
        self.maze_y = self.maze_info['maze_y']

        # Загрузка спрайтов из конфигурации
        start_pos, final_pos, self.path = path_utils.calculate_positions(self.maze_info, self.grid, self.debug_mode)
        self.init_sprites(start_pos, final_pos)
        self.background = self.get_background()
        self.enemy_manager = EnemyManager(self)
        self.enemy_manager.spawn_enemies()

        # # Инициализация системы "тумана войны"
        # self.init_fog_of_war()

        self.visibility_grid = [
            [False for _ in range(self.grid_width)]
            for _ in range(self.grid_height)
        ]
        # Помечаем стартовую клетку как открытую
        start_cell_row = (start_pos[1] - self.maze_y) // self.cell_size
        start_cell_col = (start_pos[0] - self.maze_x) // self.cell_size
        self.visibility_grid[start_cell_row][start_cell_col] = True

        # base_cloud_image = pg.image.load('images/smoke4.png').convert_alpha()
        # base_cloud_image = pg.image.load(fog_images[difficulty]).convert_alpha()
        base_cloud_image_path = random.choice(all_smoke_images[difficulty])
        base_cloud_image = pg.image.load(base_cloud_image_path).convert_alpha()

        # 7) Создаём объект FogOfWar
        self.fog = FogOfWar(
            maze_x=self.maze_x,
            maze_y=self.maze_y,
            grid_width=self.grid_width,
            grid_height=self.grid_height,
            cell_size=self.cell_size,
            base_cloud_image=base_cloud_image
        )

        self.fog_delay = 0.2  # 1.5 секунды задержки
        self.fog_delay_timer = 0.0
        self.fog_ready = False  # Флаг готовности тумана
        self.fog_delay_font = pg.font.SysFont('Arial', 30)  # Шрифт для сообщения

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

        if self.difficulty == 'EXPLORE':
            final_image = self.select_explore_final()
            if final_image:
                final_data = final_image
                final_image = final_data['image']
                width = 50
                height = 50
            else:
                final_image = 'images/planets/23.gif'  # Запасной вариант
                width = 50
                height = 50
        else:
            final_config = self.sprite_set['final']
            if isinstance(final_config, dict):
                final_image = final_config['image']
                width = final_config.get('width', 50)
                height = final_config.get('height', 50)
            else:
                final_image = final_config

        if final_image.endswith('.gif'):
            if self.difficulty == 'EXPLORE':
                self.final = FinalGifSprite(end_pos[0], end_pos[1], final_image, scale=0.15, rotation_speed=1)
            else:
                self.final = FinalGifSprite(end_pos[0], end_pos[1], final_image, scale=0.17, rotation_speed=1)

        else:
            self.final = GameSprite(final_image, end_pos[0], end_pos[1], width, height)
        self.all_sprites.add(self.walls, self.player, self.final)


    def select_explore_final(self):
        available_planets = [
            planet for planet in planets.values()
            if not planet['discovered'] and planet['image'] not in used_explore_finals
        ]
        if not available_planets:
            return None
        selected_planet = random.choice(available_planets)
        used_explore_finals.add(selected_planet['image'])

        return selected_planet


    def update(self):
        if not self.fog_ready:
            self.fog_delay_timer += self.clock.get_time() / 1000.0

            # Плавное уменьшение прозрачности
            progress = min(1.0, self.fog_delay_timer / self.fog_delay)
            self.current_alpha = int(255 * (1 - progress))  # От 255 до 0

            if self.fog_delay_timer >= self.fog_delay:
                self.fog_ready = True
                self.current_alpha = 0  # Полностью прозрачный


        self.player.update()
        self.player.bullets.update()
        self.enemy_manager.enemies.update()
        self.all_sprites.update()
        # self.update_fog_of_war()  # Обновляем видимость облаков

        pg.sprite.groupcollide(self.player.bullets, self.walls, True, False)
        pg.sprite.groupcollide(self.player.bullets, self.enemy_manager.enemies, True, True)

        if pg.sprite.spritecollideany(self.player, self.enemy_manager.enemies):
            self.player.lives -= 1


        # 1) Сначала вычисляем, какие клетки находятся в зоне видимости:
        #    (игрок находится в центре некоторого круга радиусом reveal_radius_cells * cell_size)
        player_x, player_y = self.player.rect.center
        player_cell_col = (player_x - self.maze_x) // self.cell_size
        player_cell_row = (player_y - self.maze_y) // self.cell_size

        # Задаём радиус видимости в клетках (например, 2 клетки вокруг игрока):
        r_cells = 2
        # Создаём локальный массив для обновлённого состояния (каждый кадр новый):
        new_visibility = [
            [False for _ in range(self.grid_width)]
            for _ in range(self.grid_height)
        ]

        # Помечаем все клетки, которые лежат в радиусе r_cells
        for dr in range(-r_cells, r_cells + 1):
            for dc in range(-r_cells, r_cells + 1):
                rr = player_cell_row + dr
                cc = player_cell_col + dc
                if 0 <= rr < self.grid_height and 0 <= cc < self.grid_width:
                    # проверим, находится ли клетка именно в круге (по центрам)
                    cell_center_x = self.maze_x + cc * self.cell_size + self.cell_size // 2
                    cell_center_y = self.maze_y + rr * self.cell_size + self.cell_size // 2
                    dist = ((cell_center_x - player_x) ** 2 + (cell_center_y - player_y) ** 2) ** 0.5
                    if dist <= r_cells * self.cell_size:
                        new_visibility[rr][cc] = True

        # 2) Обновляем FogOfWar именно этим новым состоянием:
        self.fog.update(new_visibility)

    def get_background(self):
        if self.difficulty == 'EASY':
            return Starfield_white(w=5000, h=900, stars_count=2000)
            # return Backgrounds('images/back.jpg', WIDTH, HEIGHT, 0, 0)
        if self.difficulty == 'MEDIUM':
            return MotherboardBackground(w=5000, h=900)
        if self.difficulty == 'HARD':
            return CircleBackground(w=1100, h=800, circles_count=200)
        elif self.difficulty in ('EXPLORE'):
            return Starfield_palette(w=5000, h=900, stars_count=2000)


    def render(self, window):
        if self.difficulty == 'EASY':
            self.background.update(window)
        elif self.difficulty in ('MEDIUM'):
            self.background.render(window)
        elif self.difficulty in ('HARD'):
            # window.fill((0, 0, 0))
            self.background.reset(window)
        elif self.difficulty in ('EXPLORE'):
            self.background.update(window)
        else:
            window.fill((0, 0, 0))

        self.draw_debug_path(window)
        self.enemy_manager.enemies.draw(window)
        self.all_sprites.draw(window)
        self.player.bullets.draw(window)

        player_center = (self.player.rect.centerx, self.player.rect.centery)
        reveal_radius = self.cell_size * 2   # здесь вы можете настроить любой радиус (в клетках * cell_size)
        self.fog.render(window, player_center, reveal_radius)
        if not self.fog_ready:
            # Создаем поверхность для затемнения
            overlay = pg.Surface(window.get_size(), pg.SRCALPHA)
            overlay.fill((0, 0, 0, self.current_alpha))
            window.blit(overlay, (0, 0))


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
