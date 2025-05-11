import pygame
import random
import math

# Инициализация
pygame.init()
screen_width, screen_height = 1100, 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# ========== НАСТРОЙКИ ========== (можно свободно менять)
SETTINGS2 = {
    'stars': {
        'count': 100,
        'min_speed': 0.5,
        'max_speed': 0.8,
        'min_size': 1.0,
        'max_size': 3.0
    },
    'title': {
        'text': 'CosmoMan',
        'font_size': 100,
        'pulsation': True,
        'reflection': True,
        'flash_probability': 0.01,
        'color_change_speed': 0.02
    },
    'buttons': {
        'names': ["START", "CONTROLS", "FOUND PLANETS", "RATING"],
        'vertical_spacing': 50,  # Расстояние между кнопками
        'top_margin': 270,  # Расстояние от верхней границы экрана до первой кнопки
        'width': 350,
        'height': 60,
        'base_color': (100, 200, 255, 150),  # Базовый цвет (RGBA)
        'hover_color': (255, 255, 255, 200),  # Цвет при наведении (RGBA)

        'bg_color': (0, 0, 50, 100),  # Цвет фона кнопки (RGBA)
        'glow_transparency': 30,  # Прозрачность свечения (0-255)
        'glow_size': 15 # Размер свечения

    }
}
SETTINGS = {
    'stars': {
        'count': 100,
        'min_speed': 0.5,
        'max_speed': 0.8,
        'min_size': 1.0,
        'max_size': 3.0
    },
    'title': {
        'text': 'SELECT LEVEL',
        'font_size': 80,
        'pulsation': True,
        'reflection': False,
        'flash_probability': 0.01,
        'color_change_speed': 0.01
    },
    'buttons': {
        'names': ["LEVEL1", "LEVEL2", "LEVEL3", "EXPLORE UNIVERSITY"],
        'vertical_spacing': 50,  # Расстояние между кнопками
        'top_margin': 270,  # Расстояние от верхней границы экрана до первой кнопки
        'width': 450,
        'height': 60,
        'base_color': (100, 200, 255, 150),  # Базовый цвет (RGBA)
        'hover_color': (255, 255, 255, 200),  # Цвет при наведении (RGBA)

        'bg_color': (0, 0, 50, 100),  # Цвет фона кнопки (RGBA)
        'glow_transparency': 30,  # Прозрачность свечения (0-255)
        'glow_size': 15, # Размер свечения
        'inactive_color': (150, 150, 150, 100),  # Цвет неактивной кнопки
        'inactive_bg_color': (0, 0, 30, 50)  # Фон неактивной кнопки

    }
}


# ========== КЛАСС КНОПКИ ==========
class Button:
    def __init__(self, text, y_pos):
        cfg = SETTINGS['buttons']
        self.font = pygame.font.Font('nasalization-rg.otf', 40)
        self.text = text
        self.base_color = cfg['base_color']
        self.hover_color = cfg['hover_color']
        self.inactive_color = cfg['inactive_color']
        self.bg_color = cfg['bg_color']
        self.inactive_bg = cfg['inactive_bg_color']
        self.current_color = self.base_color
        self.rect = pygame.Rect(0, y_pos, cfg['width'], cfg['height'])
        self.rect.centerx = screen_width // 2
        self.glow = False
        self.active = True  # Добавляем статус активности

    def set_active(self, is_active):
        """Метод для изменения статуса активности"""
        self.active = is_active

    def update(self, mouse_pos):
        if self.active:
            self.glow = self.rect.collidepoint(mouse_pos)
            self.current_color = self.hover_color if self.glow else self.base_color
        else:
            self.glow = False
            self.current_color = self.inactive_color

    def draw(self):
        cfg = SETTINGS['buttons']

        # Выбираем цвет фона в зависимости от активности
        bg_color = self.bg_color if self.active else self.inactive_bg

        # Фон кнопки
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=10)

        # Эффект свечения только для активных кнопок
        if self.glow and self.active:
            glow_surf = pygame.Surface((self.rect.width + cfg['glow_size'] * 2,
                                        self.rect.height + cfg['glow_size'] * 2),
                                       pygame.SRCALPHA)

            for i in range(cfg['glow_size']):
                alpha = int(cfg['glow_transparency'] * (1 - i / cfg['glow_size']))
                color = (*self.current_color[:3], alpha)
                radius = int(self.rect.height / 2 + i * 2)
                pygame.draw.rect(glow_surf, color,
                                 (i, i,
                                  self.rect.width + cfg['glow_size'] * 2 - i * 2,
                                  self.rect.height + cfg['glow_size'] * 2 - i * 2),
                                 border_radius=radius)

            screen.blit(glow_surf, (self.rect.x - cfg['glow_size'],
                                    self.rect.y - cfg['glow_size']))

        # Текст кнопки
        text_surf = self.font.render(self.text, True, self.current_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)



