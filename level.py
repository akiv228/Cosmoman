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
import createwalls
import path_utils
from enemy_manager import EnemyManager

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
            self.maze_info = createwalls.load_maze(filename)
            gw, gh = self.maze_info['grid_width'], self.maze_info['grid_height']
        else:
            gw, gh = self.grid_sizes[difficulty]
            self.maze_info = generate_maze(gw, gh, difficulty)
            createwalls.save_maze(filename, self.maze_info)

        self.walls = pg.sprite.Group()
        wall_rects = createwalls.reconstruct_wall_rects(self.maze_info)
        for rect in wall_rects:
            self.walls.add(Wall(rect.x, rect.y, rect.width, rect.height))

        self.grid = (gw, gh)
        self.path = []

        start_pos, final_pos = self.calculate_positions()
        self.init_sprites(start_pos, final_pos)

        self.background = self.get_background()
        self.enemy_manager = EnemyManager(self)
        self.enemy_manager.spawn_enemies()

    def calculate_positions(self):
        gw, gh = self.grid
        cs = self.maze_info['cell_size']
        graph = self.build_graph()

        corners = [(0,0), (0,gw-1), (gh-1,0), (gh-1,gw-1)]
        max_dist = 0
        best_pair = (corners[0], corners[1])

        for start in corners:
            distances = self.bfs(graph, start)
            for end in corners:
                if distances.get(end, 0) > max_dist:
                    max_dist = distances[end]
                    best_pair = (start, end)

        if self.debug_mode:
            self.path = self.reconstruct_path(graph, *best_pair)

        start_pos = self.adjust_position(*best_pair[0])
        end_pos = self.adjust_position(*best_pair[1])
        return start_pos, end_pos

    def build_graph(self):
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
        cs = self.maze_info['cell_size']
        wall_thickness = self.maze_info['wall_thickness']

        if (row, col) == (0, 0):
            obj_size = max(30, 35)
        else:
            obj_size = max(40, 40)

        offset = (obj_size / 2) + (wall_thickness / 2) + 5
        x = self.maze_info['maze_x'] + col * cs + cs // 2
        y = self.maze_info['maze_y'] + row * cs + cs // 2
        return (int(x), int(y))

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

        self.final = GameSprite(
            'images/planet.png',
            end_pos[0], end_pos[1],
            40, 40, False
        )

        self.all_sprites.add(self.walls, self.player, self.final)

    def get_background(self):
        if self.difficulty == 'EASY':
            return Backgrounds('images/back.jpg', WIDTH, HEIGHT, 0, 0)
        elif self.difficulty == 'MEDIUM':
            return Fon(w=5000, h=900, stars_count=2000)
        return starfield

    def draw_debug_path(self, surface):
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
        self.enemy_manager.enemies.update()

        pg.sprite.groupcollide(self.player.bullets, self.walls, True, False)
        pg.sprite.groupcollide(self.player.bullets, self.enemy_manager.enemies, True, True)

        if pg.sprite.spritecollideany(self.player, self.enemy_manager.enemies):
            self.player.lives -= 1

    def render(self, window):
        if self.difficulty == 'EASY':
            self.background.reset(window)
        elif self.difficulty == 'MEDIUM':
            self.background.update(window)
        else:
            window.blit(self.background.alpha_surface, (0, 0))
            self.background.run()

        self.draw_debug_path(window)
        self.enemy_manager.enemies.draw(window)
        self.all_sprites.draw(window)
        self.player.bullets.draw(window)