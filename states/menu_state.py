from pygame import sprite
import pygame as pg
from states.game_state import State
from states.level_select_state import LevelSelectState
from constants import win_width, win_height, BLACK_BLUE, WHITE, txt_welcome
from grafics_classes import Backgrounds, Menu, Label
from game_music import mixer

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = Backgrounds('images\\m_start_back2.jpg', win_width + 20, win_height + 20, -10, 0)
        self.menu_but = sprite.Group()
        self.button_start = Menu('images\\start.png', 550, 370, 130, 130)
        self.button_manual = Menu('images\\instruction.png', 380, 395, 110, 110)
        self.button_sound = Menu('images\\sound.png', 185, 365, 170, 170)
        self.menu_but.add(self.button_start, self.button_manual)
        self.text_back = Label(140, 0, 680, 40, BLACK_BLUE)
        self.text_back.set_text(txt_welcome, 62, WHITE)
        self.check_sound = 0
        mixer.music.load('sound\\fon1.mp3')
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                x, y = e.pos
                if self.button_start.collidepoint(x, y):
                    from states.level_select_state import LevelSelectState
                    self.game.set_state(LevelSelectState(self.game))
                elif self.button_manual.collidepoint(x, y):
                    pass  # Можно добавить InstructionState
                elif self.button_sound.collidepoint(x, y):
                    self.check_sound += 1
                    if self.check_sound % 2:
                        mixer.music.pause()
                    else:
                        mixer.music.unpause()

    def update(self):
        pass # Логика обновления меню, если нужна (например, анимации)

    def render(self, window):
        self.background.reset(window)
        self.button_sound.reset(window)
        self.menu_but.draw(window)
        self.text_back.draw(window, 0, -7)


