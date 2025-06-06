import pygame as pg
from pygame.math import Vector2
from random import randrange


class PlanetSystem:
    def __init__(self, win_size):
        self.win_width, self.win_height = win_size
        self.planets = []
        self.create_initial_system()

    def create_initial_system(self):
        # Очищаем предыдущие планеты
        self.planets.clear()

        # # Два центральных "Солнца"
        # self.planets.append(Planet(
        #     position=Vector2(600, 400),
        #     radius=20,
        #     imovable=True,
        #     color=(255, 255, 100)  # Желтый цвет для солнц
        # ))
        # self.planets.append(Planet(
        #     position=Vector2(200, 400),
        #     radius=20,
        #     imovable=True,
        #     color=(255, 150, 50)  # Оранжевый цвет
        # ))
        #
        # # Планеты в движении
        # self.planets.append(Planet(
        #     position=Vector2(400, 200),
        #     delta=Vector2(0, 0),
        #     radius=10,
        #     color=(200, 200, 255)  # Голубой
        # ))
        # self.planets.append(Planet(
        #     position=Vector2(400, 210),
        #     delta=Vector2(1, 2),
        #     radius=5,
        #     color=(255, 100, 100)  # Красный
        # ))

        # self.planets.append(Planet(Vector2(400, 400), radius=50, imovable=True))

        # self.planets.append(Planet(Vector2(400, 200), delta=Vector2(3, 0), radius=10))
        # self.planets.append(Planet(Vector2(400, 600), delta=Vector2(-3, 0), radius=10))
        # self.planets.append(Planet(Vector2(600, 400), delta=Vector2(0, 3), radius=10))
        # self.planets.append(Planet(Vector2(200, 400), delta=Vector2(0, -3), radius=10))


        # self.planets.append(Planet(Vector2(400, 200), delta=Vector2(3, 0), radius=10))
        # self.planets.append(Planet(Vector2(400, 600), delta=Vector2(-3, 0), radius=10))


        # self.planets.append(Planet(Vector2(800, 400), radius=20, imovable=True))
        # self.planets.append(Planet(Vector2(280, 400), radius=20, imovable=True))
        #
        # self.planets.append(Planet(Vector2(400, 200), delta=Vector2(0, 0), radius=10))
        # self.planets.append(Planet(Vector2(400, 210), delta=Vector2(1, 2), radius=5))
        # self.planets.append(Planet(Vector2(200, 200), delta=Vector2(randrange(-3, 3), 2), radius=5))

        # Создаем сетку статических планет
        grid_dimension = 15
        grid_gap = 80
        for x in range(grid_dimension):
            for y in range(grid_dimension):
                self.planets.append(Planet(
                    position=Vector2(grid_gap * x + 40, grid_gap * y + 40),
                    radius=3,
                    imovable=True,
                    color=(100, 100, 150)  # Серо-голубой
                ))

    def update(self):
        for planet in self.planets:
            planet.process(self.planets)

    def draw(self, surface):
        for planet in self.planets:
            planet.draw(surface)


class Planet:
    def __init__(self, position, delta=Vector2(0, 0), radius=10,
                 imovable=False, color=(255, 255, 255)):
        self.position = position
        self.radius = radius
        self.delta = delta
        self.imovable = imovable
        self.color = color
        self.eatable = False

    def process(self, planets):
        # This function will be called once every frame
        # and it is responsible for calculating where the planet will go.

        # No Movement Calculations will happen if the planet doesnt move at all.
        # it also wont be eaten.
        if not self.imovable:
            for i in planets:

                if not i is self:
                    try:
                        if self.eatable:
                            if self.position.distance_to(i.position) < self.radius + i.radius:
                                print('Eaten')

                                i.radius += self.radius

                                planets.remove(self)

                        dir_from_obj  = (i.position - self.position).normalize() * 0.01 * (i.radius / 10)
                        self.delta += dir_from_obj

                    except:
                        print('In the same spot2')

            self.position += self.delta


    def draw(self, surface):
        pg.draw.circle(surface, self.color, self.position, self.radius)
        # Добавляем блик для больших планет
        if self.radius > 5:
            highlight_color = (
                min(255, self.color[0] + 50),
                min(255, self.color[1] + 50),
                min(255, self.color[2] + 50)
            )
            highlight_pos = self.position + Vector2(-self.radius // 3, -self.radius // 3)
            pg.draw.circle(surface, highlight_color, highlight_pos, self.radius // 4)


