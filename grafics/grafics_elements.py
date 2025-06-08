import pygame as pg



class Backgrounds:
    def __init__(self, image_path, w, h, x, y):
        self.image = pg.transform.scale(pg.image.load(image_path), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class ImageButton(pg.sprite.Sprite):
    def __init__(self, image_path, x, y, width, height):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(image_path), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Label:
    def __init__(self, x, y, width, height, color):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.font = None
        self.text = None

    def set_text(self, text, size, text_color):
        self.font = pg.font.Font(None, size)
        self.text = self.font.render(text, True, text_color)

    def draw(self, window, shift_x=0, shift_y=0):
        if self.text:
            window.blit(self.text, (self.rect.x + shift_x, self.rect.y + shift_y))

    def Text(self, param, param1, param2):
        pass


class InputBox(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, placeholder='', inactive_color=(200, 200, 200), active_color=(255, 255, 255),
                 is_password=False):
        super().__init__()
        self.rect = pg.Rect(x, y, w, h)
        self.color = inactive_color
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.placeholder = placeholder
        self.text = ''
        self.text_color = (255, 255, 255)
        self.font = pg.font.Font(None, 32)
        self.active = False
        self.is_password = is_password
        self.image = pg.Surface((w, h), pg.SRCALPHA)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.active_color if self.active else self.inactive_color

        if event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_RETURN:
                return True
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def update(self):
        self.image.fill((0, 0, 0, 0))  # Прозрачный фон
        pg.draw.rect(self.image, self.color, (0, 0, self.rect.w, self.rect.h), 2)

        if not self.text and not self.active:
            text_surface = self.font.render(self.placeholder, True, (150, 150, 150))
        else:
            display_text = '*' * len(self.text) if self.is_password else self.text
            text_surface = self.font.render(display_text, True, self.text_color)

        self.image.blit(text_surface, (5, 5))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