# ========== КЛАССЫ ==========
class Star:
    def __init__(self):
        cfg = SETTINGS['stars']
        self.x = random.uniform(0, screen_width)
        self.y = random.uniform(0, screen_height)
        self.speed = random.uniform(cfg['min_speed'], cfg['max_speed'])
        self.size = random.uniform(cfg['min_size'], cfg['max_size'])
        self.base_alpha = random.randint(150, 255)
        self.alpha = self.base_alpha
        self.angle = 0

    def update(self):
        self.y += self.speed
        if self.y > screen_height:
            self.y = -10
            self.x = random.uniform(0, screen_width)

        self.angle += 0.1
        self.alpha = self.base_alpha + int(50 * math.sin(self.angle))
        self.alpha = max(50, min(255, self.alpha))

    def draw(self):
        color = (255, 255, 255, self.alpha)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))


class NeonText:
    def __init__(self):
        cfg = SETTINGS['title']
        self.font = pygame.font.Font('nasalization-rg.otf', cfg['font_size'])
        self.base_text = self.font.render(cfg['text'], True, (255, 255, 255))
        self.glow_size = 0
        self.glow_dir = 1
        self.hue = 0
        self.time = 0
        self.flash_alpha = 0

    def update(self):
        cfg = SETTINGS['title']
        if cfg['pulsation']:
            self.glow_size += self.glow_dir * 0.3
            if self.glow_size > 8 or self.glow_size < 0:
                self.glow_dir *= -1

        self.time += cfg['color_change_speed']
        self.hue = (math.sin(self.time) + 1) * 128

        if random.random() < cfg['flash_probability']:
            self.flash_alpha = 255
        self.flash_alpha = max(0, self.flash_alpha - 10)

    def draw(self):
        cfg = SETTINGS['title']
        main_color = pygame.Color(0)
        main_color.hsva = (self.hue, 100, 100, 100)
        text_surf = self.font.render(cfg['text'], True, main_color)

        # Эффект свечения
        if cfg['pulsation']:
            glow_color = (main_color.r, main_color.g, main_color.b, 50)
            glow_surf = pygame.Surface((self.base_text.get_width() + 20,
                                        self.base_text.get_height() + 20), pygame.SRCALPHA)
            for i in range(int(self.glow_size)):
                temp_surf = self.font.render(cfg['text'], True, glow_color)
                glow_surf.blit(temp_surf, (10 - i, 10 - i))
            screen.blit(glow_surf, ((screen_width - text_surf.get_width()) // 2 - 10, 40))

        screen.blit(text_surf, ((screen_width - text_surf.get_width()) // 2, 50))

        # Отражение
        if cfg['reflection']:
            reflection = pygame.transform.flip(text_surf, False, True)
            reflection.set_alpha(20 + self.flash_alpha)
            gradient = pygame.Surface((reflection.get_width(), reflection.get_height()))
            for y in range(reflection.get_height()):
                alpha = 255 - int(255 * y / reflection.get_height())
                gradient.fill((255, 255, 255, alpha), (0, y, reflection.get_width(), 1))
            reflection.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(reflection, ((screen_width - text_surf.get_width()) // 2,
                                     50 + text_surf.get_height() - 30))

# ========== ФУНКЦИЯ СОЗДАНИЯ КНОПОК ==========
def create_buttons():
    cfg = SETTINGS['buttons']
    button_count = len(cfg['names'])

    # Рассчитываем стартовую позицию
    if button_count == 1:
        # Для одной кнопки - строго по центру
        start_y = (screen_height - cfg['height']) // 2
    else:
        # Для нескольких кнопок - смещаем вверх
        total_height = (button_count * cfg['height']) + ((button_count - 1) * cfg['vertical_spacing'])
        start_y = cfg['top_margin']
        max_y = screen_height - total_height
        if start_y > max_y:
            start_y = max_y

    buttons = []
    for i in range(button_count):
        y_pos = start_y + i * (cfg['height'] + cfg['vertical_spacing'])
        buttons.append(Button(cfg['names'][i], y_pos))

    return buttons



stars = [Star() for _ in range(SETTINGS['stars']['count'])]
neon_text = NeonText()
buttons = create_buttons()

# ========== ГЛАВНЫЙ ЦИКЛ ==========
running = True
while running:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление и отрисовка
    for star in stars:
        star.update()
        star.draw()

    neon_text.update()
    neon_text.draw()

    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw()
    buttons[0].set_active(False)  # Делаем первую кнопку неактивной
    buttons[1].set_active(False)  # Делаем третью кнопку неактивной
    buttons[2].set_active(False)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()