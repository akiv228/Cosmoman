from pygame import sprite
import pygame as pg
from states.game_state import State
from constants import win_width, win_height, GREY_BLUE, WHITE, txt_select
from grafics_classes import Backgrounds, Menu, Label

class LevelSelectState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = Backgrounds('images\\select.jpg', win_width + 20, win_height + 20, -10, 0)
        self.select_but = sprite.Group()
        self.button_select1 = Menu('images\\select1.png', 170, 120, 190, 100)
        self.button_select2 = Menu('images\\select2.png', 170, 250, 190, 100)
        self.button_select3 = Menu('images\\select3.png', 170, 375, 190, 100)
        self.button_explore = Menu('images\\explore.png', 400, 375, 190, 100)
        self.button_back = Menu('images\\menu.png', 20, 425, 100, 100)
        self.select_but.add(self.button_select1, self.button_select2, self.button_select3,
                            self.button_explore, self.button_back)
        self.text_back = Label(140, 0, 680, 40, GREY_BLUE)
        self.text_back.set_text(txt_select, 62, WHITE)

    def handle_events(self, events):
        from states.play_state import PlayState
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                x, y = e.pos
                if self.button_back.collidepoint(x, y):
                    from states.menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
                elif self.button_select1.collidepoint(x, y) and self.game.completed_difficulties >= 0:
                    self.game.set_state(PlayState(self.game, 'EASY'))
                elif self.button_select2.collidepoint(x, y) and self.game.completed_difficulties >= 1:
                    self.game.set_state(PlayState(self.game, 'MEDIUM'))
                elif self.button_select3.collidepoint(x, y) and self.game.completed_difficulties >= 2:
                    self.game.set_state(PlayState(self.game, 'HARD'))
                elif self.button_explore.collidepoint(x, y) and self.game.completed_difficulties >= 3:
                    self.game.set_state(PlayState(self.game, 'EXPLORE'))

    def update(self):
        pass

    def render(self, window):
        self.background.reset(window)
        self.text_back.draw(window, 0, 0)
        if self.game.completed_difficulties >= 0:
            self.button_select1.reset(window)
        if self.game.completed_difficulties >= 1:
            self.button_select2.reset(window)
        if self.game.completed_difficulties >= 2:
            self.button_select3.reset(window)
        if self.game.completed_difficulties >= 3:
            self.button_explore.reset(window)
        self.button_back.reset(window)
