import pygame as pg
import random
import math
import asyncio
import platform
from states.game_state import State

vec2, vec3 = pg.math.Vector2, pg.math.Vector3

# Configuration from config.py
from config import WIDTH, HEIGHT, COLORS, Z_DISTANCE, ALPHA, FPS

COLORS = 'blue cyan skyblue purple magenta'.split()
Z_DISTANCE = 100  # расстояние по оси z  с которого начнут двигаться звезды
ALPHA = 30

RES = WIDTH, HEIGHT
NUM_STARS = 1000  # Denser starfield
CENTER = vec2(WIDTH // 2, HEIGHT // 2)

class Star:
    def __init__(self, screen):
        self.screen = screen
        self.pos3d = self.get_initial_pos3d()
        self.vel = random.uniform(2.0, 5.0)  # Faster initial velocity
        self.color = random.choice(COLORS)
        self.screen_pos = vec2(0, 0)
        self.size = 5

    def get_initial_pos3d(self, scale_pos=35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * scale_pos
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = random.uniform(1, Z_DISTANCE)  # Random initial depth
        return vec3(x, y, z)

    def get_pos3d(self, scale_pos=35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * scale_pos
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = Z_DISTANCE
        return vec3(x, y, z)

    def update(self, speed_multiplier):
        self.pos3d.z -= self.vel * speed_multiplier
        if self.pos3d.z < 1:
            self.pos3d = self.get_pos3d()
        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.15 * self.pos3d.z)  # Larger stars
        self.pos3d.xy = self.pos3d.xy.rotate(0.5)

    def draw(self):
        s = self.size
        if (-s < self.screen_pos.x < WIDTH + s) and (-s < self.screen_pos.y < HEIGHT + s):
            pg.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))

class Starfield:
    def __init__(self, screen):
        self.screen = screen
        self.stars = [Star(screen) for _ in range(NUM_STARS)]
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(ALPHA)

    def update(self, speed_multiplier):
        for star in self.stars:
            star.update(speed_multiplier)
        self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)

    def draw(self):
        self.screen.blit(self.alpha_surface, (0, 0))
        for star in self.stars:
            star.draw()


class IntroState(State):
    def __init__(self, game, next_state_class):
        super().__init__(game)
        self.starfield = Starfield(game.window)
        self.timer = 0
        self.duration = 2.0  # 3-second transition
        self.next_state_class = next_state_class

    def handle_events(self, events):
        for e in events:
            if e.type == pg.QUIT:
                self.game.running = False

    # def update(self):
    #     dt = self.game.clock.get_time() / 1000.0
    #     self.timer += dt
    #     if self.timer >= self.duration:
    #         self.game.set_state(self.next_state_class(self.game))
    #     progress = self.timer / self.duration
    #     speed_multiplier = 0.6 - progress  # Deceleration effect
    #     self.starfield.update(speed_multiplier)
    def update(self):
        dt = self.game.clock.get_time() / 1000.0  # Time elapsed since last frame in seconds
        self.timer += dt  # Accumulate total time
        if self.timer >= self.duration:  # Check if transition is complete (4 seconds)
            self.game.set_state(self.next_state_class(self.game))  # Switch to next state
        progress = self.timer / self.duration  # Fraction of transition completed (0 to 1)
        speed_multiplier = 0.7 - progress  # Linearly decreases from 1 to 0
        # speed_multiplier = 0.5 - progress ** 2
        self.starfield.update(speed_multiplier)  # Update starfield with this multiplier

#     def update(self):
#         dt = self.game.clock.get_time() / 1000.0
#         self.timer += dt
#         if self.timer >= self.duration:
#             self.game.set_state(self.next_state_class(self.game))
#         progress = self.timer / self.duration
#         # Квадратичное замедление для более плавного эффекта
#         speed_multiplier = 1 - progress ** 2
#         # Увеличение вращения к концу
#         rotation_speed = self.config['rotation_base'] * (1 + progress * 2)
#         # Эффект растворения через затухание
#         alpha = 1 - progress
#         self.starfield.update(speed_multiplier, rotation_speed)
#         self.alpha = alpha

    def render(self, window):
        self.starfield.draw()






