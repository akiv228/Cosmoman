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


    # Настраиваем количество циклов по сложности
    cycles_config = {
        'EASY': 1,  # Без циклов
        'MEDIUM': 5,
        'HARD': 10,
        'EXPLORE': 15
    }
    # add_cycles(grid_width, grid_height, removed_walls, dsu, cycles_config[difficulty])
    # if not is_maze_connected(grid_width, grid_height, removed_walls):
    #     raise ValueError("Лабиринт не связный!")
    if not is_maze_connected(grid_width, grid_height, removed_walls):
        print("Ошибка! Лабиринт не связный. Перегенерируйте.")
        return generate_maze(grid_width, grid_height, difficulty)  # Рекурсивный перезапуск

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

    return wall_sprites

def get_wall_weight(wall_type, difficulty):
    """Возвращает вес стены в зависимости от типа и сложности"""
    weights = {
        'EASY': {'v': (1, 10), 'h': (1, 10)},   # Случайные веса
        # 'MEDIUM': {'v': (5, 20), 'h': (5, 20)},  # Более высокие веса
        'MEDIUM': {'v': (10, 50), 'h': (10, 50)},
        'HARD': {'v': (10, 50), 'h': (10, 50)},  # Максимальные веса
        'EXPLORE': {'v': (1, 100), 'h': (1, 100)} # Полный рандом
    }
    min_w, max_w = weights[difficulty][wall_type]
    return random.randint(min_w, max_w)


def add_cycles(grid_width, grid_height, removed_walls, dsu, num_cycles):
    # Список всех стен, которые были удалены (проходы)
    candidates = [wall for wall in removed_walls if wall[3] > 1]  # Не трогаем стены с весом 1

    for _ in range(num_cycles):
        if not candidates:
            break
        # Выбираем случайную стену из кандидатов
        wall = random.choice(candidates)
        candidates.remove(wall)

        # Проверяем, что её добавление не разъединит лабиринт
        row, col = wall[1], wall[2]
        if wall[0] == 'h':
            cell_a = row * grid_width + col
            cell_b = (row + 1) * grid_width + col
        else:
            cell_a = row * grid_width + col
            cell_b = row * grid_width + (col + 1)

        # Если клетки уже связаны (есть другой путь), можно добавить стену обратно (создать цикл)
        if dsu.find(cell_a) == dsu.find(cell_b):
            removed_walls.remove(wall)

# def add_cycles(grid_width, grid_height, removed_walls, dsu, num_cycles):
#     cycles_added = 0
#     candidate_walls = [wall for wall in removed_walls
#                        if is_wall_creates_cycle(wall, grid_width, dsu)]
#
#     while cycles_added < num_cycles and candidate_walls:
#         wall = random.choice(candidate_walls)
#         removed_walls.remove(wall)
#         candidate_walls.remove(wall)
#         cycles_added += 1
#
#
# def is_wall_creates_cycle(wall, grid_width, dsu):
#     wall_type, row, col = wall  # Теперь работает с правильной структурой
#     if wall_type == 'h':
#         cell_a = row * grid_width + col
#         cell_b = (row + 1) * grid_width + col
#     else:
#         cell_a = row * grid_width + col
#         cell_b = row * grid_width + (col + 1)
#
#     return dsu.find(cell_a) == dsu.find(cell_b)


def is_maze_connected(grid_width, grid_height, removed_walls):
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

    # Все ячейки должны принадлежать одному множеству
    root = dsu.find(0)
    for i in range(1, grid_width * grid_height):
        if dsu.find(i) != root:
            return False
    return True


# def is_maze_connected(grid_width, grid_height, removed_walls):
#     temp_dsu = DSU(grid_width * grid_height)
#     for wall in removed_walls:
#         wall_type, row, col = wall
#         if wall_type == 'h':
#             cell_a = row * grid_width + col
#             cell_b = (row + 1) * grid_width + col
#         else:
#             cell_a = row * grid_width + col
#             cell_b = row * grid_width + (col + 1)
#         temp_dsu.union(cell_a, cell_b)
#
#     root = temp_dsu.find(0)
#     return all(temp_dsu.find(i) == root for i in range(grid_width * grid_height))

