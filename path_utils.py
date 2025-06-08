from collections import deque, defaultdict

def build_graph(maze_info):
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

def find_all_segments(maze_info):

    removed_walls = maze_info['removed_walls']
    gw, gh = maze_info['grid_width'], maze_info['grid_height']
    segments = []

    # Горизонтальные сегменты
    for r in range(gh):
        c = 0
        while c < gw - 1:
            if ('v', r, c) in removed_walls:
                start = c
                while c < gw - 1 and ('v', r, c) in removed_walls:
                    c += 1
                segment = [(r, i) for i in range(start, c + 1)]
                if len(segment) >= 2:
                    segments.append(segment)
            else:
                c += 1

    # Вертикальные сегменты
    for c in range(gw):
        r = 0
        while r < gh - 1:
            if ('h', r, c) in removed_walls:
                start = r
                while r < gh - 1 and ('h', r, c) in removed_walls:
                    r += 1
                segment = [(i, c) for i in range(start, r + 1)]
                if len(segment) >= 2:
                    segments.append(segment)
            else:
                r += 1

    return segments