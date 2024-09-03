import pygame
import time
import subprocess
import os
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30
TEXT_SPEED = 0.4  # Speed of the typewriter effect (seconds between characters)
FONT_SIZE = 40

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Typewriter Effect')
clock = pygame.time.Clock()

# Load font
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

def open_file(file_path):
    
    try:
        if sys.platform == "win32":
            os.startfile(file_path)  # For Windows
        elif sys.platform == "darwin":
            subprocess.call(["open", file_path])  # For macOS
        else:
            subprocess.call(["xdg-open", file_path])  # For Linux
    except Exception as e:
        print(f"Error opening file: {e}")

def main():
    intro_text = "BINEXE"
    file_to_open = "menu.py"  # Update with the path to your file

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_text(intro_text, WIDTH // 2 - font.size(intro_text)[0] // 2, HEIGHT // 2 - font.size(intro_text)[1] // 2)
        
        # Check for exit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Allow the user to quit after text is displayed
        pygame.time.wait(2000)  # Wait for 2 seconds before opening the file
        open_file(file_to_open)  # Open the specified file
        running = False

    pygame.quit()

if __name__ == "__main__":
    main()
