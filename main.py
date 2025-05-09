import asyncio
import platform
import pygame as pg
from pygame import display, time, event
from config import win_width, win_height, txt_caption, FPS
from states.menu_state import MenuState
from states.login_state import LoginState
from game_music import mixer
from starfield import *

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
        #Тут важно понимать какие атрибуты прописывать перед сменой State иначе те которые идут после видны не будут в других обработчиках по сслыке game
        # self.current_state = LoginState(self)
        self.current_state = IntroState(self, LoginState);
        # game.current_state = IntroState(game, MenuState)
        #self.current_state = MenuState(self)
        self.total_prizes_collected = 0
        self.completed_difficulties = 0
        # self.states={
        #     'menu':MenuState(self),
        #     'level_select':LevelSelectState(self),
        #     'play':PlayState(self),
        #     'pause':PauseState(self),
        #     'win':WinState(self),
        #     'lose':LoseState(self)
        # }

    def set_state(self, state):
        self.current_state = state

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