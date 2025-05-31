import pygame
import random
import math


class MotherboardBackground:
    def __init__(self, w, h, components=200, tracks=300, lights=50):
        self.width = w
        self.height = h
        self.components = components
        self.tracks = tracks
        self.lights = lights
        self.time = 0
        self.glow_cycle_speed = 2.5

        self.static_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        self._generate_static_background()

    def _generate_static_background(self):
        # цвет платы (темно-зеленый)
        self.static_surface.fill((10, 30, 15))

        # цвета для элементов
        board_colors = [(20, 60, 30), (15, 45, 20), (25, 50, 25)]
        track_colors = [(40, 120, 60), (30, 100, 50), (50, 150, 75)]
        component_colors = [(30, 30, 40), (25, 25, 35), (20, 20, 30)]
        contact_colors = [(180, 180, 200), (200, 200, 220), (160, 160, 180)]

        # рисуем дорожки
        for _ in range(self.tracks):
            start_x = random.randint(0, self.width)
            start_y = random.randint(0, self.height)
            segments = random.randint(3, 8)
            thickness = random.choice([1, 1, 2, 2, 3])
            color = random.choice(track_colors)

            current_x, current_y = start_x, start_y
            for _ in range(segments):
                angle = random.choice([0, 90, 180, 270])
                length = random.randint(20, 100)
                rad = math.radians(angle)

                end_x = current_x + int(length * math.cos(rad))
                end_y = current_y + int(length * math.sin(rad))

                # ограничение в пределах экрана
                end_x = max(0, min(end_x, self.width))
                end_y = max(0, min(end_y, self.height))

                pygame.draw.line(
                    self.static_surface,
                    color,
                    (current_x, current_y),
                    (end_x, end_y),
                    thickness
                )
                current_x, current_y = end_x, end_y

        # рисуем компоненты (чипы, разъемы)
        for _ in range(self.components):
            comp_type = random.choice(['chip', 'chip', 'connector'])
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            color = random.choice(component_colors)

            if comp_type == 'chip':
                # прямоугольник чипа
                width = random.randint(20, 60)
                height = random.randint(10, 30)
                pygame.draw.rect(
                    self.static_surface,
                    color,
                    (x, y, width, height),
                    0,
                    border_radius=3
                )

                # контакты чипа
                contact_color = random.choice(contact_colors)
                for side in ['top', 'bottom']:
                    contacts = random.randint(8, 16)
                    spacing = width / (contacts + 1)
                    for i in range(contacts):
                        cx = x + spacing * (i + 1)
                        cy = y if side == 'top' else y + height
                        pygame.draw.circle(
                            self.static_surface,
                            contact_color,
                            (int(cx), int(cy)),
                            2
                        )

            elif comp_type == 'connector':
                # разъем (ряд контактов)
                pins = random.randint(5, 15)
                pin_spacing = 8
                width = pins * pin_spacing
                height = random.randint(15, 25)

                # основание разъема
                pygame.draw.rect(
                    self.static_surface,
                    color,
                    (x, y, width, height)
                )

                # контакты разъема
                contact_color = random.choice(contact_colors)
                for i in range(pins):
                    pin_x = x + (i * pin_spacing) + pin_spacing // 2
                    pygame.draw.line(
                        self.static_surface,
                        contact_color,
                        (pin_x, y + height),
                        (pin_x, y + height + 15),
                        2
                    )

    def update(self, dt):
        self.time += dt

    def render(self, surface):
        # статическая основа платы
        surface.blit(self.static_surface, (0, 0))

        # динамические светящиеся элементы
        pulse = 0.5 + 0.5 * math.sin(self.time * self.glow_cycle_speed)
        glow_intensity = int(180 + 75 * pulse)

        # рисуем светящиеся дорожки
        for _ in range(int(self.lights * 0.6)):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 3)
            pygame.draw.circle(
                surface,
                (0, 200 + int(55 * pulse), 0, glow_intensity),
                (x, y),
                size
            )

        # рисуем светящиеся компоненты
        for _ in range(int(self.lights * 0.4)):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(2, 4)
            pygame.draw.circle(
                surface,
                (0, 100 + int(155 * pulse), 200 + int(55 * pulse), glow_intensity),
                (x, y),
                size
            )