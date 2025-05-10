
import pygame as pg
from constants import *
from base_sprite import *
from random import randint
import random
import math


# class Star2(sprite.Sprite):
#     def __init__(self, w, h) -> None:
#         super().__init__()
#         self.r = randint(1, 2)
#         self.image = Surface((self.r * 2, self.r * 2), SRCALPHA)
#         self.rect = self.image.get_rect()
#         self.rect.x = randint(0, w)
#         self.rect.y = randint(1, h)
#         self.color = (255, 255, 255, 255)
#         self.shine_speed = randint(1, 100)
#         self.shine_deep = randint(150, 250)
#         self.shine_revers = False
#         self.shine_ok = randint(0, 1)
#
#     def update(self):
#         if self.shine_ok == 1: self.color = self.__shine()
#         draw.circle(self.image, self.color, (self.r, self.r), self.r)
#
#     def __shine(self):
#         # моргание звезд - зависит от shine_speed и shine_deep
#         # которые создаются случайно для каждой звезды
#         color = self.color[3]
#         if self.shine_revers:
#             color += self.shine_speed
#             if color >= 255:
#                 color = 255
#                 self.shine_revers = False
#         else:
#             color -= self.shine_speed
#             if color <= 255 - self.shine_deep:
#                 color = 255 - self.shine_deep
#                 self.shine_revers = True
#         return tuple(list(self.color)[0:3] + [color])

class Star2(sprite.Sprite):
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

class Star:
    def __init__(self, w, h):
        self.x = random.randint(0, w)
        self.y = random.randint(0, h)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 2)

class Starfield:
    def __init__(self, w, h, star_count):
        self.w = w
        self.h = h
        self.stars = [Star(w, h) for _ in range(star_count)]
        self.alpha_surface = pg.Surface((w, h), pg.SRCALPHA)

    def run(self):
        self.alpha_surface.fill((0, 0, 0, 255))
        for star in self.stars:
            star.y += star.speed
            if star.y > self.h:
                star.y = 0
                star.x = random.randint(0, self.w)
            pg.draw.circle(self.alpha_surface, (255, 255, 255), (int(star.x), int(star.y)), star.size)

# starfield = Starfield(710, 540, 300)

vec2, vec3 = pg.math.Vector2, pg.math.Vector3
CENTER = vec2(WIDTH // 2, HEIGHT // 2)

class Star_rect():
    def __init__(self):

        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.05, 0.25)
        self.color = random.choice(COLORS)
        self.screen_pos = vec2(0, 0)
        self.size = 10


    def get_pos3d(self, scale_pos=35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        return vec3(x, y, Z_DISTANCE)


    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)
        # rotate xy
        self.pos3d.xy = self.pos3d.xy.rotate(0.2)
        # mouse
        # mouse_pos = CENTER - vec2(pg.mouse.get_pos())
        # self.screen_pos += mouse_pos


    def draw(self, window):
        s = self.size
        if (-s < self.screen_pos.x < WIDTH + s) and (-s < self.screen_pos.y < HEIGHT + s):
            pg.draw.rect(window, self.color, (*self.screen_pos, self.size, self.size))



# класс главного фона у 3 уровня
class Starfield_rects():
    def __init__(self):
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(ALPHA)
        self.stars = [Star_rect() for i in range(NUM_STARS)]


    def run(self, window):
        [star.update() for star in self.stars]
        self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
        [star.draw(window) for star in self.stars]




# from pygame import *
# from grafics_classes import *
# from constants import *
#
# main_back = Backgrounds('images\\back.jpg', win_width, win_height, 0, 0)
# main_back2 = Backgrounds('images\\back.jpg', win_width, win_height, 0, 0)
# start_back = Backgrounds('images\\m_start_back2.jpg', win_width + 20, win_height + 20, -10, 0)
# manual_back = Backgrounds('images\\instr.jpg', win_width, win_height, 0, 0)
# select_back = Backgrounds('images\\select.jpg', win_width + 20, win_height + 20, -10, 0)
# pause_back = Backgrounds('images\\pause.jpg', win_width + 20, win_height, 0, 0)
# lose_back = Backgrounds('images\\lose.jpg', 710, 540, 0, 0)
# win_back = Backgrounds('images\\win.jpg', 710, 540, 0, 0)
# back_line = Screensaver(0, 0, 710, 30, BLACK_BLUE)
#
# text_back1 = Label(140, 0, 680, 40, BLACK_BLUE)
# text_back1.set_text(txt_welcome, 62, WHITE)
# text_back_select = Label(140, 0, 680, 40, GREY_BLUE)
# text_back_select.set_text(txt_select, 62, WHITE)
# text_back2 = Label(230, 5, 200, 50, (DARK_BLUE))
# text_back2.set_text(txt_win, 55, WHITE)
# text_back3 = Label(30, 60, 300, 40, DARK_BLUE)
# title_instr = Label(140, 0, 680, 40, BLACK_BLUE)
# title_instr.set_text(instr, 62, WHITE)
# txt_lives = Label(10, 0, 70, 30, BLACK_BLUE)
#
# texts = []
# for text in text_rules.values():
#     texts.append(text)
# rul1 = Rules(texts[0])
# rul2 = Rules(texts[1])
# rul3 = Rules(texts[2])
# rul4 = Rules(texts[3])
# rul5 = Rules(texts[4])
#
# menu_but = sprite.Group()
# button_start = Menu('images\\start.png', 550, 370, 130, 130)
# button_manual = Menu('images\\instruction.png', 380, 395, 110, 110)
# button_sound = Menu('images\\sound.png', 185, 365, 170, 170)
# menu_but.add(button_start, button_manual)
#
# button_back = Menu('images\\menu.png', 510, 400, 130, 135)
# select_but = sprite.Group()
# button_select1 = Menu('images\\select1.png', 170, 120, 190, 100)
# button_select2 = Menu('images\\select2.png', 170, 250, 190, 100)
# button_select3 = Menu('images\\select3.png', 170, 375, 190, 100)
# button_explore_universe = Menu('images\\explore.png', 400, 375, 190, 100)  # Add this image yourself
# button_back_s = Menu('images\\menu.png', 20, 425, 100, 100)
# select_but.add(button_select1, button_select2, button_select3, button_explore_universe, button_back_s)
#
# button_manual2 = Menu('images\\instruction.png', 100, 90, 120, 120)
# button_start2 = Menu('images\\start.png', 490, 60, 150, 150)
# button_back3 = Menu('images\\menu.png', 100, 370, 130, 135)
# button_unpause = Menu('images\\start.png', 350, 380, 150, 150)
# button_back_final = Menu('images\\menu.png', 30, 380, 130, 135)
# button_restart = Menu('images\\restart.png', 520, 390, 120, 120)
#
