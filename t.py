import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1350, 780
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Preamble Typewriter Effect')
background_image = pygame.image.load("cont.jpeg")
background_image = pygame.transform.scale(background_image, (width,height))
# Set up fonts
font = pygame.font.Font("times_new.ttf", 21)  # Use your desired font and size

# Preamble text, split into lines
preamble_lines = [
    "We, THE PEOPLE OF INDIA, having solemnly resolved to constitute",
    "India into a SOVEREIGN SOCIALIST SECULAR DEMOCRATIC",
    "REPUBLIC and to secure to all its citizens:",
    "JUSTICE, Social, Economic and Political;",
    "LIBERTY of thought, expression, belief, faith and worship;",
    "EQUALITY of status and of opportunity; and to promote among them all;",
    "FRATERNITY assuring the dignity of the individual and the unity and integrity of the Nation;",
    "IN OUR CONSTITUENT ASSEMBLY this twenty-sixth day of",
    "November, 1949, do HEREBY ADOPT, ENACT AND GIVE TO",
    "OURSELVES THIS CONSTITUTION."
]

# Variables for typewriter effect
displayed_lines = [""] * len(preamble_lines)  # Initialize displayed lines as empty strings
line_index = 0
char_index = 0
delay = 35  # Delay in milliseconds between each character
last_update = pygame.time.get_ticks()

# Line height (distance between lines)
line_height = font.get_linesize()*1.7
skip=False

skip_button_text = font.render("Skip", True, (150,75,0))
skip_button_rect = skip_button_text.get_rect(bottomright=(width - 180, height - 90))
# Main game loop
run = True
while run:

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if skip_button_rect.collidepoint(event.pos):
                skip = True  # User clicked the skip button
    # Typewriter effect logic
    current_time = pygame.time.get_ticks()
    if not skip:
        if current_time - last_update > delay:
            if line_index < len(preamble_lines):
                if char_index < len(preamble_lines[line_index]):
                    displayed_lines[line_index] += preamble_lines[line_index][char_index]
                    char_index += 1
                else:
                    line_index += 1
                    char_index = 0
                last_update = current_time
    else:
        displayed_lines = preamble_lines[:] 
    screen.blit(background_image, (0, 0))
    # Render and display each line centered on the screen
    for i, line in enumerate(displayed_lines):
        text_surface = font.render(line, True, (245, 245, 220))  # White text color
        text_rect = text_surface.get_rect(center=(width // 2, 175 + i * line_height))  # Center horizontally
        screen.blit(text_surface, text_rect.topleft)

    pygame.draw.rect(screen, (245,245,220), skip_button_rect.inflate(10, 10))  # Draw a red rectangle for the button
    screen.blit(skip_button_text, skip_button_rect.topleft)

    # Update the display
    pygame.display.update()

pygame.quit()
sys.exit()
