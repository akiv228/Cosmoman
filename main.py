import asyncio
import platform
import pygame as pg
from pygame import display, time, event
from config import win_width, win_height, txt_caption, FPS
from states.menu_state import MenuState
from states.login_state import LoginState
from game_music import mixer
from test_intro import *

class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        mixer.init()
        self.window = display.set_mode((win_width, win_height))
        display.set_caption(txt_caption)
        self.clock = time.Clock()
        self.running = True
        self.music_flag = 0
        self.user_data = None
        self.current_music = None
        self.current_state = IntroState(self, LoginState)
        self.completed_difficulties = 0

    def set_state(self, state):
        self.current_state = state
        if hasattr(state, 'music') and state.music != self.current_music:
            mixer.music.load(state.music)
            mixer.music.set_volume(0.8)
            mixer.music.play(-1)
            self.current_music = state.music

    async def run(self):
        while self.running:
            events = event.get()
            for e in events:
                if e.type == pg.QUIT: self.running = False
            self.current_state.handle_events(events)
            self.current_state.update()
            self.current_state.render(self.window)
            display.update()
            self.clock.tick(FPS)
            await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    game = Game()
    asyncio.ensure_future(game.run())
else:
    if __name__ == "__main__":
        game = Game()
        asyncio.run(game.run())