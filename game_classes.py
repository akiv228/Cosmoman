import pygame as pg
from config import *
from base_sprite import *
from random import randint


# класс стен и препятствий
class Wall(sprite.Sprite):
     def __init__(self, x, y, width, height):
        super().__init__()
        self.image = Surface([width, height])
        self.image.fill(LIGHT_GREY)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# класс бонуса в игре
# class Prize(sprite.Sprite):
#     def __init__(self, x, y, win_width = 30, win_height = 30):
#         super().__init__()
#         self.image = transform.scale(image.load('images\\bonus.png'), (win_width, win_height))
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
class Prize(GameSprite):
    def __init__(self, x, y):
        super().__init__('images\\bonus.png', x, y, 30, 30, False)

#
# #класс спрайта-врага
# class Enemy(GameSprite):
#  side = "left"
#  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, direction, board1, board2, xbool, anime):
#      # вызываем конструктор класса (Sprite):
#      GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y, anime)
#      self.speed = player_speed
#     # направление движения врага
#      self.direction = direction
#     # флаг, будет ли враг поворачиваться при движении влево или вправо
#      self.xbool = xbool
#     # крайние границы движения врага
#      self.board1 = board1
#      self.board2 = board2
#      self.index = 0
#
#
#   #движение врага
#  def update(self):
#     # будет ли спрайт анимированный
#     if self.anime:
#         if self.index >= 10:
#             self.index = 0
#         self.image = self.images[self.index//5]
#
#
#     if self.direction == 'h':
#         if self.rect.x <= self.board1:
#             if self.xbool:
#                 self.image = transform.flip(self.image, True, False)
#             self.side = "right"
#         if self.rect.x >= self.board2:
#             if self.xbool:
#                 self.image = transform.flip(self.image, True, False)
#             self.side = "left"
#         if self.side == "left":
#             self.rect.x -= self.speed
#         else:
#             self.rect.x += self.speed
#
#     elif self.direction == 'v':
#         if self.rect.y <= self.board1:
#             self.side = "down"
#         if self.rect.y >= self.board2:
#             self.side = "up"
#         if self.side == "down":
#             self.rect.y += self.speed
#         else:
#             self.rect.y -= self.speed
#         self.index += 1

class Enemy(GameSprite):
    def __init__(self, image_path, x, y, width, height, speed, direction, board1, board2, walls):
        super().__init__(image_path, x, y, width, height, anime=False)
        self.speed = speed
        self.direction = direction
        self.board1 = board1
        self.board2 = board2
        self.moving_forward = True
        self.walls = walls

    def update(self):
        old_rect = self.rect.copy()

        if self.direction == 'h':
            if self.moving_forward:
                self.rect.x += self.speed
                if self.rect.x >= self.board2:
                    self.moving_forward = False
            else:
                self.rect.x -= self.speed
                if self.rect.x <= self.board1:
                    self.moving_forward = True
        elif self.direction == 'v':
            if self.moving_forward:
                self.rect.y += self.speed
                if self.rect.y >= self.board2:
                    self.moving_forward = False
            else:
                self.rect.y -= self.speed
                if self.rect.y <= self.board1:
                    self.moving_forward = True

        if pg.sprite.spritecollideany(self, self.walls):
            self.rect = old_rect
            self.moving_forward = not self.moving_forward


# class Enemy(GameSprite):
#     def __init__(self, image_path, x, y, width, height, speed, direction, board1, board2):
#         super().__init__(image_path, x, y, width, height, anime=False)
#         self.speed = speed
#         self.direction = direction  # 'h' - горизонтально, 'v' - вертикально
#         self.board1 = board1
#         self.board2 = board2
#         self.moving_forward = True
#
#     def update(self):
#         if self.direction == 'h':
#             if self.moving_forward:
#                 self.rect.x += self.speed
#                 if self.rect.x >= self.board2:
#                     self.moving_forward = False
#             else:
#                 self.rect.x -= self.speed
#                 if self.rect.x <= self.board1:
#                     self.moving_forward = True
#         elif self.direction == 'v':
#             if self.moving_forward:
#                 self.rect.y += self.speed
#                 if self.rect.y >= self.board2:
#                     self.moving_forward = False
#             else:
#                 self.rect.y -= self.speed
#                 if self.rect.y <= self.board1:
#                     self.moving_forward = True