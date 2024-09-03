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

popup_texts = {
    "SOVEREIGN": "sov.jpg",
    "REPUBLIC": "Republic - a state in which power rests with the people",
    # Add more words and their popup texts here
}

# Function to play intro video
def play_intro_video(video_path):
    clip = VideoFileClip(video_path)
    for frame in clip.iter_frames(fps=24, dtype='uint8'):
        frame_surface = pygame.surfarray.make_surface(np.swapaxes(frame, 0, 1))  # Convert to Pygame surface
        frame_surface = pygame.transform.scale(frame_surface, (1340, height))
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        pygame.time.wait(int(300 / 24))

# Play the intro video
play_intro_video("intro.mp4")

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

    word_rects = []  # List to store word rectangles and texts
    y_offset = 175  # Starting vertical position for text
    for i, line in enumerate(displayed_lines):
        words = line.split()
        text_surface = font.render(line, True, (245, 245, 220))
        text_rect = text_surface.get_rect(center=(width // 2, y_offset + i * line_height))
        screen.blit(text_surface, text_rect.topleft)

        start_x = text_rect.left
        for word in words: # pop up window poition
            word_surface = font.render(word, True, (245, 245, 220))
            word_rect = word_surface.get_rect(topleft=(start_x, text_rect.top))
            word_rects.append((word, word_rect))
            start_x += word_surface.get_width()+5

    # Mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Draw popup text
    for word, rect in word_rects:
        if rect.collidepoint(mouse_pos) and word in popup_texts:
            # Draw popup window
            popup_surface = pygame.Surface((300, 100))
            popup_surface.fill((50, 50, 50))  # Background color of the popup
            popup_rect = popup_surface.get_rect(center=(rect.x,rect.y-50))  # Center popup near mouse
            
            popup_text = popup_font.render(popup_texts[word], True, (255, 255, 255))
            popup_text_rect = popup_text.get_rect(center=popup_surface.get_rect().center)

            popup_image=popup_texts[words]
            popup_image = pygame.transform.scale(popup_image, (popup_surface.width,popup_surface.height))

            popup_surface.blit(popup_image, popup_surface.get_rect().topleft)
            screen.blit(popup_surface, popup_rect.topleft)
            

            # Debugging: Draw a red rectangle around the word
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
        subprocess.run([sys.executable, 'test3.py'])  
        sys.exit()

pygame.quit()
