import pygame

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hover Tooltip Example')

# Set up fonts
font_large = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# Text to display
display_text = "HOVER OVER ME"
text_surface = font_large.render(display_text, True, (255, 255, 255))  # White text
text_rect = text_surface.get_rect(center=(width // 2, height // 2))

# Tooltip text
tooltip_text = "This is a tooltip"
tooltip_surface = font_small.render(tooltip_text, True, (0, 0, 0))  # Black text
tooltip_background = pygame.Surface(tooltip_surface.get_size())
tooltip_background.fill((255, 255, 255))  # White background

# Main loop
run = True
while run:
    screen.fill((0, 0, 0))  # Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw the main text
    screen.blit(text_surface, text_rect.topleft)

    # Check if the mouse is hovering over the text
    mouse_pos = pygame.mouse.get_pos()
    if text_rect.collidepoint(mouse_pos):
        # Display the tooltip near the mouse cursor
        tooltip_position = (mouse_pos[0] + 10, mouse_pos[1] + 10)
        screen.blit(tooltip_background, tooltip_position)
        screen.blit(tooltip_surface, tooltip_position)

    # Update the display
    pygame.display.flip()

pygame.quit()

