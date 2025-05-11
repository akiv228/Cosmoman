from pygame import sprite
import pygame as pg
from .game_state import State
from grafics_classes import Backgrounds, Menu, Label
from .config_state import MenuState as cfg
from game_music import mixer
from grafic_elements import Star, NeonText, Button

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.stars = [Star(cfg.stars) for _ in range(cfg.stars['count'])]
        self.neon_text = NeonText(cfg.title)
        button_count = len(cfg.buttons['names'])
        total_height = (button_count * cfg.buttons['height']) + ((button_count - 1) * cfg.buttons['vertical_spacing'])
        start_y = cfg.buttons['top_margin']
        self.buttons = [Button(name, start_y + i * (cfg.buttons['height'] + cfg.buttons['vertical_spacing']), cfg.buttons)
                        for i, name in enumerate(cfg.buttons['names'])]
        self.button_sound = Menu(*cfg.sound)
        self.cross_image = cfg.cross.convert_alpha()
        self.cross_image = pg.transform.scale(self.cross_image, (40, 40))
        self.cross_rect = self.cross_image.get_rect()
        self.cross_rect.center = (self.button_sound.rect.right - 80, self.button_sound.rect.centery)
        self.check_sound = 0
        self.music = cfg.music

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.rect.collidepoint(e.pos):
                        if button.text == "START":
                            from .level_select_state import LevelSelectState
                            self.game.set_state(LevelSelectState(self.game))
                        elif button.text == "CONTROLS":
                            from .popup_state import PopupState
                            self.game.set_state(PopupState(self.game, self))
                if self.button_sound.rect.collidepoint(e.pos):
                    self.check_sound += 1
                    if self.check_sound % 2:
                        mixer.music.pause()
                    else:
                        mixer.music.unpause()

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
        self.button_sound.reset(window)
        if self.check_sound % 2:
            window.blit(self.cross_image, self.cross_rect)