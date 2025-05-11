import math
import colorsys
import pygame as pg
from pygame import Surface, SRCALPHA
from random import choice, uniform, randint, expovariate
from pygame import sprite
from pygame import draw

# Helper functions for gradient generation
def interpolate_color(color1, color2, ratio):
    r = int(color1[0] + (color2[0] - color1[0]) * ratio)
    g = int(color1[1] + (color2[1] - color1[1]) * ratio)
    b = int(color2[2] + (color2[2] - color1[2]) * ratio)
    return (r, g, b)

def create_linear_gradient(width, height, color1, color2, vertical=False):
    surface = pg.Surface((width, height), pg.SRCALPHA)
    if vertical:
        for y in range(height):
            ratio = y / (height - 1)
            color = interpolate_color(color1, color2, ratio)
            pg.draw.line(surface, color, (0, y), (width, y))
    else:
        for x in range(width):
            ratio = x / (width - 1)
            color = interpolate_color(color1, color2, ratio)
            pg.draw.line(surface, color, (x, 0), (x, height))
    return surface

def create_radial_gradient(width, height, center_color, outer_color, steps=100):
    surface = pg.Surface((width, height), pg.SRCALPHA)
    center = (width // 2, height // 2)
    max_radius = int(math.hypot(width // 2, height // 2))
    for i in range(steps):
        ratio = i / (steps - 1)
        color = interpolate_color(center_color, outer_color, ratio)
        radius = int(max_radius * (1 - ratio))
        pg.draw.circle(surface, color, center, radius)
    return surface

def create_angular_gradient(width, height, base_hue, saturation=0.5, lightness=0.2):
    surface = pg.Surface((width, height), pg.SRCALPHA)
    center = (width // 2, height // 2)
    for x in range(width):
        for y in range(height):
            dx = x - center[0]
            dy = y - center[1]
            angle = math.atan2(dy, dx)
            hue = (angle + math.pi) / (2 * math.pi) + base_hue
            hue %= 1.0
            color = colorsys.hls_to_rgb(hue, lightness, saturation)
            color = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
            surface.set_at((x, y), color)
    return surface

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

class Star2(sprite.Sprite):
    COLOR_PALETTES = [
        {
            'base_hue': uniform(0.0, 1.0),
            'type': choice(['analogous', 'triad', 'monochromatic'])
        }
        for _ in range(20)
    ]

    def __init__(self, w, h, palette_config) -> None:
        super().__init__()
        self.layer = randint(0, 2)
        hue, saturation, lightness = self._generate_hsl_color(palette_config)
        self.base_color = self._hsl_to_rgb(hue, saturation, lightness)
        self.r = self._generate_size()
        self.true_radius = self.r * uniform(0.8, 1.2)
        self.shine_type = choice(['sine', 'pulse', 'random'])
        self.shine_phase = uniform(0, math.pi * 2)
        self.shine_speed = uniform(0.05, 0.3) * (3 - self.layer)
        self.shine_power = uniform(0.5, 1.0)
        self.image = Surface((self.r * 2 * 2, self.r * 2 * 2), SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (randint(0, w), randint(0, h))

    def _generate_hsl_color(self, config):
        hue = config['base_hue']
        if config['type'] == 'analogous':
            hue += uniform(-0.1, 0.1)
        elif config['type'] == 'triad':
            hue += choice([0.33, -0.33])
        elif config['type'] == 'monochromatic':
            hue += uniform(-0.05, 0.05)
        saturation = 0.7 + self.layer * 0.1
        lightness = 0.5 - self.layer * 0.15
        return (hue % 1.0,
                clamp(saturation + uniform(-0.1, 0.1), 0.4, 0.9),
                clamp(lightness + uniform(-0.1, 0.1), 0.3, 0.7))

    def _hsl_to_rgb(self, h, s, l):
        rgb = colorsys.hls_to_rgb(h, l, s)
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def _generate_size(self):
        base_sizes = [3.5, 2.0, 1.0]
        return int(base_sizes[self.layer] * expovariate(1.0))

    def update(self):
        if self.shine_type == 'sine':
            alpha = 150 + int(105 * math.sin(self.shine_phase))
        elif self.shine_type == 'pulse':
            alpha = 255 if math.sin(self.shine_phase) > 0 else 100
        else:
            alpha = randint(100, 255)
        self.shine_phase += self.shine_speed
        alpha = int(alpha * self.shine_power)
        self.image.fill((0, 0, 0, 0))
        glow_radius = int(self.true_radius * 2.5)
        for i in range(3):
            alpha_glow = int(alpha * (0.3 - i * 0.1))
            draw.circle(self.image,
                        (*self.base_color, alpha_glow),
                        (self.r * 2, self.r * 2),
                        int(glow_radius * (1 - i * 0.3)))
        draw.circle(self.image,
                    (*self.base_color, alpha),
                    (self.r * 2, self.r * 2),
                    int(self.true_radius))

class Fon2_2:
    def __init__(self, w, h, stars_count=2000):
        self.w = w
        self.h = h
        self.image = Surface((w, h))
        self.rect = self.image.get_rect()
        self.palette_config = choice(Star2.COLOR_PALETTES)
        self.stars = [Star2(w, h, self.palette_config) for _ in range(stars_count)]
        self.parallax_factors = [2.5 ** i for i in [0.5, 1.0, 1.5]]
        self.camera_speed = (uniform(-1.5, 1.5), uniform(-1.5, 1.5))

        # Initialize gradient layers
        self.gradient_layers = []
        # Radial gradient
        center_color, outer_color = self.generate_gradient_colors(2)
        radial_surface = create_radial_gradient(w, h, center_color, outer_color)
        self.gradient_layers.append(radial_surface)
        # Linear gradient
        start_color, end_color = self.generate_gradient_colors(2)
        vertical = choice([True, False])
        linear_surface = create_linear_gradient(w, h, start_color, end_color, vertical)
        self.gradient_layers.append(linear_surface)
        # Angular gradient
        base_hue = self.palette_config['base_hue']
        angular_surface = create_angular_gradient(w, h, base_hue, saturation=0.5, lightness=0.2)
        self.gradient_layers.append(angular_surface)

        # Animation parameters
        self.gradient_phases = [uniform(0, 2 * math.pi) for _ in self.gradient_layers]
        self.gradient_speeds = [uniform(0.1, 0.5) for _ in self.gradient_layers]
        self.frame = 0

    def generate_gradient_colors(self, num_colors):
        colors = []
        for _ in range(num_colors):
            hue, saturation, lightness = self._generate_hsl_color(self.palette_config)
            rgb = self._hsl_to_rgb(hue, saturation, lightness)
            colors.append(rgb)
        return colors

    def _generate_hsl_color(self, config):
        hue = config['base_hue']
        if config['type'] == 'analogous':
            hue += uniform(-0.1, 0.1)
        elif config['type'] == 'triad':
            hue += choice([0.33, -0.33])
        elif config['type'] == 'monochromatic':
            hue += uniform(-0.05, 0.05)
        saturation = 0.5
        lightness = 0.2  # Dark tones for nebula effect
        return (hue % 1.0, saturation, lightness)

    def _hsl_to_rgb(self, h, s, l):
        rgb = colorsys.hls_to_rgb(h, l, s)
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def update(self, scr):
        self.frame += 1
        self.image.fill((0, 0, 0))

        # Draw gradient layers with animated transparency
        for i, gradient_surface in enumerate(self.gradient_layers):
            phase = self.gradient_phases[i]
            speed = self.gradient_speeds[i]
            alpha = 128 + int(127 * math.sin(phase + self.frame * speed * 0.1))
            temp_surface = pg.Surface((self.w, self.h), pg.SRCALPHA)
            temp_surface.blit(gradient_surface, (0, 0))
            temp_surface.set_alpha(alpha)
            self.image.blit(temp_surface, (0, 0))

        # Draw stars
        for star in sorted(self.stars, key=lambda x: x.layer):
            dx = self.camera_speed[0] * self.parallax_factors[star.layer]
            dy = self.camera_speed[1] * self.parallax_factors[star.layer]
            star.rect.centerx = (star.rect.centerx + dx) % self.w
            star.rect.centery = (star.rect.centery + dy) % self.h
            star.update()
            self.image.blit(star.image, star.rect.topleft)

        scr.blit(self.image, (0, 0))