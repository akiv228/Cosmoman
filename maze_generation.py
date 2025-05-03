import pickle
import random
from pygame import Rect
from constants import WIDTH, HEIGHT


class DSU: #Disjoint Set Union
    def __init__(self, size):
        self.parent = list(range(size)) # Изначально каждый элемент — корень

        self.rank = [0] * size  # Добавляем ранги  - высота (глубина) поддерева

    #  Рекурсивно находит корень множества с оптимизацией (эвристикой) сжатия путей
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # path compression
        return self.parent[x]


    #  Объединяет два множества с учетом ранга для минимизации глубины дерева
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            # Объединение по рангу
            if self.rank[root_x] < self.rank[root_y]: # если глубина дерева х меньше, то подвешиваем его к более глубокому
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else: # self.rank[root_x] == self.rank[root_y]:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1


def generate_maze(grid_width, grid_height, difficulty):
    # Этап 1: Рассчет размеров и позиционирование
    layout = calculate_layout(grid_width, grid_height)

    # Этап 2: Генерация всех возможных стен
    walls = generate_all_walls(grid_width, grid_height, difficulty)
    # Этап 3: Построение MST алгоритмом Крускала

    # Сортировка стен по весу (от меньшего к большему)
    walls.sort(key=lambda x: x[3])

    dsu = DSU(grid_width * grid_height)
    removed_walls = set()
    # Kruskal's algorithm
    for wall in walls:
        cell_a, cell_b = get_cells_from_wall(wall, grid_width)
        if dsu.find(cell_a) != dsu.find(cell_b):
            dsu.union(cell_a, cell_b)
            removed_walls.add((wall[0], wall[1], wall[2]))


    # add_cycles(grid_width, grid_height, dsu, removed_walls, walls, cycles_config[difficulty])
    # add_cycles(grid_width, grid_height, removed_walls, get_cycles_config(grid_width, grid_height, difficulty))
    add_cycles_optimized(grid_width, grid_height, removed_walls, get_cycles_config(grid_width, grid_height, difficulty))

    if not is_maze_connected(dsu):
         print("Ошибка! Лабиринт не связный. Перегенерируйте.")
         return generate_maze(grid_width, grid_height, difficulty)  # Рекурсивный перезапуск
    # if not is_maze_connected2(grid_width, grid_height, removed_walls):
    #      print("Ошибка! Лабиринт не связный. Перегенерируйте.")

# Этап 5: Финальная проверка связности
    if not validate_maze(grid_width, grid_height, removed_walls):
        print("Ошибка! Лабиринт не связный. Перегенерируйте.")
        # return generate_maze(grid_width, grid_height, difficulty)
    if not validate_maze2(grid_width, grid_height, removed_walls):
        print("Ошибка! Лабиринт не связный. Перегенерируйте.")


    if not validate_maze3(grid_width, grid_height, removed_walls):
        print("Ошибка! Лабиринт не связный. Перегенерируйте.")


    present_walls = [wall for wall in walls if wall not in removed_walls]

    return {
        'removed_walls': removed_walls,
        'grid_width': grid_width,
        'grid_height': grid_height,
        'cell_size': layout['cell_size'],
        'maze_x': layout['maze_x'],
        'maze_y': layout['maze_y'],
        'present_walls': present_walls,
        'wall_thickness': 3
    }


def get_cells_from_wall(wall, grid_width):
    """
    Возвращает две соседние клетки, между которыми находится стена.

    Параметры:
    wall (tuple): (тип_стены, ряд, столбец, [вес])
    grid_width (int): ширина сетки

    Возвращает:
    tuple: (индекс_клетки_A, индекс_клетки_B)
    """
    wall_type, row, col = wall[0], wall[1], wall[2]

    if wall_type == 'h':
        # Горизонтальная стена соединяет клетки сверху и снизу
        upper_cell = row * grid_width + col
        lower_cell = (row + 1) * grid_width + col
        return (upper_cell, lower_cell)

    else:  # Вертикальная стена
        # Вертикальная стена соединяет клетки слева и справа
        left_cell = row * grid_width + col
        right_cell = row * grid_width + (col + 1)
        return (left_cell, right_cell)



def calculate_layout(grid_width, grid_height):
    """Рассчитывает размеры и позиционирование лабиринта"""
    cell_size_x = (WIDTH - 40) // grid_width # 20px padding с каждой стороны
    cell_size_y = (HEIGHT - 100) // grid_height # 50px сверху и снизу
    cell_size = min(cell_size_x, cell_size_y)

    return {
        'cell_size': cell_size,
        'maze_x': (WIDTH - grid_width * cell_size) // 2,
        'maze_y': (HEIGHT - grid_height * cell_size) // 2 + 20
    }


