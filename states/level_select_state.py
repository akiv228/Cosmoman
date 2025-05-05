from pygame import sprite
import pygame as pg
from states.game_state import State
from grafics_classes import Backgrounds, Menu, Label
from .config import LevelSelectState as cfg

class LevelSelectState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = Backgrounds(*cfg.bg)
        self.select_but = sprite.Group()
        self.button_select1, self.button_select2 = Menu(*cfg.btn[0]), Menu(*cfg.btn[1])
        self.button_select3, self.button_explore = Menu(*cfg.btn[2]), Menu(*cfg.explore)
        self.button_back = Menu(*cfg.back)
        self.select_but.add(self.button_select1, self.button_select2, self.button_select3,
                            self.button_explore, self.button_back)
        self.text_back = Label(*cfg.pre_init_back_label)
        self.text_back.set_text(*cfg.back_label)

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                set_state = self.game.set_state
                level_above = self.game.completed_difficulties
                if not self.button_back.collidepoint(*e.pos): from .play_state import PlayState
                if self.button_back.collidepoint(*e.pos):
                    from .menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
                elif self.button_select1.collidepoint(*e.pos) and level_above >= 0: set_state(PlayState(self.game, 'EASY'))
                elif self.button_select2.collidepoint(*e.pos) and level_above >= 1: set_state(PlayState(self.game, 'MEDIUM'))
                elif self.button_select3.collidepoint(*e.pos) and level_above >= 2: set_state(PlayState(self.game, 'HARD'))
                elif self.button_explore.collidepoint(*e.pos) and level_above >= 3: set_state(PlayState(self.game, 'EXPLORE'))

    def update(self):
        pass

    def render(self, window):
        self.background.reset(window)
        self.text_back.draw(window, 0, 0)
        button_rules = {
            0: self.button_select1,
            1: self.button_select2,
            2: self.button_select3,
            3: self.button_explore
        }
        for level, button in button_rules.items():
            if self.game.completed_difficulties >= level: button.reset(window)
        self.button_back.reset(window)
