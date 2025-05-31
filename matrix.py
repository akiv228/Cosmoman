import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix Digital Rain")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FADE_ALPHA = 13 # Equivalent to rgba(0, 0, 0, 0.05) with 255 scale (0.05 * 255 ≈ 13)

# Font setup
FONT_SIZE = 13
font = pygame.font.SysFont("MS Gothic", FONT_SIZE)

def random_katakana():
 return chr(0x30A0 + int(random.random() * 96))

# Calculate columns based on screen width and font size
COLUMNS = WIDTH // FONT_SIZE

# Adjust font size if it's too big for the screen
if COLUMNS < 10:
 FONT_SIZE = 12
 drops = [0] * COLUMNS # Starting y-position for each column

# Create a surface for fading background
fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
fade_surface.fill((0, 0, 0, FADE_ALPHA))

# Game loop
clock = pygame.time.Clock()
running = True

while running:
 # Event handling
 for event in pygame.event.get():
  if event.type == pygame.QUIT:
   running = False

 # Apply fading background
 screen.blit(fade_surface, (0, 0))

 # Draw and update drops
 for i in range(len(drops)):
 # Randomly select a character
  char = random_katakana()
  x = i * FONT_SIZE # Calculate x position based on column index
  y = drops[i] * FONT_SIZE # Calculate y position based on drop position

 # Render character in green with antialiasing
 text = font.render(char, True, GREEN) # Antialiasing enabled
 text_rect = text.get_rect(topleft=(x, y))
 screen.blit(text, text_rect)

 # Increment drop position
 drops[i] += 1

 # Adjust the reset condition to be slightly more frequent
 if y > HEIGHT and random.random() > 0.95:
  drops[i] = random.randint(-20, 0)
 # Reset drop if it goes off-screen with a small random chance
 if y > HEIGHT and random.random() > 0.975:
  drops[i] = 0

 # Update display
 pygame.display.flip()
 clock.tick(20) # 20 FPS (~50ms interval like JS setInterval)

# Quit Pygame
pygame.quit()
