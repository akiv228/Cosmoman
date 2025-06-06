import time
import pygame as pg

from grafics.elements_for_menu_select_login import NeonText
from .game_state import State
from planet import FinalGifSprite
from config import win_width as W, win_height as H

class PlanetState(State):
    def __init__(self, game):
        super().__init__(game)
        title = {
            'text': 'Planetary Map',
            'font_size': 95,
            'pulsation': True,
            'reflection': True,
            'flash_probability': 0.01,
            'color_change_speed': 0.02
        }

        game.upd_discovered()

        self.neon_text = NeonText(title)
        self.planets = self.game.planets
        self.locked_image = pg.image.load('images/locked_planet.png').convert_alpha()
        original_width, original_height = self.locked_image.get_size()
        scale = min(100 / original_width, 100 / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        self.locked_image = pg.transform.scale(self.locked_image, (new_width, new_height))

        spacing_x = 150
        spacing_y = 160
        start_x = 200
        start_y = 200
        self.planet_positions = [
            (start_x + i * spacing_x, start_y + j * spacing_y)
            for j in range(4)
            for i in range(5)
        ]
        
        for i, planet in enumerate(self.planets):
            planet['position'] = self.planet_positions[i]
            planet['locked_image'] = self.locked_image
            if planet.get('discovered', False) and not planet.get('gif'):
                planet['gif'] = FinalGifSprite(
                    self.planet_positions[i][0] + 50,
                    self.planet_positions[i][1] + 45,
                    planet['image'],
                    scale=0.2, rotation_speed=1
                )

    def handle_events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    from .menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
            elif e.type == pg.MOUSEBUTTONDOWN:
                pass

    def update(self):
        for planet in self.planets:
            if planet['discovered']:
                planet['gif'].update()
        self.neon_text.update()

    def render(self, window):
        window.fill((0, 0, 0))
        self.dark_surface = pg.Surface((W, H))
        self.dark_surface.set_alpha(120)
        self.dark_surface.fill((0, 0, 0))
        self.neon_text.draw(window)
        for planet in self.planets:
            if planet['discovered']:
                planet['gif'].image = planet['gif'].image.convert_alpha()
                window.blit(planet['gif'].image, planet['gif'].rect)
            else:
                window.blit(planet['locked_image'], planet['position'])

    def enter(self):
        pass