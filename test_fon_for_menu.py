import pygame
import random
import math

# Инициализация
pygame.init()
screen_width, screen_height = 1100, 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


class Star:
    def __init__(self):
        self.x = random.uniform(0, screen_width)
        self.y = random.uniform(0, screen_height)
        self.speed = random.uniform(0.5, 0.8)
        self.size = random.uniform(1.0, 3.0)
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
        self.font = pygame.font.Font('nasalization-rg.otf', 100)
        self.base_text = self.font.render('CosmoMan', True, (255, 255, 255))
        self.glow_size = 0
        self.glow_dir = 1
        self.hue = 0
        self.time = 0
        self.flash_alpha = 0

    def update(self):
        self.glow_size += self.glow_dir * 0.3
        if self.glow_size > 8 or self.glow_size < 0:
            self.glow_dir *= -1

        self.time += 0.02
        self.hue = (math.sin(self.time) + 1) * 128

        # Случайные вспышки
        if random.random() < 0.05:
            self.flash_alpha = 255
        self.flash_alpha = max(0, self.flash_alpha - 10)

    def draw(self):
        main_color = pygame.Color(0)
        main_color.hsva = (self.hue, 100, 100, 100)
        text_surf = self.font.render('CosmoMan', True, main_color)

        # Эффект свечения
        glow_color = (main_color.r, main_color.g, main_color.b, 50)
        glow_surf = pygame.Surface((self.base_text.get_width() + 20,
                                    self.base_text.get_height() + 20), pygame.SRCALPHA)

        for i in range(int(self.glow_size)):
            temp_surf = self.font.render('CosmoMan', True, glow_color)
            glow_surf.blit(temp_surf, (10 - i, 10 - i))

        # Позиция текста
        text_pos = (
            (screen_width - text_surf.get_width()) // 2,
            50
        )

        screen.blit(glow_surf, (text_pos[0] - 10, text_pos[1] - 10))
        screen.blit(text_surf, text_pos)

        # Отражение с вспышками
        reflection = pygame.transform.flip(text_surf, False, True)
        reflection.set_alpha(70 + self.flash_alpha)

        gradient = pygame.Surface((reflection.get_width(), reflection.get_height()))
        for y in range(reflection.get_height()):
            alpha = 255 - int(255 * y / reflection.get_height())
            gradient.fill((255, 255, 255, alpha), (0, y, reflection.get_width(), 1))

        reflection.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(reflection, (text_pos[0], text_pos[1] + text_surf.get_height() - 30))


class Button:
    def __init__(self, text, y_offset):
        self.font = pygame.font.Font('nasalization-rg.otf', 40)
        self.text = text
        self.base_color = (100, 200, 255)
        self.hover_color = (255, 255, 255)
        self.current_color = self.base_color
        self.rect = pygame.Rect(0, 0, 350, 60)
        self.rect.center = (screen_width // 2, screen_height // 2 + y_offset)
        self.glow = False

    def update(self, mouse_pos):
        self.glow = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.glow else self.base_color

    def draw(self):
        # Фон кнопки
        pygame.draw.rect(screen, (0, 0, 150), self.rect, border_radius=10)

        # Эффект свечения
        if self.glow:
            glow_surf = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*self.current_color, 50),
                             (0, 0, self.rect.width + 20, self.rect.height + 20),
                             border_radius=15)
            screen.blit(glow_surf, (self.rect.x - 10, self.rect.y - 10))

        # Текст кнопки
        text_surf = self.font.render(self.text, True, self.current_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


# Создание объектов
stars = [Star() for _ in range(100)]
neon_text = NeonText()
buttons = [
    Button("START", -100 + 50),
    Button("CONTROLS", -20 + 50 ),
    Button("FOUND PLANETS", 60 + 50),
    Button("RATING", 140 + 50)
]

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

    # Кнопки
    for btn in buttons:
        btn.update(mouse_pos)
        btn.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()