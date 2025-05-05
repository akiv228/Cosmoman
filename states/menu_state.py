from pygame import sprite
import pygame as pg
from .game_state import State
from grafics_classes import Backgrounds, Menu, Label
from .config import MenuState as cfg
from game_music import mixer

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = Backgrounds(*cfg.bg)
        self.menu_but = sprite.Group()
        self.button_start = Menu(*cfg.start)
        self.button_manual = Menu(*cfg.manual)
        self.button_sound = Menu(*cfg.sound)
        self.menu_but.add(self.button_start, self.button_manual)
        self.text_back = Label(*cfg.label)
        self.text_back.set_text(*cfg.greetings)
        self.cross_image = cfg.cross.convert_alpha()
        self.cross_image = pg.transform.scale(self.cross_image, (40, 40))
        self.cross_rect = self.cross_image.get_rect()
        self.cross_rect.center = (self.button_sound.rect.right - 80, self.button_sound.rect.centery)
        
        self.check_sound = 0
        if not game.music_flag:
            mixer.music.load(cfg.music)
            mixer.music.set_volume(0.2)
            mixer.music.play(-1)
            game.music_flag = 1

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.button_start.collidepoint(*e.pos):
                    from .level_select_state import LevelSelectState
                    self.game.set_state(LevelSelectState(self.game))
                elif self.button_manual.collidepoint(*e.pos):
                    from .popup_state import PopupState
                    self.game.set_state(PopupState(self.game, self))
                elif self.button_sound.collidepoint(*e.pos):
                    self.check_sound += 1
                    if self.check_sound % 2:
                        mixer.music.pause()
                    else:
                        mixer.music.unpause()

    def update(self):
        pass

    def render(self, window):
        self.background.reset(window)
        self.button_sound.reset(window)
        self.menu_but.draw(window)
        self.text_back.draw(window, 0, -7)
        if self.check_sound % 2:
            window.blit(self.cross_image, self.cross_rect)