import pygame as pg
from random import randint, uniform
from math import sqrt, sin


class CircleBackground:
    def __init__(self, w, h, circles_count=30):
        self.width = w
        self.height = h
        self.circles_count = circles_count
        self.velocity = [1.2, 1.2]
        self.max_distance = 100
        self.circles = []
        self.create_circles()
        self.time = 0
        self.color_speed = 0.01

    def create_circles(self):
        for _ in range(self.circles_count):
            x = randint(0, self.width)
            y = randint(0, self.height)
            velocity_x = uniform(-self.velocity[0], self.velocity[0])
            velocity_y = uniform(-self.velocity[1], self.velocity[1])
            self.circles.append((x, y, velocity_x, velocity_y))

    def update(self):
        self.time += self.color_speed
        circles_moved = []

        for circle in self.circles:
            x, y, velocity_x, velocity_y = circle

            x += velocity_x
            y += velocity_y

            if x >= self.width or x <= 0:
                velocity_x *= -1
            if y >= self.height or y <= 0:
                velocity_y *= -1

            circles_moved.append((x, y, velocity_x, velocity_y))

        self.circles = circles_moved

    def connect_circles(self):
        lines = []
        quantity = len(self.circles)
        for p0 in range(quantity - 1):
            for p1 in range(p0 + 1, quantity):
                lines.append([self.circles[p0][:2], self.circles[p1][:2]])
        return lines

    def color(self, distance, k):
        x = int((self.max_distance - distance) * 255 / self.max_distance)
        if k < (self.width // 2 + self.height // 2):
            return (x, 0, 0)
        else:
            return (0, x, 0)

    # def color(self, distance, x, y):
    #     # Используем sin/cos для плавного изменения цветов
    #     r = int((sin(self.time + x / 100) * 0.5 + 0.5) * 255 * (1 - distance / self.max_distance))
    #     g = int((sin(self.time * 1.1 + y / 100) * 0.5 + 0.5) * 255 * (1 - distance / self.max_distance))
    #     b = int((sin(self.time * 1.2 + (x + y) / 200) * 0.5 + 0.5) * 255 * (1 - distance / self.max_distance))
    #     return (r, g, b)



    # def color(self, distance, x, y):
    #     # Разделяем экран на 4 квадранта с разными цветовыми схемами
    #     center_x, center_y = self.width // 2, self.height // 2
    #
    #     if x < center_x and y < center_y:  # Левый верхний
    #         return (int(255 * (1 - distance / self.max_distance)), 100, 100)
    #     elif x >= center_x and y < center_y:  # Правый верхний
    #         return (100, int(255 * (1 - distance / self.max_distance)), 100)
    #     elif x < center_x and y >= center_y:  # Левый нижний
    #         return (100, 100, int(255 * (1 - distance / self.max_distance)))
    #     else:  # Правый нижний
    #         return (int(255 * (distance / self.max_distance)),
    #                 int(255 * (1 - distance / self.max_distance)),
    #                 int(255 * (distance / self.max_distance)))

    def reset(self, window):
        """Отрисовка фона на поверхности window"""
        window.fill((0, 0, 0))  # Черный фон

        # Обновляем позиции кругов
        self.update()

        # Рисуем линии
        for line in self.connect_circles():
            start_pos, end_pos = line
            distance = sqrt((start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2)
            k = start_pos[0] + start_pos[1]

            if distance < self.max_distance:
                pg.draw.line(window, self.color(distance, k), start_pos, end_pos, 1)

        # Рисуем круги
        for circle in self.circles:
            x, y, _, _ = circle
            k = x + y

            if k < (self.width // 2 + self.height // 2):
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)

            pg.draw.circle(window, color, (int(x), int(y)), 2)