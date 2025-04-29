from pygame import sprite
from base_sprite import GameSprite
from bullet import Bullet
from constants import win_width, win_height

class Player(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, x_speed, y_speed, anime, xbool, lives=3):
        super().__init__(image, x, y, size_x, size_y, anime)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.lives = lives
        self.direction = 'right'
        self.bullets = sprite.Group()
        self.limit = 5  # Will be set in place_objects
        self.collected_prizes = 0  # Assuming this exists for prize tracking

    def fire(self, sound):
        if self.limit > 0:
            # sound.play()  # Uncomment if sound is available
            if self.direction == 'left':
                bullet = Bullet('images\\bullet_left.png', self.rect.left, self.rect.centery, 15, 20, 15, 'left')
            elif self.direction == 'right':
                bullet = Bullet('images\\bullet.png', self.rect.right, self.rect.centery, 15, 20, 15, 'right')
            elif self.direction == 'top':
                bullet = Bullet('images\\bullet_up.png', self.rect.centerx, self.rect.top, 15, 20, 15, 'top')
            elif self.direction == 'bottom':
                bullet = Bullet('images\\bullet_down.png', self.rect.centerx, self.rect.bottom, 15, 20, 15, 'bottom')
            self.bullets.add(bullet)
            self.limit -= 1

    def update(self):
        if self.rect.x <= win_width - 80 and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, self.walls, False)
        if self.x_speed > 0:
            if self.anime:
                self.image = self.images[0]
            self.direction = 'right'
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            if self.anime:
                self.image = self.images[1]
            self.direction = 'left'
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        if self.rect.y <= win_height - 80 and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, self.walls, False)
        if self.y_speed > 0:
            self.direction = 'bottom'
            if self.anime:
                self.image = self.images[3]
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            self.direction = 'top'
            if self.anime:
                self.image = self.images[2]
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def take_bonus(self, sound):
        prizes_touched = sprite.spritecollide(self, self.prize, False)
        for prize in prizes_touched:
            self.collected_prizes += 1
            # if check_sound % 2 == 0:
            #     sound.play()
            prize.kill()

import pygame as pg
from base_sprite import GameSprite
# from bullet import Bullet

# class Player(GameSprite):
#     def __init__(self, image_path, x, y, width, height, x_speed, y_speed, rotated, is_collide, lives):
#         super().__init__(image_path, x, y, width, height, rotated)
#         self.x_speed = x_speed
#         self.y_speed = y_speed
#         self.is_collide = is_collide
#         self.lives = lives
#         self.walls = None
#         self.prizes = None
#         self.bullets = None
#         self.limit = 0
#         self.collected_prizes = 0
#
#     def update(self):
#         next_x = self.rect.x + self.x_speed
#         next_y = self.rect.y + self.y_speed
#         temp_rect = self.rect.copy()
#         temp_rect.x = next_x
#         temp_rect.y = next_y
#
#         if self.walls and not pg.sprite.spritecollide(self, self.walls, False):
#             self.rect.x = next_x
#             self.rect.y = next_y
#
#         collected = pg.sprite.spritecollide(self, self.prizes, True)
#         if collected:
#             self.collected_prizes += len(collected)
#
#     def fire(self, sound):
#         if self.bullets and self.limit > 0:
#             bullet = Bullet(self.rect.centerx, self.rect.top)
#             self.bullets.add(bullet)
#             self.limit -= 1