import pygame
import time
import subprocess
import os
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1350, 750
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

# Constants for images and fonts
IMAGE_SIZE = (300, 200)  # Size of each rectangle (width, height)
BACKGROUND_COLOR = (0, 0, 0)  # Black background
IMAGE_SPACING = 50  # Space between images
HEADING_FONT_SIZE = 72  # Increased font size
HEADING_COLOR = (139, 69, 19)  # Brown color (RGB)
HEADING_VERTICAL_OFFSET = 47  # Offset to raise the heading

# Path to the custom font
CUSTOM_FONT_PATH = "times_new.ttf"  # Update this path to your custom font file

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('MENU')

# Load images
def load_image(file_path, size=None):
    """Load an image and optionally resize it."""
    try:
        image = pygame.image.load(file_path)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Error loading image: {e}")
        sys.exit()

# Define image paths
background_image_path = "background.jpeg"  # Path to background image
image_paths = [
    "preamble.jpg",
    "PRINCIPLES.jpg",
    "RIGHTS.jpg",
    "DUTIES.jpg"
]

# Define file paths to open
file_paths = [
    "preamble.py",
    "comingsoon.jpg",
    "test3.py",
    "comingsoon.jpg"
]

# Load all images
background_image = load_image(background_image_path, (WIDTH, HEIGHT))
loaded_images = [load_image(image_path, IMAGE_SIZE) for image_path in image_paths]

# Load custom font
def load_font(file_path, size):
    """Load a custom font from the specified file path."""
    try:
        return pygame.font.Font(file_path, size)
    except pygame.error as e:
        print(f"Error loading font: {e}")
        sys.exit()

# Set up font for heading using custom font
heading_font = load_font(CUSTOM_FONT_PATH, HEADING_FONT_SIZE)
heading_text = "MENU"
heading_surface = heading_font.render(heading_text, True, HEADING_COLOR)

# Adjust heading position
heading_rect = heading_surface.get_rect(center=(WIDTH // 2, HEADING_FONT_SIZE // 2 + HEADING_VERTICAL_OFFSET))

def draw_images():
    """Draw the images in a 2x2 grid with spacing, centered on the screen."""
    screen.blit(background_image, (0, 0))  # Draw the background image
    
    # Draw the heading
    screen.blit(heading_surface, heading_rect.topleft)

    # Calculate positions with spacing
    img_width, img_height = IMAGE_SIZE
    spacing = IMAGE_SPACING
    grid_width = 2 * (img_width + spacing) - spacing
    grid_height = 2 * (img_height + spacing) - spacing
    start_x = (WIDTH - grid_width) // 2
    start_y = (HEIGHT - grid_height) // 2

    # Positions of images with spacing
    positions = [
        (start_x, start_y),                          # Top-left
        (start_x + img_width + spacing, start_y),    # Top-right
        (start_x, start_y + img_height + spacing),   # Bottom-left
        (start_x + img_width + spacing, start_y + img_height + spacing)  # Bottom-right
    ]
    
    for pos, img in zip(positions, loaded_images):
        screen.blit(img, pos)  # Draw image at specified position
    
    return positions

def main():
    intro_text = "BINEXE"
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                image_positions = draw_images()  # Draw images and get their positions
                img_width, img_height = IMAGE_SIZE
                for idx, (pos_x, pos_y) in enumerate(image_positions):
                    rect = pygame.Rect(pos_x, pos_y, img_width, img_height)
                    if rect.collidepoint(mouse_x, mouse_y):
                        open_file(file_paths[idx])  # Open corresponding file
                        running = False
                        break

        draw_text(intro_text, WIDTH // 2 - font.size(intro_text)[0] // 2, HEIGHT // 2 - font.size(intro_text)[1] // 2)
        pygame.display.flip()  # Update the display
        
        # Wait for the typewriter effect to complete
        pygame.time.wait(int(len(intro_text) * TEXT_SPEED * 1000))

        # Draw images and wait for user interaction
        pygame.time.wait(1400)  # Wait before showing images
        draw_images()  # Draw the images on the screen
        pygame.display.flip()  # Update the display
        pygame.time.wait(3000)

    pygame.quit()

if __name__ == "__main__":
    main()
