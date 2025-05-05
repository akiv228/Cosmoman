import pygame as pg
from .game_state import State
from grafics_classes import Backgrounds, Menu
from .config import LoseState as cfg

class LoseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = Backgrounds(*cfg.bg)
        self.button_back = Menu(*cfg.back)
        self.button_restart = Menu(*cfg.reset)

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.button_back.collidepoint(*e.pos):
                    from .menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
                elif self.button_restart.collidepoint(*e.pos):
                    from .level_select_state import LevelSelectState
                    self.game.set_state(LevelSelectState(self.game))


    def update(self):
        pass

    def render(self, window):
        self.background.reset(window)
        window.blit(pg.transform.scale(cfg.lose_label, (650, 600)), (15, -200))
        self.button_back.reset(window)
        self.button_restart.reset(window)