import asyncio
import platform
import pygame as pg
from pygame import display, time, event
from config import win_width, win_height, txt_caption, FPS
from grafics.elements_for_menu_select_login import SoundNotification
from states.intro_state import IntroState
from states.menu_state import MenuState
from states.login_state import LoginState
from game_music import mixer
from models import User




class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        mixer.init()
        self.window = display.set_mode((win_width, win_height), pg.HWSURFACE | pg.DOUBLEBUF)
        # self.window = display.set_mode((win_width, win_height))
        display.set_caption(txt_caption)
        self.usr = User()
        self.clock = time.Clock()
        self.running = True
        self.music_flag = 0  # Можно использовать эту переменную для состояния звука
        self.user_data = None
        self.current_music = None
        self.current_state = IntroState(self, LoginState)
        self.completed_difficulties = 0
        self.sound_enabled = True  # Добавляем флаг состояния звука
        self.sound_notification = SoundNotification(self)
        self.planets = [
            {
                'id': i,
                'discovered': False,
                'image': f'images/planets/{i}.gif',
                'gif': None,  # Will be initialized in PlanetState
            } for i in range(1, 21)
        ]


    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            mixer.music.unpause()
        else:
            mixer.music.pause()
        self.sound_notification.show()

    def set_state(self, state):
        self.current_state = state
        state.enter()
        # self.current_state = state
        # if hasattr(state, 'music') and state.music != self.current_music:
        #     mixer.music.load(state.music)
        #     mixer.music.set_volume(0.8)
        #     mixer.music.play(-1)
        #     self.current_music = state.music
        #     # Применяем текущее состояние звука при смене состояния
        #     if not self.sound_enabled:
        #         mixer.music.pause()

    def complete_level(self, planet_id):
        for planet in self.planets:
            if planet['id'] == planet_id:
                planet['discovered'] = True
                break

    async def run(self):
        while self.running:
            events = event.get()
            for e in events:
                if e.type == pg.QUIT: self.running = False
            self.current_state.handle_events(events)
            dt = self.clock.tick(FPS) / 1000.0
            self.sound_notification.update(dt)
            self.current_state.update()
            self.current_state.render(self.window)

            self.sound_notification.draw(self.window)
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