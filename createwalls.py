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
    present_walls = maze_info['present_walls']


    wall_sprites = []
    wall_sprites.append(Rect(maze_x, maze_y, gw * cs, wall_thickness))
    wall_sprites.append(Rect(maze_x, maze_y + gh * cs, gw * cs, wall_thickness))  # Нижняя граница
    wall_sprites.append(Rect(maze_x, maze_y, wall_thickness, gh * cs))  # Левая граница
    wall_sprites.append(Rect(maze_x + gw * cs, maze_y, wall_thickness, gh * cs + wall_thickness))  # Правая граница


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