from .game_state import State
from grafics_classes import Menu
import config_state
from config_state import W, H, WHITE
from .config_state import PopupState as cfg
import pygame as pg
import os

class PopupState(State):
    def __init__(self, game, parent_state):
        super().__init__(game)
        self.parent_state = parent_state
        self.background = pg.transform.scale(cfg.instruction.convert(), (W, H))
        self.close_btn = Menu(*cfg.cross)
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

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.close_btn.collidepoint(*e.pos):
                    from .menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
                    
    def update(self):
        pass
        
    def render(self, window):
        window.blit(self.background, (0, 0))
        #for decor in self.decor_elements:
        #    window.blit(decor, (W//2 - decor.get_width()//2, H//2 - 150))
        
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
                text = self.font.render(line, True, (0, 0, 0))
                window.blit(text, (x_offset + padding, y_offset))
                if (padding > 0): padding = 0
            y_offset += 40 if line else 20
        self.close_btn.reset(window)