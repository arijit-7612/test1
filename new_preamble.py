import pygame
import sys
import subprocess
from moviepy.editor import VideoFileClip
import numpy as np
import pygame.surfarray as surfarray

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1350, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Preamble Typewriter Effect')

# Load and rotate the background image
background_image = pygame.image.load("cont.jpeg")
rotated_image = pygame.transform.rotate(background_image, 90)
rotated_image = pygame.transform.scale(rotated_image, (width, height))

# Set up fonts
font = pygame.font.Font("times_new.ttf", 21)
popup_font = pygame.font.Font("times_new.ttf", 16)  # Font for popup text

# Preamble text
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

# Variables for typewriter effect
displayed_lines = [""] * len(preamble_lines)
line_index = 0
char_index = 0
delay = 35
last_update = pygame.time.get_ticks()

line_height = font.get_linesize() * 1.7
skip = False
next_button = False

# Skip/Next button setup
skip_button_text = font.render("Skip", True, (150, 75, 0))
skip_button_rect = skip_button_text.get_rect(bottomright=(width - 150, height - 130))

# Popup text for specific words or phrases
popup_texts = {
    "SOVEREIGN": "sov.jpg",
    "REPUBLIC": "republic.jpg",
    "SOCIALIST": "SOCIALIST.jpg",
    "SECULAR": "Secular.jpg",
    "DEMOCRATIC": "democratic.jpg",
    "JUSTICE, Social, Economic and Political;": "JUSTICE.jpg",
    "LIBERTY": "LIBERTY.jpg",
    "EQUALITY": "equality.jpg",
    "FRATERNITY": "FRATERNITY.jpg",
    "CONSTITUENT ASSEMBLY": "IN OUR CONSTITUENT ASSEMBLY.jpg",
    "HEREBY ADOPT, ENACT AND GIVE TO": "LAST PHRASE.jpg",
    # Add more phrases or words here
}



# Main loop
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if skip_button_rect.collidepoint(event.pos):
                if not skip:
                    skip = True  
                    skip_button_text = font.render("Next", True, (150, 75, 0))  
                else:
                    next_button = True  

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

    word_rects = []  # List to store word/phrase rectangles and texts
    y_offset = 175  # Starting vertical position for text
    for i, line in enumerate(displayed_lines):
        words = line.split()
        text_surface = font.render(line, True, (245, 245, 220))
        text_rect = text_surface.get_rect(center=(width // 2, y_offset + i * line_height))
        screen.blit(text_surface, text_rect.topleft)

        start_x = text_rect.left
        for word in words:
            word_surface = font.render(word, True, (245, 245, 220))
            word_rect = word_surface.get_rect(topleft=(start_x, text_rect.top))
            word_rects.append((word, word_rect))
            start_x += word_surface.get_width() + 5

        # Create rectangles for multi-word phrases
        for phrase, popup in popup_texts.items():
            if phrase in line:
                phrase_surface = font.render(phrase, True, (245, 245, 220))
                phrase_start = line.find(phrase)
                phrase_end = phrase_start + len(phrase)
                phrase_rect = pygame.Rect(text_rect.left + font.size(line[:phrase_start])[0],
                                          text_rect.top,
                                          font.size(phrase)[0],
                                          text_rect.height)
                word_rects.append((phrase, phrase_rect))

    # Mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Draw popup text
    for word, rect in word_rects:
        if rect.collidepoint(mouse_pos) and word in popup_texts:
            if popup_texts[word].endswith(".jpg") or popup_texts[word].endswith(".png"):
                # Load and display the image if the popup text is an image file path
                popup_image = pygame.image.load(popup_texts[word])
                popup_image = pygame.transform.scale(popup_image, (450, 250))
                popup_surface = pygame.Surface((450, 250))
                popup_surface.blit(popup_image, (0, 0))
            else:
                # Render and display the popup text
                popup_surface = pygame.Surface((300, 100))
                popup_surface.fill((50, 50, 50))  # Background color of the popup
                popup_text = popup_font.render(popup_texts[word], True, (255, 255, 255))
                popup_text_rect = popup_text.get_rect(center=popup_surface.get_rect().center)
                popup_surface.blit(popup_text, popup_text_rect.topleft)

            popup_rect = popup_surface.get_rect(center=(rect.x + 300, rect.y - 140))  # Center popup near mouse
            screen.blit(popup_surface, popup_rect.topleft)

            # Debugging: Draw a red rectangle around the word/phrase
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)  # Red rectangle for debugging

    pygame.draw.rect(screen, (245, 245, 220), skip_button_rect.inflate(10, 10))  # Draw a rectangle for the button
    screen.blit(skip_button_text, skip_button_rect.topleft)  # Draw the text on the button

    pygame.display.update()

    if (line_index >= len(preamble_lines) and char_index == 0):
        skip = True
        skip_button_text = font.render("Next", True, (150, 75, 0))
        screen.blit(skip_button_text, skip_button_rect.topleft)
        
    if next_button:  
        pygame.time.delay(750)
        pygame.quit()  
        subprocess.run([sys.executable, 'menu.py'])  
        sys.exit()

pygame.quit()
