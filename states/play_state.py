import pygame as pg
from game_music import mixer
from states.game_state import State
from states.pause_state import PauseState
from .config_state import PlayState as cfg, used_explore_finals
from level import Level
from grafics.grafics_elements import Label
from config import scores, serv, W, H
import requests


class PlayState(State):
    def __init__(self, game, difficulty):
        super().__init__(game)
        self.level = Level(difficulty, game.clock)
        self.game_link = game
        self.finish = False
        self.txt_lives = Label(*cfg.hp)
        self.music = cfg.music

        self.start_time = pg.time.get_ticks()
        self.time_limit = 300000
        self.time_left = self.time_limit
        self.txt_timer = Label(*cfg.hp)
        self.txt_timer.set_text("5:00", 24, (255, 255, 255))
        self.last_update = 0

    def handle_events(self, events):
        for e in events:
            if e.type in (pg.KEYDOWN, pg.KEYUP): player = self.level.player
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_LEFT:
                    player.x_speed = -10
                elif e.key == pg.K_RIGHT:
                    player.x_speed = 10
                elif e.key == pg.K_UP:
                    player.y_speed = -10
                elif e.key == pg.K_DOWN:
                    player.y_speed = 10
                elif e.key == pg.K_SPACE:
                    player.fire(None)
                elif e.key == pg.K_ESCAPE:
                    self.game.set_state(PauseState(self.game, self))
            elif e.type == pg.KEYUP:
                if e.key in (pg.K_LEFT, pg.K_RIGHT):
                    player.x_speed = 0
                elif e.key in (pg.K_UP, pg.K_DOWN):
                    player.y_speed = 0
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_m:
                    self.game.toggle_sound()

    def update(self):
        if not self.finish:
            self.level.update()
            self.check_game_state()
            # self.update_timer()
        mixer.music.set_volume(0.2)

    # def update_timer(self):
    #     current_time = pg.time.get_ticks()
    #     elapsed = current_time - self.start_time
    #     self.time_left = max(0, self.time_limit - elapsed)
    #     seconds = self.time_left // 1000
    #     minutes = seconds // 60
    #     seconds = seconds % 60
    #     time_str = f"{minutes:02d}:{seconds:02d}"
    #     self.txt_timer.set_text(time_str, 24, (255, 255, 255))

    #     if self.time_left <= 0:
    #         from states.lose_state import LoseState
    #         self.finish = True
    #         self.game.set_state(LoseState(self.game))

    # def render(self, window):
    #     self.level.render(window)
    #     self.txt_lives.set_text(*cfg.hp_text(self.level.player))
    #     self.txt_lives.draw(window, 0, 0)
    #     self.txt_timer.draw(window, W // 2, 0)
    def update_timer(self):
        current_time = pg.time.get_ticks()
        elapsed = current_time - self.start_time
        self.time_left = max(0, self.time_limit - elapsed)
        seconds = self.time_left // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.txt_timer.set_text(time_str, 24, (255, 255, 255))
        self.last_update = current_time  # Обновляем время последнего обновления

        if self.time_left <= 0:
            from states.lose_state import LoseState
            self.finish = True
            self.game.set_state(LoseState(self.game))

    def render(self, window):
        current_time = pg.time.get_ticks()
        # Обновляем таймер только если прошло более 500 мс с последнего обновления
        if current_time - self.last_update > 500:
            self.update_timer()

        self.level.render(window)
        self.txt_lives.set_text(*cfg.hp_text(self.level.player))
        self.txt_lives.draw(window, 5, 5)
        self.txt_timer.draw(window, W // 2, 0)

    def check_game_state(self):
        player = self.level.player
        if player.lives <= 0:
            from states.lose_state import LoseState
            self.finish = True
            self.game.set_state(LoseState(self.game))
        elif pg.sprite.collide_rect(player, self.level.final):
            from states.win_state import WinState
            self.finish = True
            self.game.completed_difficulties += 1
            if self.level.difficulty == 'EXPLORE':
                used_explore_finals.add(self.level.final.image_path)
            bscore = 0.0 if self.game.usr.best_score == "-" else float(self.game.usr.best_score)
            self.game.usr.best_score = str(bscore + float(scores[self.level.difficulty]) * self.get_k())
            requests.post(f'http://{serv["host"]}:{serv["port"]}/update',
                          data={'tkn': self.game.usr.jwt, 'scr': scores[self.level.difficulty] * self.get_k()},
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
            self.game.set_state(WinState(self.game))

    def get_k(self) -> float:
        return round(float(self.time_left) / 150000, 2)

    def enter(self):
        if self.music != self.game.current_music:
            mixer.music.load(self.music)
            mixer.music.set_volume(0.7)
            mixer.music.play(-1)
            self.game.current_music = self.music
        if self.game.sound_enabled:
            mixer.music.unpause()
        else:
            mixer.music.pause()