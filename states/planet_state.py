import pygame as pg
from .game_state import State
from planet import FinalGifSprite


class PlanetState(State):
    def __init__(self, game):
        super().__init__(game)
        self.planets = self.game.planets  # List of planet data from Game class
        self.locked_image = pg.image.load('images/locked_planet.png').convert_alpha()
        original_width, original_height = self.locked_image.get_size()
        scale = min(100 / original_width, 100 / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        self.locked_image = pg.transform.scale(self.locked_image, (new_width, new_height))

        spacing_x = 160
        spacing_y = 160
        start_x = 200
        start_y = 200
        self.planet_positions = [
            (start_x + i * spacing_x, start_y + j * spacing_y)
            for j in range(4)
            for i in range(5)
        ]

        # Initialize planet sprites
        for i, planet in enumerate(self.planets):
            if not planet['gif']:  # Create GIF sprite if not already initialized
                planet['gif'] = FinalGifSprite(
                    self.planet_positions[i][0],
                    self.planet_positions[i][1],
                    planet['image'],
                    scale=0.15, rotation_speed=1
                )
            planet['position'] = self.planet_positions[i]
            planet['locked_image'] = self.locked_image

    def handle_events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    from .menu_state import MenuState
                    self.game.set_state(MenuState(self.game))
            elif e.type == pg.MOUSEBUTTONDOWN:
                # Optional: Add interaction with planets if needed
                pass

    def update(self):
        for planet in self.planets:
            if planet['discovered']:
                planet['gif'].update()  # Update animation for discovered planets

    def render(self, window):
        window.fill((0, 0, 0))  # Black background
        for planet in self.planets:
            if planet['discovered']:
                planet['gif'].image = planet['gif'].image.convert_alpha()
                window.blit(planet['gif'].image, planet['gif'].rect)
            else:
                window.blit(planet['locked_image'], planet['position'])

    def enter(self):
        pass  # Add music or effects if desired