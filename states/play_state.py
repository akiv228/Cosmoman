import pygame as pg

from game_music import mixer
from states.game_state import State
from states.pause_state import PauseState
from .config_state import PlayState as cfg, used_explore_finals
from level import Level
from grafics.grafics_elements import  Label
# from game_music import win as win_sound, lose as lose_sound

class PlayState(State):
    def __init__(self, game, difficulty):
        super().__init__(game)
        self.level = Level(difficulty)
        self.finish = False
        self.txt_lives = Label(*cfg.hp)
        self.music = cfg.music

    def handle_events(self, events):
        for e in events:
            if e.type in (pg.KEYDOWN, pg.KEYUP): player = self.level.player
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_LEFT: player.x_speed = -10
                elif e.key == pg.K_RIGHT: player.x_speed = 10
                elif e.key == pg.K_UP: player.y_speed = -10
                elif e.key == pg.K_DOWN: player.y_speed = 10
                elif e.key == pg.K_SPACE: player.fire(None)
                elif e.key == pg.K_ESCAPE:
                    self.game.set_state(PauseState(self.game, self))
                    # self.game.toggle_sound()
            elif e.type == pg.KEYUP:
                if e.key in (pg.K_LEFT, pg.K_RIGHT): player.x_speed = 0
                elif e.key in (pg.K_UP, pg.K_DOWN): player.y_speed = 0
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_m:
                    self.game.toggle_sound()  # Используем метод из Game

    def update(self):
        if not self.finish:
            self.level.update()
            self.check_game_state()
        mixer.music.set_volume(0.2)

    def render(self, window):
        self.level.render(window)
        self.txt_lives.set_text(*cfg.hp_text(self.level.player))
        self.txt_lives.draw(window, 0, 0)

    # def check_game_state(self):
    #     player = self.level.player
    #     if player.lives <= 0:
    #         from states.lose_state import LoseState
    #         self.finish = True
    #         # lose_sound()
    #         self.game.set_state(LoseState(self.game))
    #     elif pg.sprite.collide_rect(player, self.level.final):
    #         from states.win_state import WinState
    #         self.finish = True
    #         # self.game.total_prizes_collected += player.collected_prizes
    #         self.game.completed_difficulties += 1
    #         # win_sound()
    #         self.game.set_state(WinState(self.game))

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
            # Если уровень EXPLORE, фиксируем финальный спрайт как использованный
            if self.level.difficulty == 'EXPLORE':
                used_explore_finals.add(
                    self.level.final.image_path)  # Предполагается, что у FinalGifSprite есть image_path
            self.game.set_state(WinState(self.game))

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