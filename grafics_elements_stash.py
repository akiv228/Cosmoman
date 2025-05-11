import pygame as pg
from pygame.math import clamp
from pygame import *
from random import *
from math import *
import colorsys
from config import *


class ColorStar(sprite.Sprite):
    # Увеличиваем количество палитр и добавляем динамическую генерацию
    COLOR_PALETTES = [
        # Генератор палитр на основе HSL
        {
            'base_hue': uniform(0.0, 1.0),
            'type': choice(['analogous', 'triad', 'monochromatic'])
        }
        for _ in range(20)  # 20 уникальных палитр
    ]

    def __init__(self, w, h, palette_config) -> None:
        super().__init__()
        self.layer = randint(0, 2)

        # Генерация цвета на основе HSL
        hue, saturation, lightness = self._generate_hsl_color(palette_config)
        self.base_color = self._hsl_to_rgb(hue, saturation, lightness)

        # Параметры звезды
        self.r = self._generate_size()
        self.true_radius = self.r * uniform(0.8, 1.2)  # Вариация размера

        # Настройки мерцания
        self.shine_type = choice(['sine', 'pulse', 'random'])
        self.shine_phase = uniform(0, pi * 2)
        self.shine_speed = uniform(0.05, 0.3) * (3 - self.layer)  # Ближние быстрее
        self.shine_power = uniform(0.5, 1.0)

        # Графические компоненты
        self.image = Surface((self.r * 2 * 2, self.r * 2 * 2), SRCALPHA)  # Больше места для эффектов
        self.rect = self.image.get_rect()
        self.rect.center = (randint(0, w), randint(0, h))

    def _generate_hsl_color(self, config):
        # Генерация гармоничных цветов на основе теории цвета
        hue = config['base_hue']
        if config['type'] == 'analogous':
            hue += uniform(-0.1, 0.1)
        elif config['type'] == 'triad':
            hue += choice([0.33, -0.33])
        elif config['type'] == 'monochromatic':
            hue += uniform(-0.05, 0.05)

        saturation = 0.7 + self.layer * 0.1
        lightness = 0.5 - self.layer * 0.15
        return (hue % 1.0,
                clamp(saturation + uniform(-0.1, 0.1), 0.4, 0.9),
                clamp(lightness + uniform(-0.1, 0.1), 0.3, 0.7))

    def _hsl_to_rgb(self, h, s, l):
        # Конвертация HSL в RGB с коррекцией для pygame
        rgb = colorsys.hls_to_rgb(h, l, s)
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def _generate_size(self):
        # Нелинейная зависимость размера от слоя
        base_sizes = [3.5, 2.0, 1.0]
        return int(base_sizes[self.layer] * expovariate(1.0))

    def update(self):
        # Динамическое мерцание разного типа
        if self.shine_type == 'sine':
            alpha = 150 + int(105 * sin(self.shine_phase))
        elif self.shine_type == 'pulse':
            alpha = 255 if sin(self.shine_phase) > 0 else 100
        else:  # random
            alpha = randint(100, 255)

        self.shine_phase += self.shine_speed
        alpha = int(alpha * self.shine_power)

        # Рисуем звезду с эффектом свечения
        self.image.fill((0, 0, 0, 0))
        glow_radius = int(self.true_radius * 2.5)
        for i in range(3):
            alpha_glow = int(alpha * (0.3 - i * 0.1))
            draw.circle(self.image,
                        (*self.base_color, alpha_glow),
                        (self.r * 2, self.r * 2),
                        int(glow_radius * (1 - i * 0.3)))

        draw.circle(self.image,
                    (*self.base_color, alpha),
                    (self.r * 2, self.r * 2),
                    int(self.true_radius))


class WhiteStar(sprite.Sprite):
    def __init__(self, w, h) -> None:
        super().__init__()
        self.r = randint(1, 3)
        self.image = Surface((self.r * 2, self.r * 2), SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, w)
        self.rect.y = randint(0, h)
        self.color = (255, 255, 255, 255)
        self.shine_speed = randint(1, 100)
        self.shine_deep = randint(150, 250)
        self.shine_revers = False
        self.shine_ok = randint(0, 1)
        # Добавляем слой параллакса (0 — ближний, 2 — дальний)
        self.layer = randint(0, 2)
        # Чем дальше звезда, тем она должна быть мельче и тусклее
        if self.layer == 0:
            self.r = randint(2, 3)  # Ближние звёзды — крупнее
        elif self.layer == 1:
            self.r = randint(1, 2)
            self.color = (255, 255, 255, 200)  # Средние — чуть прозрачнее
        else:
            self.r = 1
            self.color = (255, 255, 255, 150)  # Дальние — самые тусклые

    def update(self):
        if self.shine_ok == 1: self.color = self.__shine()
        draw.circle(self.image, self.color, (self.r, self.r), self.r)

    def __shine(self):
        alpha = self.color[3]  # Только альфа-канал
        if self.shine_revers:
            alpha += self.shine_speed
            if alpha >= 255:
                alpha = 255
                self.shine_revers = False
        else:
            alpha -= self.shine_speed
            if alpha <= 255 - self.shine_deep:
                alpha = 255 - self.shine_deep
                self.shine_revers = True
        # Возвращаем тот же RGB, но с новой альфой
        return (self.color[0], self.color[1], self.color[2], alpha)






# vec2, vec3 = pg.math.Vector2, pg.math.Vector3
# CENTER = vec2(WIDTH // 2, HEIGHT // 2)
#
# class Star_rect():
#     def __init__(self):
#
#         self.pos3d = self.get_pos3d()
#         self.vel = random.uniform(0.05, 0.25)
#         self.color = random.choice(COLORS)
#         self.screen_pos = vec2(0, 0)
#         self.size = 10
#
#
#     def get_pos3d(self, scale_pos=35):
#         angle = random.uniform(0, 2 * math.pi)
#         radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         return vec3(x, y, Z_DISTANCE)
#
#
#     def update(self):
#         self.pos3d.z -= self.vel
#         self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d
#
#         self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
#         self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)
#         # rotate xy
#         self.pos3d.xy = self.pos3d.xy.rotate(0.2)
#         # mouse
#         # mouse_pos = CENTER - vec2(pg.mouse.get_pos())
#         # self.screen_pos += mouse_pos
#
#
#     def draw(self, window):
#         s = self.size
#         if (-s < self.screen_pos.x < WIDTH + s) and (-s < self.screen_pos.y < HEIGHT + s):
#             pg.draw.rect(window, self.color, (*self.screen_pos, self.size, self.size))
#
#
#
# # класс главного фона у 3 уровня
# class Starfield_rects():
#     def __init__(self):
#         self.alpha_surface = pg.Surface(RES)
#         self.alpha_surface.set_alpha(ALPHA)
#         self.stars = [Star_rect() for i in range(NUM_STARS)]
#
#
#     def run(self, window):
#         [star.update() for star in self.stars]
#         self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
#         [star.draw(window) for star in self.stars]

