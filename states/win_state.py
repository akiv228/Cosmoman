import time

import pygame as pg
import requests
from grafics.planetfons_lose_win import PlanetSystem
from states.game_state import State
from grafics.grafics_elements import ImageButton
from grafics.elements_for_menu_select_login import NeonText
from .config_state import WinState as cfg
from config import win_width as W, win_height as H, serv


class WinState(State):
    def __init__(self, game, from_state):
        super().__init__(game)
        self.from_state = from_state
        self.planet_system = PlanetSystem((W, H))
        self.dark_surface = pg.Surface((W, H))
        self.dark_surface.set_alpha(120)
        self.dark_surface.fill((0, 0, 0))
        self.init_ui_elements()

        self.font_header = pg.font.Font(None, 36)
        self.font_row = pg.font.Font(None, 28)
        self.last_update_time = 0
        self.leaderboard_data = []
        self.load_leaderboard()
        self.update_interval = 5000  # 5 секунд в миллисекундах

    def init_ui_elements(self):
        self.ui_elements = {
            'Menu': {
                'texts': [NeonText(cfg.title2)],
                'buttons': [ImageButton(*cfg.back2)]
            },
            'Play': {
                'texts': [NeonText(cfg.title1)],
                'buttons': [ImageButton(*cfg.back), ImageButton(*cfg.restart)]
            }
        }

    def load_leaderboard(self):
        try:
            response = requests.get(
                f'http://{serv["host"]}:{serv["port"]}/scoreboard',
                params={'t': int(time.time())}  # Добавляем timestamp для избежания кэширования
            )
            if response.status_code == 200:
                self.leaderboard_data = response.json()
            else:
                print(f"Сервер вернул код {response.status_code}")
        except requests.RequestException as e:
            print(f"Ошибка загрузки рейтинга: {e}")
            # Можно сохранить предыдущие данные или показать сообщение об ошибке

    def draw_leaderboard(self, window):
        if not self.leaderboard_data:
            return

        # Отрисовка заголовка таблицы
        title = self.font_header.render("Toпы", True, (255, 255, 255))
        window.blit(title, (W // 2 - title.get_width() // 2, 300))

        start_y = 350
        row_height = 40
        columns = [
            ("Место", 100),
            ("Игрок", 200),
            ("Счет", 150)
        ]

        # Отрисовка заголовков столбцов
        for i, (col_name, col_width) in enumerate(columns):
            x = W // 2 - 250 + sum(w for _, w in columns[:i])
            header = self.font_row.render(col_name, True, (255, 215, 0))
            window.blit(header, (x, start_y))

        # Линия под заголовками
        pg.draw.line(window, (255, 255, 255),
                     (W // 2 - 250, start_y + 35),
                     (W // 2 + 250, start_y + 35), 2)

        for i, row in enumerate(self.leaderboard_data[:10]):
            y = start_y + 40 + i * row_height
            rank, username, _, score, pids = row
            rank = i + 1

            rank_text = self.font_row.render(str(rank), True, (255, 255, 255))
            window.blit(rank_text, (W // 2 - 250 + 50 - rank_text.get_width() // 2, y))

            name_text = self.font_row.render(username, True, (255, 255, 255))
            window.blit(name_text, (W // 2 - 150, y))

            score_text = self.font_row.render(f"{score:.1f}", True, (255, 255, 255))
            window.blit(score_text, (W // 2 + 150 - score_text.get_width() // 2, y))

            if i < len(self.leaderboard_data) - 1:
                pg.draw.line(window, (100, 100, 100),
                             (W // 2 - 250, y + row_height - 5),
                             (W // 2 + 250, y + row_height - 5), 1)

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                self.handle_button_clicks(e.pos)

    def handle_button_clicks(self, mouse_pos):
        buttons = self.ui_elements[self.from_state]['buttons']

        for button in buttons:
            if button.collidepoint(*mouse_pos):
                self.handle_button_action(button)
                break

    def handle_button_action(self, button):
        from states.menu_state import MenuState
        from states.level_select_state import LevelSelectState

        button_actions = {
            'back': lambda: self.game.set_state(MenuState(self.game)),
            'back2': lambda: self.game.set_state(MenuState(self.game)),
            'restart': lambda: self.game.set_state(LevelSelectState(self.game))
        }

        if button == self.ui_elements['Menu']['buttons'][0]:  # back2
            button_actions['back2']()
        elif button == self.ui_elements['Play']['buttons'][0]:  # back
            button_actions['back']()
        elif (self.from_state == 'Play' and
              button == self.ui_elements['Play']['buttons'][1]):  # restart
            button_actions['restart']()

    # def update(self):
    #     self.planet_system.update()
    #
    #
    #     for text in self.ui_elements[self.from_state]['texts']:
    #         text.update()


    def update(self):
        self.planet_system.update()

        current_time = pg.time.get_ticks()
        if current_time - self.last_update_time > self.update_interval:
            self.load_leaderboard()
            self.last_update_time = current_time

        for text in self.ui_elements[self.from_state]['texts']:
            text.update()


    def render(self, window):
        self.planet_system.draw(window)
        window.blit(self.dark_surface, (0, 0))
        self.draw_leaderboard(window)

        for text in self.ui_elements[self.from_state]['texts']:
            text.draw(window)

        for button in self.ui_elements[self.from_state]['buttons']:
            button.draw(window)

    def enter(self):
        self.load_leaderboard()
