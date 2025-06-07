import pygame as pg
import os
import requests
import threading
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
        self.loading = True
        self.loading_progress = 0
        self.payload = ["Загружаем вашу космическую историю..."]
        # self.payload = ["Загрузка истории..."]

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
        self.star_positions = [(pg.time.get_ticks() % W, i * 50 % H) for i in range(10)]


        self.button_back = None
        self.neon_text = NeonText(cfg.title)

        # Запускаем загрузку в фоне
        threading.Thread(target=self.load_content, daemon=True).start()

    def load_content(self):
        try:
            diff = self.next_state_creator(self.game).next_state_creator(self.game).level.difficulty
            self.loading_progress = 20

            headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user",
                    "content": f"Напиши начало для лабиринта про космонавта примерно на 100 символов, который оказался перед {mapped[diff]}. Без эмодзи и форматирования. Только завязка, без концовки. "}
                ],
                "temperature": 0.7,
            }
            self.loading_progress = 40
            res = requests.post("https://api.deepseek.com/v1/chat/completions",
                                headers=headers, json=data)
            self.loading_progress = 80

            content = res.json()['choices'][0]['message']['content']
            self.payload = [f"История для уровня {diff}:"] + [
                line.strip() for line in content.split('.') if line.strip()
            ]

            self.button_back = ImageButton(*cfg.back2)

        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")
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

        finally:
            self.loading = False
            self.loading_progress = 500

    def handle_events(self, events):
        if self.loading:
            return

        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.button_back and self.button_back.collidepoint(*e.pos):
                    self.game.set_state(self.next_state_creator(self.game))
            if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                self.game.set_state(self.parent_state)

    def enter(self):
        pass

    def update(self):
        self.planet_system.update()
        self.star_positions = [(x + 1 % W, y) for x, y in self.star_positions]
        self.neon_text.update()

    def render(self, window):
        self.planet_system.draw(window)
        window.blit(self.dark_surface, (0, 0))


        y_offset = 170
        for line in self.payload:
            if line:
                text = self.font.render(line, True, (0, 255, 0))
                window.blit(text, (W // 2 - text.get_width() // 2, y_offset))
                y_offset += 40 if line else 20


        if self.loading:
            pg.draw.rect(window, (50, 50, 50), (W // 2 - 100, H - 50, 200, 20))
            pg.draw.rect(window, (0, 255, 0), (W // 2 - 100, H - 50, 200 * (self.loading_progress / 100), 20))

            loading_text = self.font.render(
                f"Загрузка... {self.loading_progress}%",
                True, WHITE
            )
            window.blit(loading_text, (W // 2 - loading_text.get_width() // 2, H - 90))
        else:

            if self.button_back:
                self.button_back.draw(window)


        self.neon_text.draw(window)
        for x, y in self.star_positions:
            pg.draw.circle(window, WHITE, (int(x), int(y)), 2)


