import pygame as pg
import time

from .game_state import State
from grafics.grafics_elements import  ImageButton, Label, InputBox
from .config_state import LoginState as cfg, WinState
import asyncio
from grafics.elements_for_menu_select_login import Star, NeonText

class LoginState(State):
    def __init__(self, game):
        super().__init__(game)
        self.ui_elements = pg.sprite.Group()
        self.input_boxes = pg.sprite.Group()

        self.stars = [Star(cfg.stars) for _ in range(cfg.stars['count'])]
        # self.title = Label(*cfg.title)
        # self.title.set_text(*cfg.label)
        self.neon_text = NeonText(cfg.title)
        self.username_box = InputBox(*cfg.username_box[:4], *cfg.username_box[4:])
        self.password_box = InputBox(*cfg.password_box[:4], *cfg.password_box[4:])
        self.input_boxes.add(self.username_box, self.password_box)
        self.ui_elements.add(self.username_box, self.password_box)
        self.login_btn = ImageButton(*cfg.login_btn)
        self.register_btn = ImageButton(*cfg.register_btn)
        self.ui_elements.add(self.login_btn, self.register_btn)
        self.message = Label(*cfg.message)
        self.message.set_text(*cfg.msg)
    
    def handle_events(self, events):
        for e in events:
            for box in self.input_boxes: box.handle_event(e)
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.login_btn.rect.collidepoint(e.pos): self.handle_login(self.username_box.text, self.password_box.text)
                elif self.register_btn.rect.collidepoint(e.pos): self.handle_register(self.username_box.text, self.password_box.text)

    def handle_login(self, username, password):
        """Заглушка1"""
        asyncio.sleep(0.5)
        from .menu_state import MenuState
        self.game.set_state(MenuState(self.game))
        # from states.win_state import WinState
        # self.game.set_state(WinState(self.game))
        return {
            "status": "success",
            "user": {
                "id": 1,
                "username": username,
                "token": "fake_jwt_token_12345"
            }
        }

    def handle_register(self, username, password):
        """Заглушка2"""
        # asyncio.sleep(0.5)
        time.sleep(0.5)
        from .menu_state import MenuState
        self.game.set_state(MenuState(self.game))
        return {
            "status": "success",
            "message": f"User {username} registered successfully"
        }
    
    def update(self):
        self.input_boxes.update()
        self.neon_text.update()
        for star in self.stars:
            star.update()
    
    def render(self, window):
        window.fill((0, 0, 0))
        for star in self.stars:
            star.draw(window)
        self.ui_elements.draw(window)
        self.neon_text.draw(window)
        # self.title.draw(window, 0, -200)
        self.message.draw(window, 0, 150)

    def enter(self):
        pass