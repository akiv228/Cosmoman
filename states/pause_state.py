import pygame as pg
from states.game_state import State
from grafics_classes import Backgrounds, Menu
from constants import win_width, win_height

class PauseState(State):
    def __init__(self, game, previous_state):
        super().__init__(game)
        self.previous_state = previous_state
        self.background = Backgrounds('images\\pause.jpg', win_width + 20, win_height, 0, 0)
        self.button_unpause = Menu('images\\start.png', 350, 380, 150, 150)
        self.button_back = Menu('images\\menu.png', 100, 370, 130, 135)

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                x, y = e.pos
                if self.button_unpause.collidepoint(x, y):
                    self.game.set_state(self.previous_state)
                elif self.button_back.collidepoint(x, y):
                    from states.menu_state import MenuState
                    self.game.set_state(MenuState(self.game))

    def update(self):
        pass

    def render(self, window):
        self.background.reset(window)
        self.button_unpause.reset(window)
        self.button_back.reset(window)


