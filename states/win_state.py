import pygame as pg

from planet_screen import PlanetSystem
from states.game_state import State
from grafics_classes_stash import Backgrounds, Menu, Label
from grafics.elements_for_menu_select_login import NeonText, Button, Star
from .config_state import WinState as cfg
from config import win_width as W, win_height as H


class WinState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = Backgrounds(*cfg.bg)
        # self.text_back = Label(*cfg.back_label)
        # self.text_back.set_text(*cfg.per_init_back_label)
        self.neon_text = NeonText(cfg.title)
        self.button_back = Menu(*cfg.back)
        self.button_restart = Menu(*cfg.restart)

        # Создаем систему планет для фона
        self.planet_system = PlanetSystem((W, H))

        # Затемнение фона для лучшей читаемости интерфейса
        self.dark_surface = pg.Surface((W, H))
        self.dark_surface.set_alpha(120)
        self.dark_surface.fill((0, 0, 0))

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
        # Обновляем систему планет
        self.planet_system.update()
        self.neon_text.update()

    def render(self, window):
        # Рисуем фон с планетами
        self.planet_system.draw(window)

        # Затемняем фон для интерфейса
        window.blit(self.dark_surface, (0, 0))

        # Рисуем интерфейс поверх
        # self.text_back.draw(window, 0, 0)
        self.button_back.reset(window)
        self.button_restart.reset(window)

        self.neon_text.draw(window)