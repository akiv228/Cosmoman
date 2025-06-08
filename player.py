import pygame as pg
from pygame import sprite

from base_sprite import GameSprite
from bullet import Bullet
from config import WALL_OFFSET


class Player(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, x_speed, y_speed, anime, xbool, lives=3):
        super().__init__(image, x, y, size_x, size_y, anime)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.lives = lives
        self.direction = 'right'
        self.bullets = sprite.Group()
        self.limit = 5
        self.collected_prizes = 0

    def fire(self, sound):
        if self.limit > 0:
            offset = 5
            
            if self.direction == 'left':
                bullet = Bullet('images\\bullet_left.png', 
                            self.rect.left - offset,
                            self.rect.centery, 
                            15, 20, 15, 'left')
            elif self.direction == 'right':
                bullet = Bullet('images\\bullet.png', 
                            self.rect.right + offset,
                            self.rect.centery, 
                            15, 20, 15, 'right')
            elif self.direction == 'top':
                bullet = Bullet('images\\bullet_up.png', 
                            self.rect.centerx, 
                            self.rect.top - offset,
                            15, 20, 15, 'top')
            elif self.direction == 'bottom':
                bullet = Bullet('images\\bullet_down.png', 
                            self.rect.centerx, 
                            self.rect.bottom + offset,
                            15, 20, 15, 'bottom')
            
            self.bullets.add(bullet)
            if pg.sprite.spritecollideany(bullet, self.walls): bullet.kill()
            self.limit -= 1

    def update(self):
        old_pos = self.rect.copy()
        self.rect.x += self.x_speed
        self._handle_axis_collision('x', old_pos)
        self.rect.y += self.y_speed
        self._handle_axis_collision('y', old_pos)
        self._update_direction_and_animation()

    def _handle_axis_collision(self, axis, old_pos):
        collided = False

        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                collided = True
                if axis == 'x':
                    if self.x_speed > 0:
                        self.rect.right = wall.rect.left - WALL_OFFSET
                    elif self.x_speed < 0:
                        self.rect.left = wall.rect.right + WALL_OFFSET
                    elif wall.rect.left - self.rect.right < WALL_OFFSET:
                        self.rect.right = wall.rect.left - WALL_OFFSET
                    elif self.rect.left - wall.rect.right < WALL_OFFSET:
                        self.rect.left = wall.rect.right + WALL_OFFSET
                else:
                    if self.y_speed > 0:
                        self.rect.bottom = wall.rect.top - WALL_OFFSET
                    elif self.y_speed < 0:
                        self.rect.top = wall.rect.bottom + WALL_OFFSET
                    elif wall.rect.top - self.rect.bottom < WALL_OFFSET:
                        self.rect.bottom = wall.rect.top - WALL_OFFSET
                    elif self.rect.top - wall.rect.bottom < WALL_OFFSET:
                        self.rect.top = wall.rect.bottom + WALL_OFFSET

        if collided and abs(self.x_speed if axis == 'x' else self.y_speed) > 5:
            self._pixel_perfect_collision(axis, old_pos)

    def _pixel_perfect_collision(self, axis, old_pos):
        step = 1 if (self.x_speed if axis == 'x' else self.y_speed) > 0 else -1
        test_pos = old_pos.copy()
        for i in range(0, abs(self.x_speed if axis == 'x' else self.y_speed), 1):
            test_pos.x += step if axis == 'x' else 0
            test_pos.y += 0 if axis == 'x' else step
            collision = False
            for wall in self.walls:
                if test_pos.colliderect(wall.rect):
                    collision = True
                    break
            if collision:
                if axis == 'x':
                    self.rect.x = test_pos.x - step
                else:
                    self.rect.y = test_pos.y - step
                break

    def _update_direction_and_animation(self):
        if self.x_speed > 0:
            self.direction = 'right'
            if self.anime:
                self.image = self.images[0]
        elif self.x_speed < 0:
            self.direction = 'left'
            if self.anime:
                self.image = self.images[1]

        if self.y_speed > 0:
            self.direction = 'bottom'
            if self.anime:
                self.image = self.images[3]
        elif self.y_speed < 0:
            self.direction = 'top'
            if self.anime:
                self.image = self.images[2]

    def take_bonus(self, sound):
        prizes_touched = sprite.spritecollide(self, self.prize, False)
        for prize in prizes_touched:
            self.collected_prizes += 1
            # if check_sound % 2 == 0:
            #     sound.play()
            prize.kill()


