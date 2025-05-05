import pygame as pg
from constants import *
from base_sprite import *
from random import *
import path_utils




# Updated Enemy class with behavior parameter
class Enemy(GameSprite):
    def __init__(self, maze_info, image_path, x, y, width, height, speed, direction, board1, board2, walls,
                 behavior='bfs'):
        super().__init__(image_path, x, y, width, height, anime=False)
        self.maze_info = maze_info
        self.speed = speed
        self.direction = direction  # 'north', 'east', 'south', 'west' for left-hand, 'h' or 'v' for BFS
        self.walls = walls
        self.cell_size = maze_info['cell_size']
        self.behavior = behavior
        self.board1 = board1
        self.board2 = board2
        self.moving_forward = True if behavior == 'bfs' else None

    def get_current_cell(self):
        """Returns the current maze cell of the enemy."""
        maze_x, maze_y = self.maze_info['maze_x'], self.maze_info['maze_y']
        grid_x = int((self.rect.x - maze_x) / self.cell_size)
        grid_y = int((self.rect.y - maze_y) / self.cell_size)
        return (grid_y, grid_x)

    def check_wall(self, direction):
        y, x = self.get_current_cell()
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
        """Moves the enemy in the current direction."""
        if self.direction == 'north':
            self.rect.y -= self.speed
        elif self.direction == 'south':
            self.rect.y += self.speed
        elif self.direction == 'east':
            self.rect.x += self.speed
        elif self.direction == 'west':
            self.rect.x -= self.speed
        elif self.direction == 'h':
            self.rect.x += self.speed if self.moving_forward else -self.speed
        elif self.direction == 'v':
            self.rect.y += self.speed if self.moving_forward else -self.speed

    def update(self):
        old_rect = self.rect.copy()

        if self.behavior == 'bfs':
            # BFS movement along predefined segment
            self.move()
            if self.direction == 'h':
                if self.moving_forward and self.rect.x >= self.board2:
                    self.moving_forward = False
                elif not self.moving_forward and self.rect.x <= self.board1:
                    self.moving_forward = True
            elif self.direction == 'v':
                if self.moving_forward and self.rect.y >= self.board2:
                    self.moving_forward = False
                elif not self.moving_forward and self.rect.y <= self.board1:
                    self.moving_forward = True
        elif self.behavior == 'left_hand':
            # Left-hand rule movement
            directions_order = ['north', 'east', 'south', 'west']
            current_idx = directions_order.index(self.direction)
            left_dir = directions_order[(current_idx - 1) % 4]
            forward_dir = self.direction
            right_dir = directions_order[(current_idx + 1) % 4]

            if not self.check_wall(left_dir):
                self.direction = left_dir
            elif not self.check_wall(forward_dir):
                pass
            else:
                self.direction = right_dir
            self.move()

        # Collision handling
        if pg.sprite.spritecollideany(self, self.walls):
            self.rect = old_rect
            if self.behavior == 'bfs':
                self.moving_forward = not self.moving_forward
            elif self.behavior == 'left_hand':
                directions_order = ['north', 'east', 'south', 'west']
                current_idx = directions_order.index(self.direction)
                self.direction = directions_order[(current_idx + 1) % 4]