# import pygame as pg
# import random
# import math
# import asyncio
# import platform
# from states.game_state import State
#
# vec2, vec3 = pg.math.Vector2, pg.math.Vector3
#
# # Configuration from config.py
# from config import WIDTH, HEIGHT, COLORS, Z_DISTANCE, ALPHA, FPS
#
# RES = WIDTH, HEIGHT
# CENTER = vec2(WIDTH // 2, HEIGHT // 2)
# COLORS = 'blue cyan skyblue purple magenta'.split()
#
# class Star:
#     def __init__(self, screen, config):
#         self.screen = screen
#         self.config = config  # Сохраняем config как атрибут экземпляра
#         self.pos3d = self.get_initial_pos3d(config['scale_pos'])
#         self.vel = random.uniform(config['vel_min'], config['vel_max'])
#         self.color = random.choice(config['colors'])
#         self.screen_pos = vec2(0, 0)
#         self.size = 5
#
#     def get_initial_pos3d(self, scale_pos):
#         angle = random.uniform(0, 2 * math.pi)
#         radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * scale_pos
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         z = random.uniform(1, Z_DISTANCE)
#         return vec3(x, y, z)
#
#     def get_pos3d(self, scale_pos):
#         angle = random.uniform(0, 2 * math.pi)
#         radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * scale_pos
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         z = Z_DISTANCE
#         return vec3(x, y, z)
#
#     def update(self, speed_multiplier, rotation_speed):
#         self.pos3d.z -= self.vel * speed_multiplier
#         if self.pos3d.z < 1:
#             self.pos3d = self.get_pos3d(self.config['scale_pos'])  # Используем сохраненный config
#         self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
#         self.size = (Z_DISTANCE - self.pos3d.z) / (0.15 * self.pos3d.z)
#         self.pos3d.xy = self.pos3d.xy.rotate(rotation_speed)
#
#     def draw(self, alpha):
#         s = self.size
#         if (-s < self.screen_pos.x < WIDTH + s) and (-s < self.screen_pos.y < HEIGHT + s):
#             color = pg.Color(self.color)
#             color.a = int(alpha * 255)  # Применяем эффект затухания
#             pg.draw.rect(self.screen, color, (*self.screen_pos, self.size, self.size))
#
# class Starfield:
#     def __init__(self, screen, config):
#         self.screen = screen
#         self.stars = [Star(screen, config) for _ in range(config['num_stars'])]
#         self.alpha_surface = pg.Surface(RES)
#         self.alpha_surface.set_alpha(config['alpha'])
#
#     def update(self, speed_multiplier, rotation_speed):
#         for star in self.stars:
#             star.update(speed_multiplier, rotation_speed)
#         self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
#
#     def draw(self, alpha):
#         self.screen.blit(self.alpha_surface, (0, 0))
#         for star in self.stars:
#             star.draw(alpha)
#
# class IntroState(State):
#     def __init__(self, game, next_state_class):
#         super().__init__(game)
#         self.config = self.generate_config()
#         self.starfield = Starfield(game.window, self.config)
#         self.timer = 0
#         self.duration = self.config['duration']
#         self.next_state_class = next_state_class
#
#     def generate_config(self):
#         return {
#             'num_stars': random.randint(500, 1500),  # Случайное количество звезд
#             'vel_min': random.uniform(1.0, 3.0),     # Случайный диапазон скоростей
#             'vel_max': random.uniform(3.0, 6.0),
#             'colors': random.sample(COLORS, k=random.randint(3, len(COLORS))),
#             'scale_pos': random.randint(30, 40),     # Случайный масштаб позиции
#             'alpha': random.randint(20, 40),         # Случайная прозрачность следа
#             'rotation_base': random.uniform(0.2, 1.0),  # Случайная базовая скорость вращения
#             # 'duration': random.uniform(2.5, 3.0)     # Случайная продолжительность
#             'duration': 2.5
#         }
#
#     def handle_events(self, events):
#         for e in events:
#             if e.type == pg.QUIT:
#                 self.game.running = False
#
#     def update(self):
#         dt = self.game.clock.get_time() / 1000.0
#         self.timer += dt
#         if self.timer >= self.duration:
#             self.game.set_state(self.next_state_class(self.game))
#         progress = self.timer / self.duration
#         # Квадратичное замедление для более плавного эффекта
#         speed_multiplier = 1 - progress ** 2
#         # Увеличение вращения к концу
#         rotation_speed = self.config['rotation_base'] * (1 + progress * 2)
#         # Эффект растворения через затухание
#         alpha = 1 - progress
#         self.starfield.update(speed_multiplier, rotation_speed)
#         self.alpha = alpha
#
#     def render(self, window):
#         self.starfield.draw(self.alpha)