def generate_all_walls(grid_width, grid_height, difficulty):
    """Генерирует все возможные стены с весами"""
    walls = []
    for row in range(grid_height):
        for col in range(grid_width):
            if col < grid_width - 1:
                walls.append((
                    'v',
                    row,
                    col,
                    get_wall_weight('v', difficulty)
                ))
            if row < grid_height - 1:
                walls.append((
                    'h',
                    row,
                    col,
                    get_wall_weight('h', difficulty)
                ))
    return walls


def get_wall_weight(wall_type, difficulty):
    """Возвращает вес стены в зависимости от типа и сложности"""
    weights = {
        # 'EASY': {'v': (1, 10), 'h': (1, 10)},   # Случайные веса
        'EASY': {'v': (1, 10), 'h': (1, 10)},
        'MEDIUM': {'v': (5, 20), 'h': (5, 20)},  # Более высокие веса
        # 'MEDIUM': {'v': (10, 50), 'h': (10, 50)},
        'HARD': {'v': (10, 50), 'h': (10, 50)},  # Максимальные веса
        'EXPLORE': {'v': (1, 100), 'h': (1, 100)} # Полный рандом
    }
    min_w, max_w = weights[difficulty][wall_type]
    return random.randint(min_w, max_w)


def get_cycles_config(grid_width, grid_height, difficulty):
    """Возвращает количество циклов для заданной сложности"""
    grid_size = grid_width * grid_height
    return {
        'EASY': int(grid_size * 0.1),
        'MEDIUM': int(grid_size * 0.05),
        'HARD': int(grid_size * 0.1),
        'EXPLORE': int(grid_size * 0.2)
    }[difficulty]

# def add_cycles(grid_width, grid_height, dsu, removed_walls, all_walls, num_cycles):
#     # Получаем список стен, которые НЕ были удалены (физически присутствуют в лабиринте)
#     present_walls = [wall for wall in all_walls if wall not in removed_walls]
#     random.shuffle(present_walls)
#
#     cycles_added = 0
#
#     for wall in present_walls:
#         if cycles_added >= num_cycles:
#             break
#
#         # Определяем клетки по обе стороны от стены
#         if wall[0] == 'h':
#             cell_a = wall[1] * grid_width + wall[2]
#             cell_b = (wall[1] + 1) * grid_width + wall[2]
#         else:
#             cell_a = wall[1] * grid_width + wall[2]
#             cell_b = wall[1] * grid_width + (wall[2] + 1)
#
#         # Если клетки уже соединены - удаляем стену для создания цикла
#         if dsu.find(cell_a) == dsu.find(cell_b):
#             removed_walls.add(wall)
#             cycles_added += 1
#
def build_dsu_from_walls(grid_width, grid_height, walls):
    """Строит DSU на основе набора стен"""
    dsu = DSU(grid_width * grid_height)
    for wall in walls:
        cell_a, cell_b = get_cells_from_wall(wall, grid_width)
        dsu.union(cell_a, cell_b)
    return dsu


def validate_maze(grid_width, grid_height, removed_walls):
    """Проверяет связность лабиринта"""
    dsu = build_dsu_from_walls(grid_width, grid_height, removed_walls)
    return all(dsu.find(0) == dsu.find(i) for i in range(1, grid_width*grid_height))


def validate_maze2(grid_width, grid_height, removed_walls):
    dsu = build_dsu_from_walls(grid_width, grid_height, removed_walls)
    root = dsu.find(0)  # Кешируем корень стартовой клетки
    total_cells = grid_width * grid_height

    # Ранний выход при первом несовпадении
    for i in range(1, total_cells):
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


def add_cycles(grid_width, grid_height, removed_walls, num_cycles):
    candidates = list(removed_walls)
    random.shuffle(candidates)
    cycles_added = 0

    for wall in candidates:
        if cycles_added >= num_cycles:
            break

        # Удаляем стену из removed_walls (возвращаем стену в лабиринт)
        removed_walls.remove(wall)

        # Временная проверка связности
        temp_dsu = DSU(grid_width * grid_height)
        for w in removed_walls:
            row, col = w[1], w[2]
            if w[0] == 'h':
                cell_a = row * grid_width + col
                cell_b = (row + 1) * grid_width + col
            else:
                cell_a = row * grid_width + col
                cell_b = row * grid_width + (col + 1)
            temp_dsu.union(cell_a, cell_b)

        if is_maze_connected2(grid_width, grid_height, removed_walls):
            cycles_added += 1
        else:
            # Откатываем изменение, если нарушилась связность
            removed_walls.add(wall)




