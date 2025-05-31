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

    def color(self, distance, x, y):
        # Используем комбинацию обоих подходов
        center_x, center_y = self.width // 2, self.height // 2

        # Базовый цвет на основе квадрантов
        if x < center_x and y < center_y:  # Левый верхний
            base_color = (1.0, 0.4, 0.4)
        elif x >= center_x and y < center_y:  # Правый верхний
            base_color = (0.4, 1.0, 0.4)
        elif x < center_x and y >= center_y:  # Левый нижний
            base_color = (0.4, 0.4, 1.0)
        else:  # Правый нижний
            base_color = (0.8, 0.8, 0.2)

        # Добавляем динамическое изменение
        r_mod = (sin(self.time + x / 100) * 0.3 + 0.7)
        g_mod = (sin(self.time * 1.1 + y / 100) * 0.3 + 0.7)
        b_mod = (sin(self.time * 1.2 + (x + y) / 200) * 0.3 + 0.7)

                 # Учитываем расстояние
        dist_factor = 1 - distance / self.max_distance

        r = int(base_color[0] * 255 * r_mod * dist_factor)
        g = int(base_color[1] * 255 * g_mod * dist_factor)
        b = int(base_color[2] * 255 * b_mod * dist_factor)

        return (r, g, b)

    def reset(self, window):
        window.fill((0, 0, 0))  # Черный фон

        # Обновляем позиции кругов
        self.update()

        # Рисуем линии
        for line in self.connect_circles():
            start_pos, end_pos = line
            distance = sqrt((start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2)

            if distance < self.max_distance:
                # Передаем координаты начальной точки для цвета
                color = self.color(distance, start_pos[0], start_pos[1])
                pg.draw.line(window, color, start_pos, end_pos, 1)

        # Рисуем круги
        for circle in self.circles:
            x, y, _, _ = circle
            color = self.color(0, x, y)  # Для кругов distance=0, чтобы они были ярче
            pg.draw.circle(window, color, (int(x), int(y)), 2)