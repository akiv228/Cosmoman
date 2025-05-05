import platform

import pygame as pg
import random
from pygame import sprite, Surface, Rect

# Updated Wall class to include type, row, and col
class Wall(sprite.Sprite):
    def __init__(self, x, y, width, height, wall_type=None, row=None, col=None):
        super().__init__()
        self.image = Surface([width, height])
        self.image.fill((200, 200, 200))  # LIGHT_GREY, adjust as needed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = wall_type  # 'h' for horizontal, 'v' for vertical, None for outer walls
        self.row = row
        self.col = col

# Updated reconstruct_wall_rects to return wall data with type, row, and col
def reconstruct_wall_rects(maze_info):
    gw = maze_info['grid_width']
    gh = maze_info['grid_height']
    cs = maze_info['cell_size']
    maze_x = maze_info['maze_x']
    maze_y = maze_info['maze_y']
    wall_thickness = maze_info['wall_thickness']
    present_walls = maze_info['present_walls']

    wall_data = []
    # Outer boundaries (no type, row, or col needed for navigation logic)
    wall_data.append((Rect(maze_x, maze_y, gw * cs, wall_thickness), None, None, None))  # Top
    wall_data.append((Rect(maze_x, maze_y + gh * cs, gw * cs, wall_thickness), None, None, None))  # Bottom
    wall_data.append((Rect(maze_x, maze_y, wall_thickness, gh * cs), None, None, None))  # Left
    wall_data.append((Rect(maze_x + gw * cs, maze_y, wall_thickness, gh * cs + wall_thickness), None, None, None))  # Right

    # Inner walls with type, row, and col
    for wall in present_walls:
        if wall[0] == 'h':  # Horizontal wall
            x = maze_x + wall[2] * cs
            y = maze_y + (wall[1] + 1) * cs
            rect = Rect(x, y - wall_thickness // 2, cs, wall_thickness)
            wall_data.append((rect, 'h', wall[1], wall[2]))
        else:  # Vertical wall ('v')
            x = maze_x + (wall[2] + 1) * cs
            y = maze_y + wall[1] * cs
            rect = Rect(x - wall_thickness // 2, y, wall_thickness, cs)
            wall_data.append((rect, 'v', wall[1], wall[2]))

    return wall_data

# Example Level class snippet to create walls
class Level:
    def __init__(self, maze_info):
        self.maze_info = maze_info
        self.walls = pg.sprite.Group()
        wall_data = reconstruct_wall_rects(self.maze_info)
        for rect, wall_type, row, col in wall_data:
            self.walls.add(Wall(rect.x, rect.y, rect.width, rect.height, wall_type, row, col))

# Enemy class with behavior differentiation
class Enemy(sprite.Sprite):
    def __init__(self, maze_info, image_path, x, y, width, height, speed, direction, behavior, walls):
        super().__init__()
        self.maze_info = maze_info
        self.image = pg.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = direction
        self.behavior = behavior  # 'left_hand' or 'bfs'
        self.walls = walls
        self.bfs_path = []  # Placeholder for BFS path, populated elsewhere if needed

    def get_current_cell(self):
        cs = self.maze_info['cell_size']
        maze_x = self.maze_info['maze_x']
        maze_y = self.maze_info['maze_y']
        x = (self.rect.centerx - maze_x) // cs
        y = (self.rect.centery - maze_y) // cs
        return (y, x)

    def check_wall(self, direction, y, x):
        for wall in self.walls:
            if wall.type is None:  # Skip outer walls
                continue
            if direction == 'north' and wall.type == 'h' and wall.row == y - 1 and wall.col == x:
                return True
            elif direction == 'south' and wall.type == 'h' and wall.row == y and wall.col == x:
                return True
            elif direction == 'east' and wall.type == 'v' and wall.row == y and wall.col == x:
                return True
            elif direction == 'west' and wall.type == 'v' and wall.row == y and wall.col == x - 1:
                return True
        return False

    def move(self):
        old_x, old_y = self.rect.x, self.rect.y
        if self.direction == 'north':
            self.rect.y -= self.speed
        elif self.direction == 'south':
            self.rect.y += self.speed
        elif self.direction == 'east':
            self.rect.x += self.speed
        elif self.direction == 'west':
            self.rect.x -= self.speed
        # Check collision with walls
        if pg.sprite.spritecollide(self, self.walls, False):
            self.rect.x, self.rect.y = old_x, old_y
            return False
        return True

    def update(self):
        if self.behavior == 'left_hand':
            y, x = self.get_current_cell()
            # Left-hand rule: try left, then forward, then right
            directions = ['north', 'east', 'south', 'west']
            current_idx = directions.index(self.direction)
            left_idx = (current_idx - 1) % 4
            right_idx = (current_idx + 1) % 4
            left_dir = directions[left_idx]
            right_dir = directions[right_idx]

            if not self.check_wall(left_dir, y, x):
                self.direction = left_dir
                self.move()
            elif not self.check_wall(self.direction, y, x):
                self.move()
            elif not self.check_wall(right_dir, y, x):
                self.direction = right_dir
                self.move()
            else:
                self.direction = directions[(current_idx + 2) % 4]  # Turn around
                self.move()
        elif self.behavior == 'bfs':
            # BFS path following logic (assuming bfs_path is set)
            if self.bfs_path:
                next_cell = self.bfs_path.pop(0)
                # Move towards next_cell (simplified, adjust as needed)
                self.rect.x = self.maze_info['maze_x'] + next_cell[1] * self.maze_info['cell_size']
                self.rect.y = self.maze_info['maze_y'] + next_cell[0] * self.maze_info['cell_size']

# EnemyManager to handle spawning and behavior split
class EnemyManager:
    def __init__(self, maze_info, level):
        self.maze_info = maze_info
        self.level = level
        self.enemies = pg.sprite.Group()

    def spawn_enemies(self, num_enemies, spawn_positions):
        for i in range(num_enemies):
            x, y = spawn_positions[i]  # Assume spawn_positions is a list of (x, y)
            direction = random.choice(['north', 'east', 'south', 'west'])
            # 40% chance for left-hand rule, 60% for BFS
            behavior = 'left_hand' if random.random() < 0.4 else 'bfs'
            enemy = Enemy(self.maze_info, 'images/alien1.png', x, y, 30, 35, 2, direction, behavior, self.level.walls)
            # Ensure no overlap by checking collisions
            while pg.sprite.spritecollide(enemy, self.enemies, False):
                enemy.rect.x += self.maze_info['cell_size']
                if enemy.rect.x >= self.maze_info['maze_x'] + self.maze_info['grid_width'] * self.maze_info['cell_size']:
                    enemy.rect.x = self.maze_info['maze_x']
                    enemy.rect.y += self.maze_info['cell_size']
            self.enemies.add(enemy)

    def update(self):
        self.enemies.update()

# Example usage (simplified)
if platform.system() == "Emscripten":
    import asyncio
    FPS = 60

    async def main():
        pg.init()
        maze_info = {'grid_width': 10, 'grid_height': 10, 'cell_size': 32, 'maze_x': 0, 'maze_y': 0, 'wall_thickness': 4, 'present_walls': [('h', 1, 1), ('v', 2, 2)]}
        level = Level(maze_info)
        enemy_manager = EnemyManager(maze_info, level)
        enemy_manager.spawn_enemies(5, [(32, 32), (64, 64), (96, 96), (128, 128), (160, 160)])
        while True:
            enemy_manager.update()
            await asyncio.sleep(1.0 / FPS)

    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        pg.init()
        maze_info = {'grid_width': 10, 'grid_height': 10, 'cell_size': 32, 'maze_x': 0, 'maze_y': 0, 'wall_thickness': 4, 'present_walls': [('h', 1, 1), ('v', 2, 2)]}
        level = Level(maze_info)
        enemy_manager = EnemyManager(maze_info, level)
        enemy_manager.spawn_enemies(5, [(32, 32), (64, 64), (96, 96), (128, 128), (160, 160)])
        # Simple game loop for non-Emscripten
        running = True
        clock = pg.time.Clock()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            enemy_manager.update()
            clock.tick(60)
        pg.quit()