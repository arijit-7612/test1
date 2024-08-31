import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1570, 795
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Learning Constitution')

# Load background image
background_image = pygame.image.load('constitution.jpg')
background_image = pygame.transform.scale(background_image, (width, height))

# Load fundamental rights images
rights_images = [
    pygame.image.load(f'right{i}.jpg') for i in range(1, 7)
]

# Resize the fundamental rights images
box_width, box_height = 400, 200
for i in range(6):
    rights_images[i] = pygame.transform.scale(rights_images[i], (box_width, box_height))

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up fonts
custom_font_path = 'custom_font.ttf'  # Path to your custom font file
heading_font = pygame.font.Font(custom_font_path, 74)  # Font for the main heading
small_font = pygame.font.Font(custom_font_path, 36)    # Font for the boxes

# Draw text function
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Blit the background image
    screen.blit(background_image, (0, 0))

    # Draw the main heading
    draw_text('Learning Constitution of INDIA', heading_font, WHITE, screen, width // 2, 50)

    # Draw boxes for fundamental rights images
    margin = 20
    x_start = (width - (box_width + margin) * 3) // 2
    y_start = 150

    for i, image in enumerate(rights_images):
        x = x_start + (i % 3) * (box_width + margin)
        y = y_start + (i // 3) * (box_height + margin)
        screen.blit(image, (x, y))

    # Update the display
    pygame.display.flip()

