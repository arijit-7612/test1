import pygame
import sys
import os
import subprocess
import platform

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1350, 750
IMAGE_SIZE = (300, 200)  # Size of each rectangle (width, height)
IMAGE_SPACING = 50  # Space between images
HEADING_FONT_SIZE = 72  # Font size for heading
HEADING_COLOR = (139, 69, 19)  # Color for heading text
HEADING_VERTICAL_OFFSET = 50  # Vertical offset for heading

# Paths to assets
BACKGROUND_IMAGE_PATH = "background.jpeg"  # Path to background image
IMAGE_PATHS = ["preamble.jpg", "PRINCIPLES.jpg", "RIGHTS.jpg", "DUTIES.jpg"]
FILE_PATHS = ["new_preamble.py", "comingsoon.jpg", "test3.py", "comingsoon.jpg"]
CUSTOM_FONT_PATH = "times_new.ttf"  # Path to custom font file

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Menu')

def load_image(file_path, size=None):
    """Load and optionally resize an image."""
    try:
        image = pygame.image.load(file_path)
        return pygame.transform.scale(image, size) if size else image
    except pygame.error as e:
        print(f"Error loading image {file_path}: {e}")
        sys.exit()

def load_font(file_path, size):
    """Load a custom font."""
    try:
        return pygame.font.Font(file_path, size)
    except pygame.error as e:
        print(f"Error loading font {file_path}: {e}")
        sys.exit()

# Load assets
background_image = load_image(BACKGROUND_IMAGE_PATH, (WIDTH, HEIGHT))
loaded_images = [load_image(path, IMAGE_SIZE) for path in IMAGE_PATHS]
heading_font = load_font(CUSTOM_FONT_PATH, HEADING_FONT_SIZE)
heading_surface = heading_font.render("MENU", True, HEADING_COLOR)
heading_rect = heading_surface.get_rect(center=(WIDTH // 2, HEADING_FONT_SIZE // 2 + HEADING_VERTICAL_OFFSET))

def draw_images():
    """Draw background, heading, and images in a grid."""
    screen.blit(background_image, (0, 0))  # Draw the background image
    screen.blit(heading_surface, heading_rect.topleft)  # Draw the heading text
    img_width, img_height = IMAGE_SIZE   # Calculate image positions
    spacing = IMAGE_SPACING
    grid_width = 2 * (img_width + spacing) - spacing
    grid_height = 2 * (img_height + spacing) - spacing
    start_x = (WIDTH - grid_width) // 2
    start_y = (HEIGHT - grid_height) // 2
    positions = [
        (start_x, start_y),                          # Top-left
        (start_x + img_width + spacing, start_y),    # Top-right
        (start_x, start_y + img_height + spacing),   # Bottom-left
        (start_x + img_width + spacing, start_y + img_height + spacing)  # Bottom-right
    ]
    
    for pos, img in zip(positions, loaded_images):
        screen.blit(img, pos)  # Draw image at specified position
    return positions

def open_file(file_path):
    """Open a file using the default application."""
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.call(["open", file_path])
        else:
            subprocess.call(["xdg-open", file_path])
    except Exception as e:
        print(f"Error opening file {file_path}: {e}")

def main():
    """Main function to run the Pygame loop."""
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
                        open_file(FILE_PATHS[idx])  # Open corresponding file
                        running = False  # Exit after opening the file
                        break

        draw_images()  # Ensure images are always drawn
        pygame.display.flip()  # Update the display
    pygame.quit()
if __name__ == "__main__":
    main()

