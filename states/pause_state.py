import pygame as pg
from states.game_state import State
from grafics_classes_stash import Backgrounds, Menu
from .config_state import PauseState as cfg
from config import win_width as W, win_height as H


class PauseState(State):
    def __init__(self, game, previous_state):
        super().__init__(game)
        self.previous_state = previous_state

        # Полупрозрачное затемнение
        self.overlay = pg.Surface((W, H), pg.SRCALPHA)
        self.overlay.fill((0, 0, 0, 200))  # Черный с прозрачностью 50%

        # Окно паузы
        self.pause_window = pg.Surface((600, 300), pg.SRCALPHA)
        self.pause_window.fill((50, 50, 50, 200))
        self.window_rect = self.pause_window.get_rect(center=(W // 2, H // 2))

        # Параметры кнопок
        button_width, button_height = 80, 85
        total_buttons_width = 3 * button_width  # Ширина всех трех кнопок
        spacing = 50  # Расстояние между кнопками

        # Вычисляем начальную позицию для первой кнопки (чтобы все три были по центру)
        start_x = self.window_rect.centerx - (total_buttons_width + spacing * 2) // 2 + 30

        # Создаем кнопки в горизонтальный ряд
        self.button_home = Menu(
            'images\\home.png',
            start_x,
            self.window_rect.centery - (button_height - 80) // 2,
            button_width,
            button_height
        )

        self.button_info = Menu(
            'images\\info.png',
            start_x + button_width + spacing,
            self.window_rect.centery - (button_height - 80) // 2,
            button_width,
            button_height
        )

        self.button_unpause = Menu(
            'images\\pause_play.png',
            start_x + 2 * (button_width + spacing),
            self.window_rect.centery - (button_height - 80) // 2,
            button_width,
            button_height
        )
        # Текст "Пауза"
        self.font = pg.font.Font(None, 70)
        self.pause_text = self.font.render("PAUSE", True, (255, 255, 255))
        self.text_rect = self.pause_text.get_rect(center=(self.window_rect.centerx, self.window_rect.top + 50))

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.button_unpause.collidepoint(*mouse_pos):
                    self.game.set_state(self.previous_state)
                    self.game.toggle_sound()
                elif self.button_home.collidepoint(*mouse_pos):
                    from states.menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
                    self.game.toggle_sound()
                elif self.button_info.collidepoint(*mouse_pos):
                    # Добавьте обработку кнопки info
                    pass

    def update(self):
        pass

    def render(self, window):
        # Рендерим предыдущее состояние
        self.previous_state.render(window)

        # Затемнение
        window.blit(self.overlay, (0, 0))

        # Окно паузы
        window.blit(self.pause_window, self.window_rect)
        window.blit(self.pause_text, self.text_rect)

        # Кнопки
        self.button_home.reset(window)
        self.button_info.reset(window)
        self.button_unpause.reset(window)