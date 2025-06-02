import pygame as pg
import time

from .game_state import State
from grafics.grafics_elements import  ImageButton, Label, InputBox
from .config_state import LoginState as cfg, WinState
import asyncio
from grafics.elements_for_menu_select_login import Star, NeonText
import requests
import jwt
from config import W, H, serv

class LoginState(State):
    def __init__(self, game):
        super().__init__(game)
        self.usr = game.usr
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
                if self.login_btn.rect.collidepoint(e.pos):
                    self.handle_login(self.username_box.text, self.password_box.text)
                elif self.register_btn.rect.collidepoint(e.pos):
                    self.handle_register(self.username_box.text, self.password_box.text)

    def handle_login(self, username, password):
        res = requests.post(f'http://{serv["host"]}:{serv["port"]}/login', data={'username': username, 'password': password}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        res = res.json()
        try:
            res['token']
            self.usr.jwt = res['token']
            decoded = jwt.decode(res['token'], options={"verify_signature" : False})

            self.usr.username = decoded.get('username')
            bscore = int(decoded.get('best_score'))
            self.usr.best_score = "-" if 0 == bscore else str(bscore)
            print(bscore)
            from .menu_state import MenuState
            self.game.set_state(MenuState(self.game))
        except:
            self.show_error_message("Incorrect credentials")
            return -1

    def handle_register(self, username, password):
        res = requests.post(f'http://{serv["host"]}:{serv["port"]}/register', data={'username': username, 'password': password}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        res = res.json()
        print(res)
        try:
            assert res['status'] == 'success'
            print(username)
            self.usr.username = username
            self.usr.best_score = "-"
            from .menu_state import MenuState
            self.game.set_state(MenuState(self.game))
        except:
            self.show_error_message('Username already exists')
            return -1
    
    def show_error_message(self, text):
        font = pg.font.Font(None, 36)
        error_text = font.render(text, True, (255, 0, 0))
        text_rect = error_text.get_rect(
            centerx=W // 2,
            bottom=H - 50
        )
        self.error_message = (error_text, text_rect)
        self.error_time = pg.time.get_ticks()

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
        if hasattr(self, 'error_message') and pg.time.get_ticks() - self.error_time < 5000:
            window.blit(*self.error_message)

    def enter(self):
        pass