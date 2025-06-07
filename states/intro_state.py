import pygame as pg
import random
from states.game_state import State
from .config_state import IntroState as cfg
from grafics.grafics_for_intro import Starfield
from states.play_state import PlayState


class IntroState(State):
    def __init__(self, game, next_state_creator, color_set=None):
        super().__init__(game)
        self.color_set = color_set if color_set else random.choice(list(cfg.color_sets.keys()))
        self.config = self.generate_config()
        self.timer = 0
        self.duration = self.config['duration']
        self.starfield = Starfield(game.window, self.config)
        self.next_state_creator = next_state_creator

    def generate_config(self):
        color_set = cfg.color_sets[self.color_set]
        ranges = cfg.starfield_ranges
        num_colors = len(color_set)
        k = random.randint(1, num_colors) if num_colors < 3 else random.randint(3, num_colors)
        return {
            'num_stars': random.randint(*ranges['num_stars']),
            'vel_min': random.uniform(*ranges['vel_min']),
            'vel_max': random.uniform(*ranges['vel_max']),
            'colors': random.sample(color_set, k=k),
            'scale_pos': random.randint(*ranges['scale_pos']),
            'alpha': random.randint(*ranges['alpha']),
            'rotation_base': random.uniform(*ranges['rotation_base']),
            'duration': cfg.default_duration
        }

    def handle_events(self, events):
        for e in events:
            if e.type == pg.QUIT:
                self.game.running = False

    def update(self):
        dt = self.game.clock.get_time() / 1000.0
        self.timer += dt
        if self.timer >= self.duration:
            self.game.set_state(self.next_state_creator(self.game))
        progress = self.timer / self.duration
        speed_multiplier = 0.2 - progress
        rotation_speed = self.config['rotation_base'] * (1 + progress * 2)
        alpha = 1 - progress
        self.starfield.update(speed_multiplier, rotation_speed)
        self.alpha = alpha

    def render(self, window):
        self.starfield.draw(self.alpha)

    def enter(self):
        pass