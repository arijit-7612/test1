import pygame
import sys
import subprocess

import numpy as np
import pygame.surfarray as surfarray



pygame.init()


width, height = 1350, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Preamble Typewriter Effect')
background_image = pygame.image.load("cont.jpeg")
rotated_image = pygame.transform.rotate(background_image, 90)
rotated_image = pygame.transform.scale(rotated_image, (width, height))

font = pygame.font.Font("times_new.ttf", 21)  


preamble_lines = [
    "PREAMBLE",
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


displayed_lines = [""] * len(preamble_lines)  
line_index = 0
char_index = 0
delay = 35  
last_update = pygame.time.get_ticks()


line_height = font.get_linesize() * 1.7
skip = False

skip_button_text = font.render("Skip", True, (150, 75, 0))
skip_button_rect = skip_button_text.get_rect(bottomright=(width - 150, height - 130))




run = True
while run:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if skip_button_rect.collidepoint(event.pos):
                skip = True 


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


    screen.blit(rotated_image, (0, 0))
    
    for i, line in enumerate(displayed_lines):
        text_surface = font.render(line, True, (245, 245, 220))  # White text color
        text_rect = text_surface.get_rect(center=(width // 2, 175 + i * line_height))  # Center horizontally
        screen.blit(text_surface, text_rect.topleft)
        
    pygame.draw.rect(screen, (245, 245, 220), skip_button_rect.inflate(10, 10))  # Draw a rectangle for the button
    screen.blit(skip_button_text, skip_button_rect.topleft)  # Draw the text on the button

    # Update the display
    pygame.display.update()
    if line_index >= len(preamble_lines) and char_index == 0:
        pygame.time.delay(750)  # Optional delay after finishing
        pygame.quit()  # Quit Pygame before running the new script
        subprocess.run([sys.executable, 'menu.py'])  # Run the other Python file
        sys.exit()
    # Check if skip button was pressed and execute the new script
    if skip:
        pygame.time.delay(750)
        pygame.quit()  # Quit Pygame before running the new script
        subprocess.run([sys.executable, 'menu.py']) 
        sys.exit()  # Exit the program after the new script is executed

