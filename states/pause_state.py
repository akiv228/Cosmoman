import pygame as pg
from states.game_state import State
from grafics_classes_stash import Backgrounds, Menu
from .config_state import PauseState as cfg
from config import win_width as W, win_height as H


class PauseState(State):
    def __init__(self, game, previous_state):
        super().__init__(game)
        self.previous_state = previous_state

        # Создаем полупрозрачную поверхность для затемнения
        self.overlay = pg.Surface((W, H), pg.SRCALPHA)
        self.overlay.fill((0, 0, 0, 100))  # Черный с прозрачностью 50%

        # Создаем прямоугольник для окна паузы
        self.pause_window = pg.Surface((600, 300), pg.SRCALPHA)
        self.pause_window.fill((50, 50, 50, 200))  # Темно-серый с небольшой прозрачностью
        self.window_rect = self.pause_window.get_rect(center=(W // 2, H // 2))


        # self.button_unpause = Menu(*cfg.resume)
        # self.button_back = Menu(*cfg.back)

        button_width, button_height = 100, 50
        self.button_unpause = Menu(
            'images\\start.png',
            self.window_rect.centerx - button_width // 2,
            self.window_rect.centery - 40, button_width, button_height
        )

        self.button_back = Menu(
            'images\\menu.png',
            self.window_rect.centerx - button_width // 2,
            self.window_rect.centery + 40, button_width, button_height
        )

        # Текст "Пауза"
        self.font = pg.font.Font(None, 48)
        self.pause_text = self.font.render("ПАУЗА", True, (255, 255, 255))
        self.text_rect = self.pause_text.get_rect(center=(self.window_rect.centerx, self.window_rect.top + 50))

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                # Преобразуем координаты мыши относительно окна
                mouse_pos = pg.mouse.get_pos()
                if self.button_unpause.collidepoint(*mouse_pos):
                    self.game.set_state(self.previous_state)
                elif self.button_back.collidepoint(*mouse_pos):
                    from states.menu_state import MenuState
                    self.game.set_state(MenuState(self.game))

    def update(self):
        pass

    def render(self, window):
        # Сначала рисуем предыдущее состояние (игровой экран)
        self.previous_state.render(window)

        # Затем рисуем затемнение
        window.blit(self.overlay, (0, 0))

        # Рисуем окно паузы
        window.blit(self.pause_window, self.window_rect)

        # Рисуем текст и кнопки
        window.blit(self.pause_text, self.text_rect)
        self.button_unpause.reset(window)
        self.button_back.reset(window)
