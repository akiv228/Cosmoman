import pygame as pg

from game_music import mixer
from .game_state import State
from grafics.grafics_elements import ImageButton
from .config_state import LevelSelectState as cfg
from grafics.elements_for_menu_select_login import Star, NeonText, Button

class LevelSelectState(State):
    def __init__(self, game):
        super().__init__(game)
        self.stars = [Star(cfg.stars) for _ in range(cfg.stars['count'])]
        self.neon_text = NeonText(cfg.title)
        button_count = len(cfg.buttons['names'])
        total_height = (button_count * cfg.buttons['height']) + ((button_count - 1) * cfg.buttons['vertical_spacing'])
        start_y = cfg.buttons['top_margin']
        self.buttons = [Button(name, start_y + i * (cfg.buttons['height'] + cfg.buttons['vertical_spacing']), cfg.buttons)
                        for i, name in enumerate(cfg.buttons['names'])]
        for i, button in enumerate(self.buttons):
            button.set_active(i >= 0)
        self.button_back = ImageButton(*cfg.back)
        self.music = cfg.music
        self.user_font = pg.font.Font(None, 28)
        self.difficulty_map = {"LEVEL1": "EASY", "LEVEL2": "MEDIUM", "LEVEL3": "HARD", "EXPLORE UNIVERSITY": "EXPLORE"}

    def update(self):
            for star in self.stars:
                star.update()
            self.neon_text.update()
            mouse_pos = pg.mouse.get_pos()
            for button in self.buttons:
                button.update(mouse_pos)

    def render(self, window):
        window.fill((0, 0, 0))
        for star in self.stars:
            star.draw(window)
        self.neon_text.draw(window)
        for button in self.buttons:
            button.draw(window)
        self.button_back.draw(window)

        if hasattr(self.game, 'usr') and hasattr(self.game.usr, 'username'):
            user_info = f"{self.game.usr.username} | Best: {self.game.usr.best_score}"
            user_surface = self.user_font.render(user_info, True, (255, 255, 255))
            user_rect = user_surface.get_rect(bottomright=(window.get_width() - 20, window.get_height() - 20))
            
            bg_rect = user_rect.inflate(20, 10)
            pg.draw.rect(window, (0, 0, 0, 150), bg_rect, border_radius=5)
            pg.draw.rect(window, (100, 100, 255), bg_rect, 2, border_radius=5)
            
            window.blit(user_surface, user_rect)

    def enter(self):
        if self.music != self.game.current_music:
            mixer.music.load(self.music)
            mixer.music.set_volume(0.6)
            mixer.music.play(-1)
            self.game.current_music = self.music
        if self.game.sound_enabled:
            mixer.music.unpause()
        else:
            mixer.music.pause()

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.button_back.rect.collidepoint(e.pos):
                    from .menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
                for button in self.buttons:
                    if button.rect.collidepoint(e.pos) and button.active:
                        from .play_state import PlayState
                        from states.intro_state import IntroState
                        from .popup_state import PopupState
                        button_text = button.text
                        def create_play_state(game):
                            print('level',button_text)
                            return PlayState(game, self.difficulty_map[button_text])
                        
                        self.game.set_state(
                            PopupState(
                                self.game, 
                                self, 
                                lambda g: IntroState(g, create_play_state)
                            ))