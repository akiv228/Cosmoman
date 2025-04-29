import pygame as pg
from states.game_state import State
from grafics_classes import Backgrounds, Menu

class LoseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = Backgrounds('images\\lose.jpg', 710, 540, 0, 0)
        self.button_back = Menu('images\\menu.png', 30, 380, 130, 135)
        self.button_restart = Menu('images\\restart.png', 520, 390, 120, 120)

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                x, y = e.pos
                if self.button_back.collidepoint(x, y):
                    from states.menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
                elif self.button_restart.collidepoint(x, y):
                    from states.level_select_state import LevelSelectState
                    self.game.set_state(LevelSelectState(self.game))

    def update(self):
        pass

    def render(self, window):
        self.background.reset(window)
        window.blit(pg.transform.scale(pg.image.load('images\\textlose.png'), (650, 600)), (15, -200))
        self.button_back.reset(window)
        self.button_restart.reset(window)