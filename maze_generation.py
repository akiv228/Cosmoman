import pickle
import random
from pygame import Rect
from config import WIDTH, HEIGHT


class DSU: #Disjoint Set Union
    def __init__(self, size):
        self.parent = list(range(size)) # Изначально каждый элемент — корень

        self.rank = [0] * size  # Добавляем ранги  - высота (глубина) поддерева

    #  рекурсивно находит корень множества с оптимизацией (эвристикой) сжатия путей
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # path compression
        return self.parent[x]


    #  объединяет два множества с учетом ранга для минимизации глубины дерева
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            # объединение по рангу
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
    walls = generate_all_walls(grid_width, grid_height)

    # Этап 3: Построение MST алгоритмом Крускала
    # Генерация стен с весами только для сортировки
    walls_with_weights = [(wall[0], wall[1], wall[2], get_wall_weight(wall[0], difficulty)) for wall in walls]
    walls_with_weights.sort(key=lambda x: x[3])

    dsu = DSU(grid_width * grid_height)
    removed_walls = set()
    # Kruskal's algorithm
    for wall in walls_with_weights:
        cell_a, cell_b = get_cells_from_wall(wall, grid_width)
        if dsu.find(cell_a) != dsu.find(cell_b):
            dsu.union(cell_a, cell_b)
            removed_walls.add((wall[0], wall[1], wall[2]))

    # цикл через возвражение стен + проверка связности
    add_cycles(grid_width, grid_height, removed_walls, get_cycles_config(grid_width, grid_height, difficulty))
    # # Этап 4: Добавление циклов через удаление "лишних" стен
    # add_cycles_after_mst(grid_width, grid_height, removed_walls, walls, 5)
    #
    # # Этап 5: Добавление тупиков - возвращение стен
    # add_dead_ends_safe2(grid_width, grid_height, removed_walls, 5)


# Этап 5:
    if not validate_maze(grid_width, grid_height, removed_walls):
        print("Ошибка! Лабиринт не связный. Перегенерируйте.")
        # return generate_maze(grid_width, grid_height, difficulty)
    if not validate_maze2(grid_width, grid_height, removed_walls):
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

    wall (tuple): (тип_стены, ряд, столбец, [вес])
    grid_width (int): ширина сетки
    tuple: (индекс_клетки_A, индекс_клетки_B)
    """
    wall_type, row, col = wall[0], wall[1], wall[2]

    if wall_type == 'h':
        # горизонтальная соединяет клетки сверху и снизу
        upper_cell = row * grid_width + col
        lower_cell = (row + 1) * grid_width + col
        return (upper_cell, lower_cell)

    else:
        # вертикальная соединяет клетки слева и справа
        left_cell = row * grid_width + col
        right_cell = row * grid_width + (col + 1)
        return (left_cell, right_cell)



def calculate_layout(grid_width, grid_height):
    """Рассчитывает размеры и позиционирование лабиринта"""
    cell_size_x = (WIDTH - 40) // grid_width    # 20px padding с каждой стороны
    cell_size_y = (HEIGHT - 100) // grid_height # 50px сверху и снизу
    cell_size = min(cell_size_x, cell_size_y)

    return {
        'cell_size': cell_size,
        'maze_x': (WIDTH - grid_width * cell_size) // 2,
        'maze_y': (HEIGHT - grid_height * cell_size) // 2 + 20
    }


def generate_all_walls(grid_width, grid_height):
    """Генерирует все возможные стены с весами"""
    walls = []
    for row in range(grid_height):
        for col in range(grid_width):
            if col < grid_width - 1:
                walls.append((
                    'v',
                    row,
                    col
                ))
            if row < grid_height - 1:
                walls.append((
                    'h',
                    row,
                    col
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
        'EASY': int(grid_size * 0.2),
        'MEDIUM': int(grid_size * 0.05),
        'HARD': int(grid_size * 0.1),
        'EXPLORE': int(grid_size * 0.2)
    }[difficulty]


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

def add_cycles(grid_width, grid_height, removed_walls, num_cycles):
    candidates = list(removed_walls)  # копируем стены для перебора
    random.shuffle(candidates)  # случайный порядок
    cycles_added = 0

    for wall in candidates:
        if cycles_added >= num_cycles:
            break

        # удаляем стену из removed_walls (возвращаем её в лабиринт)
        removed_walls.discard(wall)  # Используем discard, чтобы не вызывать ошибку

        # проверяем, остался ли лабиринт связным
        if not validate_maze2(grid_width, grid_height, removed_walls):
            # если нет — возвращаем стену обратно
            removed_walls.add(wall)
        else:
            cycles_added += 1


def count_connections(cell, removed_walls, grid_width):
    # считает количество проходов у клетки
    connections = 0
    row = cell // grid_width
    col = cell % grid_width
    # проверяем все 4 возможных направления
    directions = [
        ('h', row-1, col),  # верхняя стена
        ('h', row, col),    # нижняя стена
        ('v', row, col-1),  # левая стена
        ('v', row, col)     # правая стена
    ]
    for wall in directions:
        if wall in removed_walls:
            connections += 1
    return connections

def add_cycles_after_mst(grid_width, grid_height, removed_walls, all_walls, num_cycles):
    non_mst_walls = [wall for wall in all_walls if wall not in removed_walls]
    random.shuffle(non_mst_walls)

    cycles_added = 0
    for wall in non_mst_walls:
        if cycles_added >= num_cycles:
            break
        # Удаляем стену
        removed_walls.add(wall)
        cycles_added += 1


def add_dead_ends_safe2(grid_width, grid_height, removed_walls, num_dead_ends):
    all_walls = generate_all_walls(grid_width, grid_height)
    present_walls = [wall for wall in all_walls if wall not in removed_walls]
    dead_ends_added = 0

    for wall in present_walls:
        if dead_ends_added >= num_dead_ends:
            break

        cell_a, cell_b = get_cells_from_wall(wall, grid_width)
        # закрываем проход
        removed_walls.discard(wall)  # убираем стену из removed_walls  она становится физической

        #  стала ли одна из клеток тупиком
        if count_connections(cell_a, removed_walls, grid_width) == 1 or \
           count_connections(cell_b, removed_walls, grid_width) == 1:
            dead_ends_added += 1
        else:
            #  не создали тупик — откатываем
            removed_walls.add(wall)
    print(dead_ends_added)

def add_dead_ends_safe(grid_width, grid_height, removed_walls, num_dead_ends):
    present_walls = [wall for wall in generate_all_walls(grid_width, grid_height) if wall not in removed_walls]
    dead_ends_added = 0

    for wall in present_walls:
        if dead_ends_added >= num_dead_ends:
            break

        cell_a, cell_b = get_cells_from_wall(wall, grid_width)
        connections_a = count_connections(cell_a, removed_walls, grid_width)
        connections_b = count_connections(cell_b, removed_walls, grid_width)

        # удаляем стену только если одна из клеток станет тупиком (1 проход)
        # и при этом не изолируется
        if (connections_a == 1 or connections_b == 1) and validate_maze2(grid_width, grid_height,
                                                                         removed_walls - {wall}):
            removed_walls.add(wall)
            dead_ends_added += 1