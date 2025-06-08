import pygame as pg
from config import *
from base_sprite import *


# класс стен и препятствий
class Wall(sprite.Sprite):
     def __init__(self, x, y, width, height):
        super().__init__()
        self.image = Surface([width, height])
        self.image.fill(LIGHT_GREY)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Prize(GameSprite):
    def __init__(self, x, y):
        super().__init__('images\\bonus.png', x, y, 30, 30, False)


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

