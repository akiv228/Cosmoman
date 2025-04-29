import pickle
import random
from pygame import Rect
from constants import WIDTH, HEIGHT


class DSU:
    def __init__(self, size):
        self.parent = list(range(size))

        self.rank = [0] * size  # Добавляем ранги

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            # Объединение по рангу
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                if self.rank[root_x] == self.rank[root_y]:
                    self.rank[root_x] += 1

def generate_maze(grid_width, grid_height, difficulty):
    # Фиксированные размеры окна из constants.py
    cell_size_x = (WIDTH - 40) // grid_width  # 20px padding с каждой стороны
    cell_size_y = (HEIGHT - 100) // grid_height  # 50px сверху и снизу

    # Унифицированный размер ячейки
    cell_size = min(cell_size_x, cell_size_y)

    # Центрирование лабиринта
    maze_x = (WIDTH - grid_width * cell_size) // 2
    maze_y = (HEIGHT - grid_height * cell_size) // 2 + 20

    walls = []
    for row in range(grid_height):
        for col in range(grid_width):
            if col < grid_width - 1:
                # Вес для вертикальных стен
                weight_v = get_wall_weight('v', difficulty)
                walls.append(('v', row, col, weight_v))
            if row < grid_height - 1:
                # Вес для горизонтальных стен
                weight_h = get_wall_weight('h', difficulty)
                walls.append(('h', row, col, weight_h))

    # Сортировка стен по весу (от меньшего к большему)
    walls.sort(key=lambda x: x[3])

    dsu = DSU(grid_width * grid_height)
    removed_walls = set()

    # Kruskal's algorithm
    for wall in walls:
        if wall[0] == 'h':
            cell_a = wall[1] * grid_width + wall[2]
            cell_b = (wall[1] + 1) * grid_width + wall[2]
        else:
            cell_a = wall[1] * grid_width + wall[2]
            cell_b = wall[1] * grid_width + (wall[2] + 1)

        if dsu.find(cell_a) != dsu.find(cell_b):
            dsu.union(cell_a, cell_b)
            removed_walls.add(wall)

    # Настройка количества циклов на основе размера сетки
    grid_size = grid_width * grid_height
    cycles_config = {
        'EASY': int(grid_size * 0.02),    # 2% от размера сетки
        'MEDIUM': int(grid_size * 0.05),
        'HARD': int(grid_size * 0.1),
        'EXPLORE': int(grid_size * 0.2)
    }
    # add_cycles(grid_width, grid_height, dsu, removed_walls, walls, cycles_config[difficulty])

    if not is_maze_connected(dsu):
         print("Ошибка! Лабиринт не связный. Перегенерируйте.")
        # return generate_maze(grid_width, grid_height, difficulty)  # Рекурсивный перезапуск
    if not is_maze_connected2(grid_width, grid_height, removed_walls):
         print("Ошибка! Лабиринт не связный. Перегенерируйте.")

    # Create wall sprites
    wall_sprites = []
    wall_thickness = 4

    # Add outer walls
    wall_sprites.append(Rect(maze_x, maze_y, grid_width * cell_size, wall_thickness))  # top
    wall_sprites.append(
        Rect(maze_x, maze_y + grid_height * cell_size, grid_width * cell_size, wall_thickness))  # bottom
    wall_sprites.append(Rect(maze_x, maze_y, wall_thickness, grid_height * cell_size))  # left
    wall_sprites.append(Rect(maze_x + grid_width * cell_size, maze_y, wall_thickness, grid_height * cell_size + wall_thickness ))  # right

    # Add internal walls
    for wall in walls:
        if wall not in removed_walls:
            if wall[0] == 'h':
                x = maze_x + wall[2] * cell_size
                y = maze_y + (wall[1] + 1) * cell_size
                wall_sprites.append(Rect(x, y - wall_thickness // 2, cell_size, wall_thickness))
            else:
                x = maze_x + (wall[2] + 1) * cell_size
                y = maze_y + wall[1] * cell_size
                wall_sprites.append(Rect(x - wall_thickness // 2, y, wall_thickness, cell_size))

    return wall_sprites, {
        'removed_walls': removed_walls,
        'grid_width': grid_width,
        'grid_height': grid_height,
        'cell_size': cell_size,
        'maze_x': maze_x,
        'maze_y': maze_y,
        'wall_thickness': wall_thickness  # добавляем толщину стен
    }

def get_wall_weight(wall_type, difficulty):
    """Возвращает вес стены в зависимости от типа и сложности"""
    weights = {
        'EASY': {'v': (1, 10), 'h': (1, 10)},   # Случайные веса
        # 'EASY': {'v': (5, 50), 'h': (5, 50)},
        'MEDIUM': {'v': (5, 20), 'h': (5, 20)},  # Более высокие веса
        # 'MEDIUM': {'v': (10, 50), 'h': (10, 50)},
        'HARD': {'v': (10, 50), 'h': (10, 50)},  # Максимальные веса
        'EXPLORE': {'v': (1, 100), 'h': (1, 100)} # Полный рандом
    }
    min_w, max_w = weights[difficulty][wall_type]
    return random.randint(min_w, max_w)


def add_cycles(grid_width, grid_height, dsu, removed_walls, all_walls, num_cycles):
    # Получаем список стен, которые НЕ были удалены (физически присутствуют в лабиринте)
    present_walls = [wall for wall in all_walls if wall not in removed_walls]
    random.shuffle(present_walls)

    cycles_added = 0

    for wall in present_walls:
        if cycles_added >= num_cycles:
            break

        # Определяем клетки по обе стороны от стены
        if wall[0] == 'h':
            cell_a = wall[1] * grid_width + wall[2]
            cell_b = (wall[1] + 1) * grid_width + wall[2]
        else:
            cell_a = wall[1] * grid_width + wall[2]
            cell_b = wall[1] * grid_width + (wall[2] + 1)

        # Если клетки уже соединены - удаляем стену для создания цикла
        if dsu.find(cell_a) == dsu.find(cell_b):
            removed_walls.add(wall)
            cycles_added += 1


def is_maze_connected(dsu):
    root = dsu.find(0)
    for i in range(1, len(dsu.parent)):
        if dsu.find(i) != root:
            return False
    return True

def is_maze_connected2(grid_width, grid_height, removed_walls):
    dsu = DSU(grid_width * grid_height)
    for wall in removed_walls:
        row, col = wall[1], wall[2]
        if wall[0] == 'h':
            cell_a = row * grid_width + col
            cell_b = (row + 1) * grid_width + col
        else:
            cell_a = row * grid_width + col
            cell_b = row * grid_width + (col + 1)
        dsu.union(cell_a, cell_b)

    root = dsu.find(0)
    return all(dsu.find(i) == root for i in range(1, grid_width * grid_height))

# def add_cycles(grid_width, grid_height, removed_walls, num_cycles):
#     candidates = list(removed_walls)
#     random.shuffle(candidates)
#     cycles_added = 0
#
#     for wall in candidates:
#         if cycles_added >= num_cycles:
#             break
#
#         # Удаляем стену из removed_walls (возвращаем стену в лабиринт)
#         removed_walls.remove(wall)
#
#         # Временная проверка связности
#         temp_dsu = DSU(grid_width * grid_height)
#         for w in removed_walls:
#             row, col = w[1], w[2]
#             if w[0] == 'h':
#                 cell_a = row * grid_width + col
#                 cell_b = (row + 1) * grid_width + col
#             else:
#                 cell_a = row * grid_width + col
#                 cell_b = row * grid_width + (col + 1)
#             temp_dsu.union(cell_a, cell_b)
#
#         if is_maze_connected(grid_width, grid_height, removed_walls):
#             cycles_added += 1
#         else:
#             # Откатываем изменение, если нарушилась связность
#             removed_walls.add(wall)




