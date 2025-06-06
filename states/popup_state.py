import config
from grafics.planetfons_lose_win import PlanetSystem
from .game_state import State
from grafics.grafics_elements import  ImageButton
from config import W, H, WHITE
from .config_state import PopupState as cfg
import pygame as pg
import os

class PopupState(State):
    def __init__(self, game, parent_state):
        super().__init__(game)
        self.parent_state = parent_state
        self.close_btn = ImageButton(*cfg.cross)
        try:
            font_path = os.path.join("fonts", "standout.ttf")
            self.font = pg.font.Font(font_path, 22)
            self.title_font = pg.font.Font(font_path, 36)
        except:
            self.font = pg.font.SysFont(None, 22)
            self.title_font = pg.font.SysFont(None, 36)
            
        self.decor_elements = []
        try:
            self.decor_elements.append(cfg.decoration.convert_alpha())
        except: pass

        self.dark_surface = pg.Surface((W, H))
        self.dark_surface.set_alpha(120)
        self.dark_surface.fill((0, 0, 0))
        self.planet_system = PlanetSystem((W, H))

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.close_btn.collidepoint(*e.pos):
                    from .menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    from .menu_state import MenuState
                    self.game.set_state(MenuState(self.game))

    def update(self):
        self.planet_system.update()
        
    def render(self, window):
        self.planet_system.draw(window)

        # Затемняем фон для интерфейса
        window.blit(self.dark_surface, (0, 0))
        
        title = self.title_font.render("Инструкция к игре", True, WHITE)
        window.blit(title, (W//2 - title.get_width()//2, 30))
        
        instruction_lines = [
            "Welcome!",
            "",
            "Основные правила:",
            "- Используйте стрелки для движения",
            "- Бла бла бла бла бла",
            "- ESC для не знаю чего, но да",
            "",
            "Цель игры: бла бла бла..."
        ]
        x_offset, y_offset, padding = config.x_offset, config.y_offset, config.padding
        for line in instruction_lines:
            if line:
                if (line == instruction_lines[-1]): padding = 160
                text = self.font.render(line, True, WHITE)
                window.blit(text, (x_offset + padding, y_offset))
                if (padding > 0): padding = 0
            y_offset += 40 if line else 20
        self.close_btn.draw(window)

    def enter(self):
        pass