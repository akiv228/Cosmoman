from base_sprite import GameSprite
from config import win_width, win_height

class Bullet(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, speed, direction):
        super().__init__(image, x, y, size_x, size_y, None)
        self.speed = speed
        self.direction = direction

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
            if self.rect.x < 0: self.kill()
        elif self.direction == 'right':
            self.rect.x += self.speed
            if self.rect.x > win_width: self.kill()
        elif self.direction == 'top':
            self.rect.y -= self.speed
            if self.rect.y < 0: self.kill()
        elif self.direction == 'bottom':
            self.rect.y += self.speed
            if self.rect.y > win_height: self.kill()

# import pygame as pg
# from base_sprite import GameSprite
#
# class Bullet(GameSprite):
#     def __init__(self, x, y):
#         super().__init__('images\\bullet.png', x, y, 5, 10, False)
#         self.speed = -10
#
#     def update(self):
#         self.rect.y += self.speed
#         if self.rect.y < 0:
#             self.kill()
