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
        self.duration = 4.0  # 3-second transition
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
        speed_multiplier = 1 - progress  # Linearly decreases from 1 to 0
        self.starfield.update(speed_multiplier)  # Update starfield with this multiplier

    def render(self, window):
        self.starfield.draw()

