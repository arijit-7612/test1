import pygame
import time

pygame.init()

WIDTH, HEIGHT = 1350, 750
FONT_SIZE = 48
TEXT_SPEED = 0.4

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Intro')
font = pygame.font.Font(None, FONT_SIZE)

def draw_text(text, x, y):
    """Draw the text on the screen with typewriter effect."""
    screen.fill((0, 0, 0))  # Fill the screen with black
    current_text = ""
    
    for char in text:
        current_text += char
        rendered_text = font.render(current_text, True, (255, 255, 255))  # Render text
        screen.blit(rendered_text, (x, y))  # Draw text on the screen
        pygame.display.flip()  # Update the display
        time.sleep(TEXT_SPEED)  # Wait for a short period

intro_text = "BINEXE"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_text(intro_text, WIDTH // 2 - font.size(intro_text)[0] // 2, HEIGHT // 2 - font.size(intro_text)[1] // 2)
    pygame.time.wait(int(len(intro_text) * TEXT_SPEED * 1000) + 1500)
    running = False  # Exit after displaying the text

pygame.quit()
