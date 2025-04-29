import asyncio
import platform
import pygame as pg
from pygame import display, time, event
from constants import win_width, win_height, txt_caption, FPS
from states.menu_state import MenuState
from game_music import mixer

class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        mixer.init()
        self.window = display.set_mode((win_width, win_height))
        display.set_caption(txt_caption)
        self.clock = time.Clock()
        self.running = True
        self.current_state = MenuState(self)
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
                if e.type == pg.QUIT:
                    self.running = False
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

#     def start(self):
#         if platform.system()=="Emscripten": asyncio.ensure_future(self.run())
#         else: asyncio.run(self.run())
#
# if __name__=='__main__': Game().start()