# Updated EnemyManager class
class EnemyManager:
    def __init__(self, level, maze_info):
        self.level = level
        self.enemies = pg.sprite.Group()
        self.maze_info = maze_info

    def filter(self, segments, used_segments, min_distance):
        non_adjacent = []
        for seg in segments:
            is_adjacent = False
            seg_center = self.segment_center(seg)
            for used_seg in used_segments:
                used_center = self.segment_center(used_seg)
                dx = seg_center[0] - used_center[0]
                dy = seg_center[1] - used_center[1]
                distance_sq = dx * dx + dy * dy
                if distance_sq < (min_distance ** 2):
                    is_adjacent = True
                    break
            if not is_adjacent:
                non_adjacent.append(seg)
        return non_adjacent

    def spawn_enemies(self):
        if not self.level.path or len(self.level.path) < 4:
            return

        cfg = {
            'EASY': {'count': 20, 'speed': 1},
            'MEDIUM': {'count': 15, 'speed': 2},
            'HARD': {'count': 5, 'speed': 3},
            'EXPLORE': {'count': 4, 'speed': 2}
        }[self.level.difficulty]

        segments = path_utils.split_path_into_segments(self.level.path)
        valid_segments = [seg for seg in segments if len(seg) >= 2 and not self.is_near_start_end(seg)]
        enemy_spacing = self.maze_info['cell_size'] * 2
        used_segments = []

        total_enemies = cfg['count']
        left_hand_count = int(total_enemies * 0.4)  # 40% follow left-hand rule
        bfs_count = total_enemies - left_hand_count

        # Spawn BFS enemies
        for _ in range(bfs_count):
            if not valid_segments: break
            available_segments = self.filter(valid_segments, used_segments, enemy_spacing)
            if not available_segments: break
            segment = self.choose_distant_segment(available_segments, enemy_spacing)
            if not segment: continue
            enemy = self.create_enemy_for_segment(segment, cfg['speed'], 'bfs')
            if enemy and not self.check_enemy_collisions(enemy, enemy_spacing):
                self.level.all_sprites.add(enemy)
                self.enemies.add(enemy)
                used_segments.append(segment)
                valid_segments.remove(segment)

        # Spawn left-hand enemies across the maze
        for _ in range(left_hand_count):
            x = self.maze_info['maze_x'] + randint(0, self.maze_info['grid_width'] - 1) * self.maze_info['cell_size'] + \
                self.maze_info['cell_size'] // 2
            y = self.maze_info['maze_y'] + randint(0, self.maze_info['grid_height'] - 1) * self.maze_info['cell_size'] + \
                self.maze_info['cell_size'] // 2
            direction = choice(['north', 'east', 'south', 'west'])
            enemy = Enemy(self.maze_info, 'images/alien1.png', x, y, 30, 35, cfg['speed'], direction, 0, 0,
                          self.level.walls, behavior='left_hand')
            if not self.check_enemy_collisions(enemy, enemy_spacing):
                self.level.all_sprites.add(enemy)
                self.enemies.add(enemy)

    def is_near_start_end(self, segment):
        start_node = segment[0]
        end_node = segment[-1]
        start_pos = self.level.path[0]
        final_pos = self.level.path[-1]
        start_dist = abs(start_node[0] - start_pos[0]) + abs(start_node[1] - start_pos[1])
        end_dist = abs(end_node[0] - final_pos[0]) + abs(end_node[1] - final_pos[1])
        return start_dist < 3 or end_dist < 3

    def create_enemy_for_segment(self, segment, speed, behavior):
        maze_x = self.level.maze_info['maze_x']
        maze_y = self.level.maze_info['maze_y']
        cell_size = self.level.maze_info['cell_size']
        wall_thickness = self.level.maze_info['wall_thickness']
        direction = path_utils.get_segment_direction(segment)
        start = segment[0]
        end = segment[-1]

        if behavior == 'bfs':
            if direction == 'right':
                x1 = maze_x + start[1] * cell_size + wall_thickness + 5
                x2 = maze_x + end[1] * cell_size - wall_thickness - 5
                y = maze_y + start[0] * cell_size + cell_size // 2
                return Enemy(self.maze_info, 'images/alien1.png', (x1 + x2) // 2, y, 30, 35, speed, 'h', x1, x2,
                             self.level.walls, behavior)
            elif direction == 'left':
                x1 = maze_x + start[1] * cell_size + wall_thickness + 5
                x2 = maze_x + end[1] * cell_size - wall_thickness - 5
                y = maze_y + start[0] * cell_size + cell_size // 2
                return Enemy(self.maze_info, 'images/alien2.png', (x1 + x2) // 2, y, 30, 35, speed, 'h', x2, x1,
                             self.level.walls, behavior)
            elif direction == 'down':
                y1 = maze_y + start[0] * cell_size + wall_thickness + 5
                y2 = maze_y + end[0] * cell_size - wall_thickness - 5
                x = maze_x + start[1] * cell_size + cell_size // 2
                return Enemy(self.maze_info, 'images/alien1.png', x, (y1 + y2) // 2, 30, 35, speed, 'v', y1, y2,
                             self.level.walls, behavior)
            elif direction == 'up':
                y1 = maze_y + start[0] * cell_size + wall_thickness + 5
                y2 = maze_y + end[0] * cell_size - wall_thickness - 5
                x = maze_x + start[1] * cell_size + cell_size // 2
                return Enemy(self.maze_info, 'images/alien2.png', x, (y1 + y2) // 2, 30, 35, speed, 'v', y2, y1,
                             self.level.walls, behavior)

    def check_enemy_collisions(self, new_enemy, min_distance):
        for enemy in self.enemies:
            if new_enemy.rect.colliderect(enemy.rect):
                return True
            dx = new_enemy.rect.centerx - enemy.rect.centerx
            dy = new_enemy.rect.centery - enemy.rect.centery
            if (dx * dx + dy * dy) < (min_distance ** 2):
                return True
        return False

    def choose_distant_segment(self, segments, min_distance):
        if not self.enemies:
            return choice(segments)
        best_segment = None
        best_score = -1
        for _ in range(3):
            segment = choice(segments)
            center = self.segment_center(segment)
            min_dist = float('inf')
            for enemy in self.enemies:
                dx = center[0] - enemy.rect.centerx
                dy = center[1] - enemy.rect.centery
                dist = dx * dx + dy * dy
                min_dist = min(min_dist, dist)
            if min_dist > best_score:
                best_score = min_dist
                best_segment = segment
        return best_segment if best_score > (min_distance ** 2) else None

    def segment_center(self, segment):
        first = segment[0]
        last = segment[-1]
        maze_x = self.level.maze_info['maze_x']
        maze_y = self.level.maze_info['maze_y']
        cell_size = self.level.maze_info['cell_size']
        x = (first[1] + last[1]) / 2 * cell_size + maze_x
        y = (first[0] + last[0]) / 2 * cell_size + maze_y
        return (x, y)