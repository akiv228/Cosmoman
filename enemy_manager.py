import pygame as pg
import random
from game_sprites import Enemy
import path_utils
from sprite_config import SPRITE_SETS
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger('EnemyManager')


class EnemyManager:
    def __init__(self, level):
        self.level = level
        self.enemies = pg.sprite.Group()
        self.enemy_configs = SPRITE_SETS[level.difficulty]['enemies']

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
            logger.warning("Path too short for enemies")
            return

        # Конфигурация в зависимости от сложности
        cfg = {
            'EASY': {'count_factor': 0.05, 'speed': 1},
            'MEDIUM': {'count_factor': 0.04, 'speed': 2},
            'HARD': {'count_factor': 0.07, 'speed': 2},
            'EXPLORE': {'count_factor': 0.05, 'speed': 2}
        }[self.level.difficulty]

        # Расстояние между врагами
        enemy_spacing = self.level.maze_info['cell_size'] * {
            'EASY': 1.5,
            'MEDIUM': 2,
            'HARD': 2.0,
            'EXPLORE': 2.0
        }[self.level.difficulty]

        # Расчет количества врагов
        cell_count = self.level.grid_width * self.level.grid_height
        planned_enemy_count = round(cell_count * cfg['count_factor'])
        logger.info(f"Planned enemies: {planned_enemy_count} (based on {cell_count} cells)")

        # Разделение пути на сегменты
        segments = path_utils.split_path_into_segments(self.level.path)
        logger.info(f"Total segments: {len(segments)}")

        # Фильтрация сегментов
        valid_segments = [
            seg for seg in segments
            if len(seg) >= 2 and not self.is_near_start_end(seg)
        ]
        logger.info(f"Valid segments (length>=2, not near start/end): {len(valid_segments)}")

        used_segments = []
        created_enemies = 0
        failed_placement = 0

        # Попытки размещения врагов
        for _ in range(planned_enemy_count):
            if not valid_segments:
                logger.warning("No valid segments left")
                break

            # Фильтрация доступных сегментов
            available_segments = self.filter(valid_segments, used_segments, enemy_spacing)
            if not available_segments:
                logger.warning("No available segments after filtering")
                break

            # Выбор наиболее удаленного сегмента
            segment = self.choose_distant_segment(available_segments, enemy_spacing)
            if not segment:
                logger.debug("No distant segment found")
                failed_placement += 1
                continue

            # Создание врага
            enemy = self.create_enemy_for_segment(segment, cfg['speed'])
            if not enemy:
                logger.error("Failed to create enemy")
                continue

            # Проверка коллизий
            if self.check_enemy_collisions(enemy, enemy_spacing):
                logger.debug("Enemy collision detected")
                failed_placement += 1
                continue

            # Успешное размещение
            self.level.all_sprites.add(enemy)
            self.enemies.add(enemy)
            used_segments.append(segment)
            valid_segments.remove(segment)
            created_enemies += 1

        # Логирование результатов
        logger.info(f"Created enemies: {created_enemies}/{planned_enemy_count}")
        if created_enemies < planned_enemy_count:
            reason = "Reasons: "
            if created_enemies + failed_placement < planned_enemy_count:
                reason += "Not enough valid segments, "
            if failed_placement > 0:
                reason += f"{failed_placement} failed placements (collisions/distance), "
            reason += f"Valid segments left: {len(valid_segments)}"
            logger.warning(reason)

    # Остальные методы без изменений (is_near_start_end, create_enemy_for_segment, и т.д.)

    def is_near_start_end(self, segment):
        start_node = segment[0]
        end_node = segment[-1]
        start_pos = self.level.path[0]
        final_pos = self.level.path[-1]
        start_dist = abs(start_node[0] - start_pos[0]) + abs(start_node[1] - start_pos[1])
        end_dist = abs(end_node[0] - final_pos[0]) + abs(end_node[1] - final_pos[1])
        return start_dist < 3 or end_dist < 3

    def create_enemy_for_segment(self, segment, speed):
        maze_x = self.level.maze_info['maze_x']
        maze_y = self.level.maze_info['maze_y']
        cell_size = self.level.maze_info['cell_size']
        wall_thickness = self.level.maze_info['wall_thickness']
        direction = path_utils.get_segment_direction(segment)
        start = segment[0]
        end = segment[-1]

        # Выбор конфигурации врага
        enemy_config = random.choice(self.enemy_configs)
        image_path = enemy_config['image']
        width = enemy_config['width']
        height = enemy_config['height']

        if direction == 'right':
            x1 = maze_x + start[1] * cell_size + wall_thickness + 5
            x2 = maze_x + end[1] * cell_size - wall_thickness - 5
            y = maze_y + start[0] * cell_size + cell_size // 2
            return Enemy(image_path, (x1 + x2) // 2, y, width, height,
                         speed, 'h', x1, x2, self.level.walls)
        # Аналогично для других направлений ('left', 'down', 'up')
        elif direction == 'left':
            x1 = maze_x + start[1] * cell_size + wall_thickness + 5
            x2 = maze_x + end[1] * cell_size - wall_thickness - 5
            y = maze_y + start[0] * cell_size + cell_size // 2
            return Enemy(image_path, (x1 + x2) // 2, y, width, height,
                         speed, 'h', x2, x1, self.level.walls)
        elif direction == 'down':
            y1 = maze_y + start[0] * cell_size + wall_thickness + 5
            y2 = maze_y + end[0] * cell_size - wall_thickness - 5
            x = maze_x + start[1] * cell_size + cell_size // 2
            return Enemy(image_path, x, (y1 + y2) // 2, width, height,
                         speed, 'v', y1, y2, self.level.walls)
        elif direction == 'up':
            y1 = maze_y + start[0] * cell_size + wall_thickness + 5
            y2 = maze_y + end[0] * cell_size - wall_thickness - 5
            x = maze_x + start[1] * cell_size + cell_size // 2
            return Enemy(image_path, x, (y1 + y2) // 2, width, height,
                         speed, 'v', y2, y1, self.level.walls)

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
            return random.choice(segments)

        best_segment = None
        best_score = -1

        for _ in range(3):
            segment = random.choice(segments)
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
