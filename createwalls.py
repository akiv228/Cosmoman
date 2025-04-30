import pickle
from pygame import Rect

def save_maze(filename, maze_info):
    with open(filename, 'wb') as f:
        pickle.dump(maze_info, f)

def load_maze(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def reconstruct_wall_rects(maze_info):
    gw = maze_info['grid_width']
    gh = maze_info['grid_height']
    cs = maze_info['cell_size']
    maze_x = maze_info['maze_x']
    maze_y = maze_info['maze_y']
    wall_thickness = maze_info['wall_thickness']

    all_walls = []
    for row in range(gh):
        for col in range(gw):
            if col < gw - 1:
                all_walls.append(('v', row, col))
            if row < gh - 1:
                all_walls.append(('h', row, col))

    removed_walls = maze_info['removed_walls']
    present_walls = [wall for wall in all_walls if wall not in removed_walls]

    wall_sprites = []
    wall_sprites.append(Rect(maze_x, maze_y, gw * cs, wall_thickness))
    wall_sprites.append(Rect(maze_x, maze_y + gh * cs, gw * cs, wall_thickness))
    wall_sprites.append(Rect(maze_x, maze_y, wall_thickness, gh * cs))
    wall_sprites.append(Rect(maze_x + gw * cs, maze_y, wall_thickness, gh * cs + wall_thickness))

    for wall in present_walls:
        if wall[0] == 'h':
            x = maze_x + wall[2] * cs
            y = maze_y + (wall[1] + 1) * cs
            wall_sprites.append(Rect(x, y - wall_thickness // 2, cs, wall_thickness))
        else:
            x = maze_x + (wall[2] + 1) * cs
            y = maze_y + wall[1] * cs
            wall_sprites.append(Rect(x - wall_thickness // 2, y, wall_thickness, cs))

    return wall_sprites