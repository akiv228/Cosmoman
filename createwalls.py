import pickle
from pygame import Rect

import pygame as pg
import random
from pygame import sprite, Surface, Rect

# # Updated Wall class to include type, row, and col
# class Wall(sprite.Sprite):
#     def __init__(self, x, y, width, height, wall_type=None, row=None, col=None):
#         super().__init__()
#         self.image = Surface([width, height])
#         self.image.fill((200, 200, 200))  # LIGHT_GREY, adjust as needed
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.type = wall_type  # 'h' for horizontal, 'v' for vertical, None for outer walls
#         self.row = row
#         self.col = col

# Updated reconstruct_wall_rects to return wall data with type, row, and col
# def reconstruct_wall_rects(maze_info):
#     gw = maze_info['grid_width']
#     gh = maze_info['grid_height']
#     cs = maze_info['cell_size']
#     maze_x = maze_info['maze_x']
#     maze_y = maze_info['maze_y']
#     wall_thickness = maze_info['wall_thickness']
#     present_walls = maze_info['present_walls']
#
#     wall_data = []
#     # Outer boundaries (no type, row, or col needed for navigation logic)
#     wall_data.append((Rect(maze_x, maze_y, gw * cs, wall_thickness), None, None, None))  # Top
#     wall_data.append((Rect(maze_x, maze_y + gh * cs, gw * cs, wall_thickness), None, None, None))  # Bottom
#     wall_data.append((Rect(maze_x, maze_y, wall_thickness, gh * cs), None, None, None))  # Left
#     wall_data.append((Rect(maze_x + gw * cs, maze_y, wall_thickness, gh * cs + wall_thickness), None, None, None))  # Right
#
#     # Inner walls with type, row, and col
#     for wall in present_walls:
#         if wall[0] == 'h':  # Horizontal wall
#             x = maze_x + wall[2] * cs
#             y = maze_y + (wall[1] + 1) * cs
#             rect = Rect(x, y - wall_thickness // 2, cs, wall_thickness)
#             wall_data.append((rect, 'h', wall[1], wall[2]))
#         else:  # Vertical wall ('v')
#             x = maze_x + (wall[2] + 1) * cs
#             y = maze_y + wall[1] * cs
#             rect = Rect(x - wall_thickness // 2, y, wall_thickness, cs)
#             wall_data.append((rect, 'v', wall[1], wall[2]))
#
#     return wall_data

def reconstruct_wall_rects(maze_info):
    gw = maze_info['grid_width']
    gh = maze_info['grid_height']
    cs = maze_info['cell_size']
    maze_x = maze_info['maze_x']
    maze_y = maze_info['maze_y']
    wall_thickness = maze_info['wall_thickness']
    present_walls = maze_info['present_walls']  # Берем готовый список оставшихся стен

    # Создаем внешние границы лабиринта
    wall_sprites = []
    wall_sprites.append(Rect(maze_x, maze_y, gw * cs, wall_thickness))  # Верхняя граница
    wall_sprites.append(Rect(maze_x, maze_y + gh * cs, gw * cs, wall_thickness))  # Нижняя граница
    wall_sprites.append(Rect(maze_x, maze_y, wall_thickness, gh * cs))  # Левая граница
    wall_sprites.append(Rect(maze_x + gw * cs, maze_y, wall_thickness, gh * cs + wall_thickness))  # Правая граница

    # Создаем спрайты для внутренних стен
    for wall in present_walls:
        if wall[0] == 'h':  # Горизонтальная стена
            x = maze_x + wall[2] * cs
            y = maze_y + (wall[1] + 1) * cs
            wall_sprites.append(Rect(x, y - wall_thickness // 2, cs, wall_thickness))
        else:  # Вертикальная стена ('v')
            x = maze_x + (wall[2] + 1) * cs
            y = maze_y + wall[1] * cs
            wall_sprites.append(Rect(x - wall_thickness // 2, y, wall_thickness, cs))

    return wall_sprites