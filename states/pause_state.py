import pygame as pg
from states.game_state import State
from grafics_classes_stash import Menu
from .config_state import PauseState as cfg


class PauseState(State):
    def __init__(self, game, previous_state):
        super().__init__(game)
        self.previous_state = previous_state

        # Создаем полупрозрачное затемнение
        self.overlay = pg.Surface((self.game.WIDTH, self.game.HEIGHT), pg.SRCALPHA)
        self.overlay.fill(cfg.overlay_color)

        # Создаем окно паузы
        self.window = pg.Surface((cfg.window_width, cfg.window_height), pg.SRCALPHA)
        self.window.fill(cfg.window_color)
        if hasattr(cfg, 'window_border_radius'):
            # Если поддерживается, делаем скругленные углы
            pg.draw.rect(self.window, cfg.window_color,
                         (0, 0, cfg.window_width, cfg.window_height),
                         border_radius=cfg.window_border_radius)
        self.window_rect = self.window.get_rect(center=(self.game.WIDTH // 2, self.game.HEIGHT // 2))

        # Создаем текст "Пауза"
        self.font = pg.font.Font(None, cfg.pause_text['font_size'])
        self.pause_text = self.font.render(cfg.pause_text['text'], True, cfg.pause_text['color'])
        self.text_rect = self.pause_text.get_rect(
            centerx=self.window_rect.centerx,
            y=self.window_rect.y + cfg.pause_text['y_offset']
        )

        # Создаем кнопки (три в ряд)
        self.buttons = []
        total_buttons_width = sum(btn['width'] for btn in cfg.buttons)
        spacing = (cfg.window_width - total_buttons_width) // (len(cfg.buttons) + 1)

        x_offset = self.window_rect.x + spacing
        for btn_cfg in cfg.buttons:
            btn = Menu(
                btn_cfg['image'],
                btn_cfg['width'],
                btn_cfg['height'],
                x_offset,
                self.window_rect.y + btn_cfg['y'],
                action=btn_cfg['action']
            )
            self.buttons.append(btn)
            x_offset += btn_cfg['width'] + spacing

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                for btn in self.buttons:
                    if btn.collidepoint(*mouse_pos):
                        self.handle_button_action(btn.action)
                        break

    def handle_button_action(self, action):
        if action == 'resume':
            self.game.set_state(self.previous_state)
        elif action == 'menu':
            from states.menu_state import MenuState
            self.game.set_state(MenuState(self.game))
        elif action == 'restart':
            from states.play_state import PlayState
            self.game.set_state(PlayState(self.game, self.previous_state.level.difficulty))

    def update(self):
        pass

    def render(self, window):
        # Рендерим предыдущее состояние (игровой экран)
        self.previous_state.render(window)

        # Затемнение
        window.blit(self.overlay, (0, 0))

        # Окно паузы
        window.blit(self.window, self.window_rect)

        # Текст "Пауза"
        window.blit(self.pause_text, self.text_rect)

        # Кнопки
        for btn in self.buttons:
            btn.reset(window)