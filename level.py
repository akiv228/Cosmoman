import pickle

import pygame as pg
from collections import defaultdict, deque

from pygame import Rect

from maze_generation import generate_maze
from player import Player
from game_classes import Wall, GameSprite, Enemy
from constants import WIDTH, HEIGHT
from grafics_classes import Backgrounds, Fon
from grafics import starfield
import random

from upload_maze import *


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
            # Загружаем данные из файла
            self.maze_info = load_maze(filename)
            gw, gh = self.maze_info['grid_width'], self.maze_info['grid_height']
        else:
            # Генерируем новый лабиринт
            gw, gh = self.grid_sizes[difficulty]
            self.maze_info = generate_maze(gw, gh, difficulty)
            # Сохраняем данные в файл
            save_maze(filename, self.maze_info)

            # Инициализация стен
        self.walls = pg.sprite.Group()
        wall_rects = self.reconstruct_wall_rects()
        for rect in wall_rects:
            self.walls.add(Wall(rect.x, rect.y, rect.width, rect.height))

        # Параметры лабиринта
        # self.maze_info = maze_info
        self.grid = (gw, gh)
        self.path = []

        # Поиск стартовой и конечной позиций
        start_pos, final_pos = self.calculate_positions()
        self.init_sprites(start_pos, final_pos)

        # Фон
        self.background = self.get_background()

        # self.enemies = pg.sprite.Group()

    def calculate_positions(self):
        """Вычисляет позиции с учетом смещения и находит путь"""
        gw, gh = self.grid
        cs = self.maze_info['cell_size']
        graph = self.build_graph()

        # Находим максимальный путь между углами
        corners = [(0,0), (0,gw-1), (gh-1,0), (gh-1,gw-1)]
        max_dist = 0
        best_pair = (corners[0], corners[1])

        for start in corners:
            distances = self.bfs(graph, start)
            for end in corners:
                if distances.get(end, 0) > max_dist:
                    max_dist = distances[end]
                    best_pair = (start, end)

        # Сохраняем путь для отладки
        if self.debug_mode:
            self.path = self.reconstruct_path(graph, *best_pair)

        # Корректируем позиции
        start_pos = self.adjust_position(*best_pair[0])
        end_pos = self.adjust_position(*best_pair[1])
        return start_pos, end_pos

    def build_graph(self):
        """Строит граф соединений лабиринта"""
        graph = defaultdict(list)
        for wall in self.maze_info['removed_walls']:
            r, c = wall[1], wall[2]
            if wall[0] == 'h':
                a, b = (r, c), (r+1, c)
            else:
                a, b = (r, c), (r, c+1)
            graph[a].append(b)
            graph[b].append(a)
        return graph

    def bfs(self, graph, start):
        """Поиск в ширину для расчета расстояний"""
        visited = {start: 0}
        q = deque([start])
        while q:
            node = q.popleft()
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited[neighbor] = visited[node] + 1
                    q.append(neighbor)
        return visited

    def reconstruct_path(self, graph, start, end):
        """Восстанавливает кратчайший путь"""
        parent = {start: None}
        q = deque([start])
        while q:
            node = q.popleft()
            if node == end:
                break
            for neighbor in graph.get(node, []):
                if neighbor not in parent:
                    parent[neighbor] = node
                    q.append(neighbor)

        path = []
        current = end
        while current:
            path.append(current)
            current = parent.get(current)
        return path[::-1]

    def adjust_position(self, row, col):
        """корректирует позицию спрайта с учетом толщины стен и размеров спрайта"""
        cs = self.maze_info['cell_size']
        wall_thickness = self.maze_info['wall_thickness']

        # размеры спрайтов (player: 30x35, final: 40x40)
        if (row, col) == (0, 0):  # предполагаем, что игрок в углу (0,0)
            obj_size = max(30, 35)  # максимальный размер игрока
        else:  # конечная цель
            obj_size = max(40, 40)  # размер планеты

        # минимальный отступ: половина размера спрайта + половина толщины стены + буфер
        offset = (obj_size / 2) + (wall_thickness / 2) + 5  # буфер 5 пикселей

        # базовая позиция центра ячейки
        x = self.maze_info['maze_x'] + col * cs + cs // 2
        y = self.maze_info['maze_y'] + row * cs + cs // 2

        # # корректировка для угловых клеток
        # if col == 0:
        #     x = self.maze_info['maze_x'] + offset
        # elif col == self.grid[0] - 1:
        #     x = self.maze_info['maze_x'] + (self.grid[0] - 1) * cs + cs // 2 - offset
        #
        # if row == 0:
        #     y = self.maze_info['maze_y'] + offset
        # elif row == self.grid[1] - 1:
        #     y = self.maze_info['maze_y'] + (self.grid[1] - 1) * cs + cs // 2 - offset

        return (int(x), int(y))


    def init_sprites(self, start_pos, end_pos):
        """Инициализирует игровые объекты"""
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.spawn_enemies()

        # save_maze("maze_data.pkl", self.maze_info)

        # Игрок
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

        # Цель
        self.final = GameSprite(
            'images/planet.png',
            end_pos[0], end_pos[1],
            40, 40, False
        )
        # отладка позиций
        print(f"игрок: центр={self.player.rect.center}, rect={self.player.rect}")
        print(f"цель: центр={self.final.rect.center}, rect={self.final.rect}")
        for wall in self.walls:
            print(f"стена: {wall.rect}")

        self.all_sprites.add(self.walls, self.player, self.final)

    def spawn_enemies(self):
        if not self.path:
            return

        # Параметры врагов в зависимости от сложности
        enemy_config = {
            'EASY': {'count': 7, 'speed': 1},
            'MEDIUM': {'count': 20, 'speed': 2},
            'HARD': {'count': 5, 'speed': 3},
            'EXPLORE': {'count': 4, 'speed': 2}
        }
        cfg = enemy_config[self.difficulty]

        # Разбиваем путь на сегменты
        segments = self.split_path_into_segments()
        valid_segments = [seg for seg in segments if len(seg) >= 2]

        wall_thickness = self.maze_info['wall_thickness']
        for segment in random.sample(valid_segments, min(cfg['count'], len(valid_segments))):
            direction = self.get_segment_direction(segment)
            if not direction:
                continue

            # Рассчитываем границы патрулирования
            maze_x = self.maze_info['maze_x']
            maze_y = self.maze_info['maze_y']
            cell_size = self.maze_info['cell_size']
            start = segment[0]
            end = segment[-1]

            if direction in ('left', 'right'):
                x1 = maze_x + start[1] * cell_size + cell_size // 2 - wall_thickness
                x2 = maze_x + end[1] * cell_size + cell_size // 2 - wall_thickness
                y = maze_y + start[0] * cell_size + cell_size // 2 - wall_thickness
                enemy = Enemy(
                    'images/alien1.png',
                    (x1 + x2) // 2, y,
                    30, 35, cfg['speed'], 'h',
                    min(x1, x2), max(x1, x2)
                )
            else:
                y1 = maze_y + start[0] * cell_size + cell_size // 2 - wall_thickness
                y2 = maze_y + end[0] * cell_size + cell_size // 2 - wall_thickness
                x = maze_x + start[1] * cell_size + cell_size // 2 - wall_thickness
                enemy = Enemy(
                    'images/alien1.png',
                    x, (y1 + y2) // 2,
                    30, 35, cfg['speed'], 'v',
                    min(y1, y2), max(y1, y2)
                )
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def split_path_into_segments(self):
        segments = []
        if len(self.path) < 2:
            return segments

        current_dir = self.get_direction(self.path[0], self.path[1])
        current_segment = [self.path[0]]

        for i in range(1, len(self.path)):
            new_dir = self.get_direction(self.path[i - 1], self.path[i])
            if new_dir == current_dir:
                current_segment.append(self.path[i])
            else:
                segments.append(current_segment)
                current_segment = [self.path[i - 1], self.path[i]]
                current_dir = new_dir

        segments.append(current_segment)
        return segments

    def get_direction(self, p1, p2):
        dx = p2[1] - p1[1]
        dy = p2[0] - p1[0]
        if dx == 1: return 'right'
        if dx == -1: return 'left'
        if dy == 1: return 'down'
        if dy == -1: return 'up'
        return None

    def get_segment_direction(self, segment):
        if len(segment) < 2:
            return None
        return self.get_direction(segment[0], segment[1])

    def get_background(self):
        if self.difficulty == 'EASY':
            return Backgrounds('images/back.jpg', WIDTH, HEIGHT, 0, 0)
        elif self.difficulty == 'MEDIUM':
            return Fon(w=5000, h=900, stars_count=2000)
        return starfield

    def draw_debug_path(self, surface):
        """Отрисовывает путь решения"""
        if not self.debug_mode or not self.path:
            return

        path_pixels = []
        for (row, col) in self.path:
            x = self.maze_info['maze_x'] + col * self.maze_info['cell_size'] + self.maze_info['cell_size']//2
            y = self.maze_info['maze_y'] + row * self.maze_info['cell_size'] + self.maze_info['cell_size']//2
            path_pixels.append((x, y))

        if len(path_pixels) >= 2:
            pg.draw.lines(surface, (255,0,0), False, path_pixels, 3)

    def update(self):
        self.player.update()
        self.player.bullets.update()
        # pg.sprite.groupcollide(self.player.bullets, self.walls, True, False)
        self.enemies.update()  # Обновляем врагов

        # Обработка столкновений
        pg.sprite.groupcollide(self.player.bullets, self.walls, True, False)
        pg.sprite.groupcollide(self.player.bullets, self.enemies, True, True)

        # Проверка столкновения игрока с врагами
        if pg.sprite.spritecollideany(self.player, self.enemies):
        # if pg.sprite.groupcollide(self.player, self.enemies, True, True):
            self.player.lives -= 1

    def render(self, window):
        # Отрисовка фона
        if self.difficulty == 'EASY':
            self.background.reset(window)
        elif self.difficulty == 'MEDIUM':
            self.background.update(window)
        else:
            window.blit(self.background.alpha_surface, (0, 0))
            self.background.run()

        # Отрисовка пути
        self.draw_debug_path(window)

        self.enemies.draw(window)
        # Отрисовка спрайтов
        self.all_sprites.draw(window)
        self.player.bullets.draw(window)

    def reconstruct_wall_rects(self):
        gw = self.maze_info['grid_width']
        gh = self.maze_info['grid_height']
        cs = self.maze_info['cell_size']
        maze_x = self.maze_info['maze_x']
        maze_y = self.maze_info['maze_y']
        wall_thickness = self.maze_info['wall_thickness']

        # Все возможные стены
        all_walls = []
        for row in range(gh):
            for col in range(gw):
                if col < gw - 1:
                    all_walls.append(('v', row, col))  # Вертикальные стены
                if row < gh - 1:
                    all_walls.append(('h', row, col))  # Горизонтальные стены

        # Удаленные стены из maze_info
        removed_walls = self.maze_info['removed_walls']
        present_walls = [wall for wall in all_walls if wall not in removed_walls]

        wall_sprites = []

        # Внешние стены
        wall_sprites.append(Rect(maze_x, maze_y, gw * cs, wall_thickness))  # верх
        wall_sprites.append(Rect(maze_x, maze_y + gh * cs, gw * cs, wall_thickness))  # низ
        wall_sprites.append(Rect(maze_x, maze_y, wall_thickness, gh * cs))  # лево
        wall_sprites.append(Rect(maze_x + gw * cs, maze_y, wall_thickness, gh * cs + wall_thickness))  # право

        # Внутренние стены
        for wall in present_walls:
            if wall[0] == 'h':  # Горизонтальная стена
                x = maze_x + wall[2] * cs
                y = maze_y + (wall[1] + 1) * cs
                wall_sprites.append(Rect(x, y - wall_thickness // 2, cs, wall_thickness))
            else:  # Вертикальная стена
                x = maze_x + (wall[2] + 1) * cs
                y = maze_y + wall[1] * cs
                wall_sprites.append(Rect(x - wall_thickness // 2, y, wall_thickness, cs))

        return wall_sprites