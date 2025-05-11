import pygame as pg
from states.game_state import State
from grafics_classes_stash import Backgrounds, Menu, Label
from .config_state import WinState as cfg

class WinState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = Backgrounds(*cfg.bg)
        self.text_back = Label(*cfg.back_label)
        self.text_back.set_text(*cfg.per_init_back_label)
        self.button_back = Menu(*cfg.back)
        self.button_restart = Menu(*cfg.restart)

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.button_back.collidepoint(*e.pos):
                    from states.menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
                elif self.button_restart.collidepoint(*e.pos):
                    from states.level_select_state import LevelSelectState
                    self.game.set_state(LevelSelectState(self.game))

    def update(self):
        pass

    def render(self, window):
        self.background.reset(window)
        self.text_back.draw(window, 0, 0)
        self.button_back.reset(window)
        self.button_restart.reset(window)
