import pygame as pg
from states.game_state import State
from grafics_classes_stash import Backgrounds, Menu
from .config_state import PauseState as cfg

class PauseState(State):
    def __init__(self, game, previous_state):
        super().__init__(game)
        self.previous_state = previous_state
        self.background = Backgrounds(*cfg.bg)
        self.button_unpause = Menu(*cfg.resume)
        self.button_back = Menu(*cfg.back)

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.button_unpause.collidepoint(*e.pos):
                    self.game.set_state(self.previous_state)
                elif self.button_back.collidepoint(*e.pos):
                    from states.menu_state import MenuState
                    self.game.set_state(MenuState(self.game))

    def update(self):
        pass

    def render(self, window):
        self.background.reset(window)
        self.button_unpause.reset(window)
        self.button_back.reset(window)


