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
        self.neon_text1 = NeonText(cfg.title1)
        self.neon_text2 = NeonText(cfg.title2)
        self.button_back2 = ImageButton(*cfg.back2)
        self.button_back = ImageButton(*cfg.back)
        self.button_restart = ImageButton(*cfg.restart)
        self.planet_system = PlanetSystem((W, H))
        self.dark_surface = pg.Surface((W, H))
        self.dark_surface.set_alpha(120)
        self.dark_surface.fill((0, 0, 0))
        self.font_header = pg.font.Font(None, 36)
        self.font_row = pg.font.Font(None, 28)

        self.leaderboard_data = []
        self.load_leaderboard()

    def load_leaderboard(self):
        try:
            response = requests.get(f'http://{serv["host"]}:{serv["port"]}/scoreboard')
            if response.status_code == 200:
                self.leaderboard_data = response.json()
        except requests.RequestException as e:
            print(f"Ошибка загрузки рейтинга: {e}")

    def draw_leaderboard(self, window):
        if not self.leaderboard_data: return
            
        title = self.font_header.render("Топы", True, (255, 255, 255))
        window.blit(title, (W//2 - title.get_width()//2, 300))
        
        start_y = 350
        row_height = 40
        columns = [
            ("Место", 100),
            ("Игрок", 200),
            ("Счет", 150)
        ]
        
        for i, (col_name, col_width) in enumerate(columns):
            x = W//2 - 250 + sum(w for _, w in columns[:i])
            header = self.font_row.render(col_name, True, (255, 215, 0))
            window.blit(header, (x, start_y))
        
        pg.draw.line(window, (255, 255, 255), 
                    (W//2 - 250, start_y + 35),
                    (W//2 + 250, start_y + 35), 2)
        
        for i, row in enumerate(self.leaderboard_data[:10]):
            y = start_y + 40 + i * row_height
            rank, username, _, score = row
            rank = i + 1
            rank_text = self.font_row.render(str(rank), True, (255, 255, 255))
            window.blit(rank_text, (W//2 - 250 + 50 - rank_text.get_width()//2, y))
            name_text = self.font_row.render(username, True, (255, 255, 255))
            window.blit(name_text, (W//2 - 150, y))
            score_text = self.font_row.render(f"{score:.1f}", True, (255, 255, 255))
            window.blit(score_text, (W//2 + 150 - score_text.get_width()//2, y))
            if i < len(self.leaderboard_data) - 1:
                pg.draw.line(window, (100, 100, 100), 
                            (W//2 - 250, y + row_height - 5),
                            (W//2 + 250, y + row_height - 5), 1)

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.button_back.collidepoint(*e.pos):
                    from states.menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
                elif self.button_back2.collidepoint(*e.pos):
                    from states.menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
                elif self.button_restart.collidepoint(*e.pos):
                    from states.level_select_state import LevelSelectState
                    self.game.set_state(LevelSelectState(self.game))

    def update(self):
        self.planet_system.update()
        self.neon_text1.update()
        self.neon_text2.update()

    def render(self, window):
        self.planet_system.draw(window)
        window.blit(self.dark_surface, (0, 0))
        self.draw_leaderboard(window)
        if self.from_state == 'Menu':
            self.neon_text2.draw(window)
            self.button_back2.draw(window)
        elif self.from_state == 'Play':
            self.neon_text1.draw(window)
            self.button_back.draw(window)
            self.button_restart.draw(window)

    def enter(self):
        self.load_leaderboard()