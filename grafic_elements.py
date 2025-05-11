import pygame
import random
import math

class Star:
    def __init__(self, config):
        self.config = config
        self.x = random.uniform(0, pygame.display.get_surface().get_width())
        self.y = random.uniform(0, pygame.display.get_surface().get_height())
        self.speed = random.uniform(config['min_speed'], config['max_speed'])
        self.size = random.uniform(config['min_size'], config['max_size'])
        self.base_alpha = random.randint(150, 255)
        self.alpha = self.base_alpha
        self.angle = 0

    def update(self):
        self.y += self.speed
        screen_height = pygame.display.get_surface().get_height()
        if self.y > screen_height:
            self.y = -10
            self.x = random.uniform(0, pygame.display.get_surface().get_width())
        self.angle += 0.1
        self.alpha = self.base_alpha + int(50 * math.sin(self.angle))
        self.alpha = max(50, min(255, self.alpha))

    def draw(self, surface):
        color = (255, 255, 255, self.alpha)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.size))

class NeonText:
    def __init__(self, config):
        self.config = config
        self.font = pygame.font.Font('nasalization-rg.otf', config['font_size'])
        self.base_text = self.font.render(config['text'], True, (255, 255, 255))
        self.glow_size = 0
        self.glow_dir = 1
        self.hue = 0
        self.time = 0
        self.flash_alpha = 0

    def update(self):
        if self.config['pulsation']:
            self.glow_size += self.glow_dir * 0.3
            if self.glow_size > 8 or self.glow_size < 0:
                self.glow_dir *= -1
        self.time += self.config['color_change_speed']
        self.hue = (math.sin(self.time) + 1) * 128
        if random.random() < self.config['flash_probability']:
            self.flash_alpha = 255
        self.flash_alpha = max(0, self.flash_alpha - 10)

    def draw(self, surface):
        main_color = pygame.Color(0)
        main_color.hsva = (self.hue, 100, 100, 100)
        text_surf = self.font.render(self.config['text'], True, main_color)
        x_pos = (surface.get_width() - text_surf.get_width()) // 2
        if self.config['pulsation']:
            glow_color = (main_color.r, main_color.g, main_color.b, 50)
            glow_surf = pygame.Surface((self.base_text.get_width() + 20,
                                        self.base_text.get_height() + 20), pygame.SRCALPHA)
            for i in range(int(self.glow_size)):
                temp_surf = self.font.render(self.config['text'], True, glow_color)
                glow_surf.blit(temp_surf, (10 - i, 10 - i))
            surface.blit(glow_surf, (x_pos - 10, 40))
        surface.blit(text_surf, (x_pos, 50))
        if self.config['reflection']:
            reflection = pygame.transform.flip(text_surf, False, True)
            reflection.set_alpha(20 + self.flash_alpha)
            gradient = pygame.Surface((reflection.get_width(), reflection.get_height()))
            for y in range(reflection.get_height()):
                alpha = 255 - int(255 * y / reflection.get_height())
                gradient.fill((255, 255, 255, alpha), (0, y, reflection.get_width(), 1))
            reflection.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(reflection, (x_pos, 50 + text_surf.get_height() - 30))

class Button:
    def __init__(self, text, y_pos, config):
        self.config = config
        self.font = pygame.font.Font('nasalization-rg.otf', 40)
        self.text = text
        self.base_color = config['base_color']
        self.hover_color = config['hover_color']
        self.inactive_color = config['inactive_color']
        self.bg_color = config['bg_color']
        self.inactive_bg = config['inactive_bg_color']
        self.current_color = self.base_color
        self.rect = pygame.Rect(0, y_pos, config['width'], config['height'])
        self.rect.centerx = pygame.display.get_surface().get_width() // 2
        self.glow = False
        self.active = True

    def set_active(self, is_active):
        self.active = is_active

    def update(self, mouse_pos):
        if self.active:
            self.glow = self.rect.collidepoint(mouse_pos)
            self.current_color = self.hover_color if self.glow else self.base_color
        else:
            self.glow = False
            self.current_color = self.inactive_color

    def draw(self, surface):
        bg_color = self.bg_color if self.active else self.inactive_bg
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=10)
        if self.glow and self.active:
            glow_surf = pygame.Surface((self.rect.width + self.config['glow_size'] * 2,
                                        self.rect.height + self.config['glow_size'] * 2),
                                       pygame.SRCALPHA)
            for i in range(self.config['glow_size']):
                alpha = int(self.config['glow_transparency'] * (1 - i / self.config['glow_size']))
                color = (*self.current_color[:3], alpha)
                radius = int(self.rect.height / 2 + i * 2)
                pygame.draw.rect(glow_surf, color,
                                 (i, i,
                                  self.rect.width + self.config['glow_size'] * 2 - i * 2,
                                  self.rect.height + self.config['glow_size'] * 2 - i * 2),
                                 border_radius=radius)
            surface.blit(glow_surf, (self.rect.x - self.config['glow_size'],
                                     self.rect.y - self.config['glow_size']))
        text_surf = self.font.render(self.text, True, self.current_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)