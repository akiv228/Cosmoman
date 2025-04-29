import pygame as pg
from states.game_state import State
from states.pause_state import PauseState
from states.win_state import WinState
from states.lose_state import LoseState
from constants import BLACK_BLUE, WHITE, win_width, win_height
from level import Level
from grafics_classes import Label
# from game_music import win as win_sound, lose as lose_sound

class PlayState(State):
    def __init__(self, game, difficulty):
        super().__init__(game)
        self.level = Level(difficulty)
        self.finish = False
        self.txt_lives = Label(10, 0, 70, 30, BLACK_BLUE)

    def handle_events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_LEFT:
                    self.level.player.x_speed = -10
                elif e.key == pg.K_RIGHT:
                    self.level.player.x_speed = 10
                elif e.key == pg.K_UP:
                    self.level.player.y_speed = -10
                elif e.key == pg.K_DOWN:
                    self.level.player.y_speed = 10
                elif e.key == pg.K_SPACE:
                    self.level.player.fire(None)
                elif e.key == pg.K_ESCAPE:
                    self.game.set_state(PauseState(self.game, self))
            elif e.type == pg.KEYUP:
                if e.key in (pg.K_LEFT, pg.K_RIGHT):
                    self.level.player.x_speed = 0
                elif e.key in (pg.K_UP, pg.K_DOWN):
                    self.level.player.y_speed = 0

    def update(self):
        if not self.finish:
            self.level.update()
            self.check_game_state()

    def render(self, window):
        self.level.render(window)
        player = self.level.player
        self.txt_lives.set_text(f'Жизни: {player.lives} Бонусы: {player.collected_prizes} Пули: {player.limit}', 20, WHITE)
        self.txt_lives.draw(window, 0, 0)

    def check_game_state(self):
        player = self.level.player
        if player.lives <= 0:
            self.finish = True
            # lose_sound()
            self.game.set_state(LoseState(self.game))
        elif pg.sprite.collide_rect(player, self.level.final):
            self.finish = True
            self.game.total_prizes_collected += player.collected_prizes
            self.game.completed_difficulties += 1
            # win_sound()
            self.game.set_state(WinState(self.game))