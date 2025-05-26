import pygame as pg
from states.game_state import State
from grafics_classes_stash import Backgrounds, Menu
from .config_state import PauseState as cfg
from config import win_width as W, win_height as H

class PauseState(State):
    def __init__(self, game, previous_state):
        super().__init__(game)
        self.previous_state = previous_state

        # Создаем накладку
        self.overlay = pg.Surface((W, H), pg.SRCALPHA)
        self.overlay.fill(cfg.overlay_color)

        # Создаем окно паузы
        self.pause_window = pg.Surface(cfg.pause_window_size, pg.SRCALPHA)
        self.pause_window.fill(cfg.pause_window_color)
        self.window_rect = self.pause_window.get_rect(center=(W // 2, H // 2))

        # Создаем текст "PAUSE"
        self.font = pg.font.Font(None, cfg.pause_text['font_size'])
        self.pause_text_surface = self.font.render(cfg.pause_text['text'], True, cfg.pause_text['color'])
        text_rect = self.pause_text_surface.get_rect()
        if cfg.pause_text['position']['x'] == 'center':
            text_rect.centerx = self.window_rect.centerx
        else:
            text_rect.x = self.window_rect.left + cfg.pause_text['position']['x']
        text_rect.y = self.window_rect.top + cfg.pause_text['position']['y']
        self.pause_text_rect = text_rect

        # Вычисляем центральную Y-координату ряда кнопок (ниже текста)
        button_row_center_y = self.pause_text_rect.bottom + cfg.button_row_gap

        # Вычисляем общую ширину кнопок с учетом отступов
        total_width = sum(button['size'][0] for button in cfg.buttons) + cfg.button_spacing * (len(cfg.buttons) - 1)
        start_x = self.window_rect.left + (self.window_rect.width - total_width) // 2 + 20

        # Создаем кнопки с индивидуальными размерами
        self.buttons = []
        current_x = start_x
        for button_cfg in cfg.buttons:
            width, height = button_cfg['size']
            x = current_x
            y = button_row_center_y - height // 2  # Центрируем каждую кнопку по вертикали
            button = Menu(button_cfg['image'], x, y, width, height)
            self.buttons.append(button)
            current_x += width + cfg.button_spacing

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                for button, button_cfg in zip(self.buttons, cfg.buttons):
                    if button.collidepoint(*mouse_pos):
                        action = button_cfg['action']
                        if action == 'unpause':
                            self.game.set_state(self.previous_state)
                            self.game.toggle_sound()
                        elif action == 'home':
                            from states.menu_state import MenuState
                            self.game.set_state(MenuState(self.game))
                            self.game.toggle_sound()
                        elif action == 'info':
                            pass  # Действие для кнопки info, если нужно

    def update(self):
        pass

    def render(self, window):
        self.previous_state.render(window)
        window.blit(self.overlay, (0, 0))
        window.blit(self.pause_window, self.window_rect)
        window.blit(self.pause_text_surface, self.pause_text_rect)
        for button in self.buttons:
            button.reset(window)