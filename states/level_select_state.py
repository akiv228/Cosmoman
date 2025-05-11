from pygame import sprite
import pygame as pg
from .game_state import State
from grafics_classes import Backgrounds, Menu, Label
from .config import LevelSelectState as cfg
from grafic_elements import Star, NeonText, Button

class LevelSelectState(State):
    def __init__(self, game):
        super().__init__(game)
        self.stars = [Star(cfg.stars) for _ in range(cfg.stars['count'])]
        self.neon_text = NeonText(cfg.title)
        button_count = len(cfg.buttons['names'])
        total_height = (button_count * cfg.buttons['height']) + ((button_count - 1) * cfg.buttons['vertical_spacing'])
        start_y = cfg.buttons['top_margin']
        self.buttons = [Button(name, start_y + i * (cfg.buttons['height'] + cfg.buttons['vertical_spacing']), cfg.buttons)
                        for i, name in enumerate(cfg.buttons['names'])]
        for i, button in enumerate(self.buttons):
            button.set_active(i <= self.game.completed_difficulties)
        self.button_back = Menu(*cfg.back)
        self.music = cfg.music

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.button_back.rect.collidepoint(e.pos):
                    from .menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
                for button in self.buttons:
                    if button.rect.collidepoint(e.pos) and button.active:
                        difficulty_map = {"LEVEL1": "EASY", "LEVEL2": "MEDIUM", "LEVEL3": "HARD", "EXPLORE UNIVERSITY": "EXPLORE"}
                        from .play_state import PlayState
                        from starfield import IntroState
                        self.game.set_state(IntroState(self.game, lambda g: PlayState(g, difficulty_map[button.text])))
                        # self.game.set_state(PlayState(self.game, difficulty_map[button.text]))

    def update(self):
        for star in self.stars:
            star.update()
        self.neon_text.update()
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

    def render(self, window):
        window.fill((0, 0, 0))
        for star in self.stars:
            star.draw(window)
        self.neon_text.draw(window)
        for button in self.buttons:
            button.draw(window)
        self.button_back.reset(window)