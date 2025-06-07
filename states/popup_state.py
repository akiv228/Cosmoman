import openai
import pygame as pg
import os

import requests

from grafics.elements_for_menu_select_login import NeonText
from grafics.planetfons_lose_win import PlanetSystem
from .game_state import State
from grafics.grafics_elements import ImageButton
from .config_state import PopupState as cfg
from .intro_state import IntroState
from config import W, H, WHITE, key, mapped

class PopupState(State):
    def __init__(self, game, parent_state, next_state_creator):
        super().__init__(game)
        self.parent_state = parent_state
        self.next_state_creator = next_state_creator
        try:
            diff = next_state_creator(self.game).next_state_creator(self.game).level.difficulty
            print(mapped[diff])
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": f"состав короткую историю без эмодзи и символов форматирования с космонавтом для прохождения {mapped[diff]} длиной примерно в 100 символов"}
                ],
                "temperature": 0.7,
            }
            res = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data)
            self.payload = ["history got level " + diff + ":"] + res.json()['choices'][0]['message']['content'].split('.')
            self.button_back = ImageButton(*cfg.back2)
        except:
            self.payload = [
            "Приветствуем!",
            "Вы попали в космическое приключение.",
            "Подготовьте свой корабль к масштабному путешествию.",
            "Отправляйтесь в соседнюю галактику исследовать её планеты.",
            "",
            "Управление:",
            "- Стрелочки — движение",
            "- Пробел — стрелять (пуль хватает с небольшим запасом)",
            "- M — включить/отключить музыку",
            "- ESC — пауза/выход в меню",
            "",
            "Цель игры:",
            "Добраться до планеты за время таймера.",
            "От этого зависит количество очков."
        ]
            self.button_back = ImageButton(*cfg.back)
        self.neon_text = NeonText(cfg.title)

        
        try:
            font_path = os.path.join("fonts", "Exo2.ttf")
            self.font = pg.font.Font(font_path, 22)
            self.title_font = pg.font.Font(font_path, 36)
        except:
            self.font = pg.font.SysFont("Arial", 22)
            self.title_font = pg.font.SysFont("Arial", 36)

        self.dark_surface = pg.Surface((W, H))
        self.dark_surface.set_alpha(180)
        self.dark_surface.fill((10, 10, 30))
        self.planet_system = PlanetSystem((W, H))
        self.decor_elements = []
        self.star_positions = [(pg.time.get_ticks() % W, i * 50 % H) for i in range(10)]

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.button_back.collidepoint(*e.pos):
                    self.game.set_state(self.next_state_creator(self.game))
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.game.set_state(self.parent_state)

    def update(self):
        self.planet_system.update()
        self.star_positions = [(x + 1 % W, y) for x, y in self.star_positions]
        self.neon_text.update()

    def render(self, window):
        # Отрисовка фона с планетами
        self.planet_system.draw(window)
        window.blit(self.dark_surface, (0, 0))

        # Заголовок в неоновом стиле
        title = self.title_font.render("ПАУЗА", True, (0, 255, 255))  # Неоново-голубой цвет
        # window.blit(title, (W // 2 - title.get_width() // 2, 50))

        instruction_lines = self.payload

        y_offset = 170
        for line in instruction_lines:
            if line:
                text = self.font.render(line, True, (0, 255, 0))  # Неоново-зеленый цвет текста
                window.blit(text, (W // 2 - text.get_width() // 2, y_offset))
            y_offset += 40 if line else 20

        # Отрисовка декоративных звезд
        for x, y in self.star_positions:
            pg.draw.circle(window, WHITE, (int(x), int(y)), 2)

        # Отрисовка кнопки закрытия
        self.button_back.draw(window)
        self.neon_text.draw(window)

    def enter(self):
        pass
