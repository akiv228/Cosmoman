import pygame as pg
from grafics.elements_for_menu_select_login import NeonText, Button, Star
from .game_state import State
from .config_state import MenuState as cfg
from game_music import mixer


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.stars = [Star(cfg.stars) for _ in range(cfg.stars['count'])]
        self.neon_text = NeonText(cfg.title)
        button_count = len(cfg.buttons['names'])
        start_y = cfg.buttons['top_margin']
        self.buttons = [Button(name, start_y + i * (cfg.buttons['height'] + cfg.buttons['vertical_spacing']), cfg.buttons)
                        for i, name in enumerate(cfg.buttons['names'])]
        # self.button_sound = Menu(*cfg.sound)
        # self.cross_image = cfg.cross.convert_alpha()
        # self.cross_image = pg.transform.scale(self.cross_image, (40, 40))
        # self.cross_rect = self.cross_image.get_rect()
        # self.cross_rect.center = (self.button_sound.rect.right - 80, self.button_sound.rect.centery)
        # self.check_sound = 0
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
                        elif button.text == "RATING":
                            from states.win_state import WinState
                            self.game.set_state(WinState(self.game))
                        elif button.text == "FOUND PLANETS":
                            from states.lose_state import LoseState
                            self.game.set_state(LoseState(self.game))
                # if self.button_sound.rect.collidepoint(e.pos):
                #     self.game.toggle_sound()

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_m:
                    self.game.toggle_sound()  #

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
        # self.button_sound.reset(window)

        # if not self.game.sound_enabled:
        #     window.blit(self.cross_image, self.cross_rect)