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

    def draw_path(self, window, path):
        if not path:
            return
        for i in range(len(path) - 1):
            start = path[i]
            end = path[i + 1]
            pg.draw.line(window, (255, 0, 0), start, end, 3)

    # Модифицируем метод find_farthest_cells
    def find_farthest_cells(self):
        from collections import defaultdict, deque

        # Строим граф смежности клеток
        graph = defaultdict(list)
        for wall in self.removed_walls:
            row, col = wall[1], wall[2]
            if wall[0] == 'h':
                cell_a = (row, col)
                cell_b = (row + 1, col)
            else:
                cell_a = (row, col)
                cell_b = (row, col + 1)
            graph[cell_a].append(cell_b)
            graph[cell_b].append(cell_a)

        # Выбираем стартовые точки из угловых клеток
        corners = [
            (0, 0),
            (0, self.grid_width - 1),
            (self.grid_height - 1, 0)
            (self.grid_height - 1, self.grid_width - 1)
        ]

        # Находим самую удаленную пару углов
        max_distance = 0
        best_pair = None
        for start in corners:
            q = deque([(start, 0)])
            visited = {}
            while q:
                node, dist = q.popleft()
                if node in visited:
                    continue
                visited[node] = dist
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        q.append((neighbor, dist + 1))

            for end in corners:
                if end in visited and visited[end] > max_distance:
                    max_distance = visited[end]
                    best_pair = (start, end)
                    self.path = self.reconstruct_path(graph, start, end)

        # Конвертация координат с учетом размеров спрайтов
        def adjust_position(row, col):
            x = self.maze_x + col * self.cell_size + self.cell_size // 2
            y = self.maze_y + row * self.cell_size + self.cell_size // 2

            # Сдвигаем от стен (примерно 10% от размера клетки)
            offset = self.cell_size * 0.01
            if col == 0:
                x += offset
            elif col == self.grid_width - 1:
                x -= offset
            if row == 0:
                y += offset
            elif row == self.grid_height - 1:
                y -= offset

            return (int(x), int(y))

        start_pixels = adjust_position(*best_pair[0])
        final_pixels = adjust_position(*best_pair[1])

        return start_pixels, final_pixels

    def reconstruct_path(self, graph, start, end):
        # BFS для восстановления пути
        from collections import deque
        parent = {}
        q = deque([start])
        parent[start] = None

        while q:
            node = q.popleft()
            if node == end:
                break
            for neighbor in graph[node]:
                if neighbor not in parent:
                    parent[neighbor] = node
                    q.append(neighbor)

        # Восстановление пути
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent[current]
        return path[::-1]


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

        # Отрисовка пути (временно)
        path_pixels = []
        for (row, col) in self.path:
            x = self.maze_x + col * self.cell_size + self.cell_size // 2
            y = self.maze_y + row * self.cell_size + self.cell_size // 2
            path_pixels.append((x, y))
        self.draw_path(window, path_pixels)


        self.all_sprites.draw(window)
        self.player.bullets.draw(window)