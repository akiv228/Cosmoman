from collections import deque, defaultdict

def build_graph(maze_info):
    """
    создает граф соединений лабиринта на основе удаленных стен.
    алгоритм: проходит по списку удаленных стен, соединяя соседние ячейки двусторонними ребрами.
    """
    graph = defaultdict(list)
    for wall in maze_info['removed_walls']:
        r, c = wall[1], wall[2]
        if wall[0] == 'h':
            a, b = (r, c), (r + 1, c)
        else:
            a, b = (r, c), (r, c + 1)
        graph[a].append(b)
        graph[b].append(a)
    return graph

def bfs(graph, start):
    """
    алгоритм: использует очередь для обхода ячеек по уровням, обновляя расстояния.
    """
    visited = {start: 0}
    q = deque([start])
    while q:
        node = q.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited[neighbor] = visited[node] + 1
                q.append(neighbor)
    return visited

def reconstruct_path(graph, start, end):
    """
    алгоритм: строит карту родителей через bfs и проходит назад от конца к началу.
    """
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
    path.reverse()
    return path

def calculate_positions(maze_info, grid, debug_mode):
    """
    алгоритм:
    - находит углы лабиринта.
    - ищет пару углов с максимальным расстоянием через bfs.
    - при debug_mode строит путь между этими углами.
    - корректирует позиции для размещения спрайтов.
    """
    gw, gh = grid
    graph = build_graph(maze_info)

    corners = [(0, 0), (0, gw - 1), (gh - 1, 0), (gh - 1, gw - 1)]
    max_dist = 0
    best_pair = (corners[0], corners[1])

    for start in corners:
        distances = bfs(graph, start)
        for end in corners:
            if distances.get(end, 0) > max_dist:
                max_dist = distances[end]
                best_pair = (start, end)

    path = []
    # if debug_mode:
    path = reconstruct_path(graph, *best_pair)

    start_pos = adjust_position(maze_info, *best_pair[0])
    end_pos = adjust_position(maze_info, *best_pair[1])
    return start_pos, end_pos, path

def adjust_position(maze_info, row, col):
    """
    алгоритм: определяет центр ячейки и добавляет смещение с учетом размеров и стен.
    """
    cs = maze_info['cell_size']
    wall_thickness = maze_info['wall_thickness']

    if (row, col) == (0, 0):
        obj_size = max(30, 35)
    else:
        obj_size = max(40, 40)

    offset = (obj_size / 2) + (wall_thickness / 2) + 5
    x = maze_info['maze_x'] + col * cs + cs // 2
    y = maze_info['maze_y'] + row * cs + cs // 2
    return (int(x), int(y))



def split_path_into_segments(path):
    segments = []
    if len(path) < 2:
        return segments

    current_dir = get_direction(path[0], path[1])
    current_segment = [path[0]]

    for i in range(1, len(path)):
        new_dir = get_direction(path[i - 1], path[i])
        if new_dir == current_dir:
            current_segment.append(path[i])
        else:
            segments.append(current_segment)
            current_segment = [path[i - 1], path[i]]
            current_dir = new_dir

    segments.append(current_segment)
    return segments

def get_direction(p1, p2):
    dx = p2[1] - p1[1]
    dy = p2[0] - p1[0]
    if dx == 1: return 'right'
    if dx == -1: return 'left'
    if dy == 1: return 'down'
    if dy == -1: return 'up'
    return None

def get_segment_direction(segment):
    if len(segment) < 2:
        return None
    return get_direction(segment[0], segment[1])