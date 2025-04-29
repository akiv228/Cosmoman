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
        wall_rects, maze_info = generate_maze(gw, gh, difficulty)  # Изменено
        self.walls = pg.sprite.Group()
        for rect in wall_rects:
            self.walls.add(Wall(rect.x, rect.y, rect.width, rect.height))

        # Извлекаем информацию о лабиринте
        self.removed_walls = maze_info['removed_walls']
        self.grid_width = gw
        self.grid_height = gh
        self.cell_size = maze_info['cell_size']
        self.maze_x = maze_info['maze_x']
        self.maze_y = maze_info['maze_y']

        # Находим стартовую и конечную позиции
        start_pos, final_pos = self.find_farthest_cells()
        self.all_sprites, self.player, self.final = self.place_objects(start_pos, final_pos)
        self.background = self.get_background()

    def find_farthest_cells(self):
        from collections import defaultdict, deque

        # Строим граф смежности
        graph = defaultdict(list)
        for wall in self.removed_walls:
            row, col = wall[1], wall[2]
            if wall[0] == 'h':
                cell_a = (row, col)
                cell_b = (row + 1, col)
            elif wall[0] == 'v':
                cell_a = (row, col)
                cell_b = (row, col + 1)
            graph[cell_a].append(cell_b)
            graph[cell_b].append(cell_a)

        # BFS для поиска самых удалённых точек
        def bfs(start):
            visited = {start: 0}
            q = deque([(start, 0)])
            max_dist = 0
            far_node = start
            while q:
                node, dist = q.popleft()
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        visited[neighbor] = dist + 1
                        q.append((neighbor, dist + 1))
                        if dist + 1 > max_dist:
                            max_dist = dist + 1
                            far_node = neighbor
            return far_node, visited

        # Первый BFS для поиска крайней точки
        start_node = (0, 0)
        far_node, _ = bfs(start_node)
        # Второй BFS для поиска диаметра
        final_node, dist_map = bfs(far_node)

        # Конвертируем клетки в экранные координаты
        def to_pixels(row, col):
            x = self.maze_x + col * self.cell_size + self.cell_size // 2
            y = self.maze_y + row * self.cell_size + self.cell_size // 2
            return (x, y)

        return to_pixels(*far_node), to_pixels(*final_node)

    def place_objects(self, start_pos, final_pos):
        all_sprites = pg.sprite.Group()

        player = Player('images\\astronaut.png', start_pos[0], start_pos[1], 30, 35, 0, 0, False, False, 3)
        final = GameSprite('images\\planet.png', final_pos[0], final_pos[1], 40, 40, False)

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