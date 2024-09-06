import pygame
import sys
import subprocess


pygame.init()


width,height = 1350, 750
IMAGE_SIZE = (250, 150)
BACKGROUND_COLOR = (0, 0, 0)
HEADING_FONT_SIZE = 72
HEADING_COLOR = (139, 69, 19)


file_paths = ["preamble.py", "comingsoon.jpg", "test3.py", "comingsoon.jpg"]
image_paths = ["preamble.jpg", "PRINCIPLES.jpg", "RIGHTS.jpg", "DUTIES.jpg"]

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('MENU')

# Load images
background_image = pygame.image.load("background.jpeg").convert()
background_image = pygame.transform.scale(background_image, (width, height))
loaded_images = [pygame.transform.scale(pygame.image.load(img), IMAGE_SIZE) for img in image_paths]

# Load font
heading_font = pygame.font.Font("times_new.ttf", HEADING_FONT_SIZE)
heading_surface = heading_font.render("MENU", True, HEADING_COLOR)
heading_rect = heading_surface.get_rect(center=(width // 2, HEADING_FONT_SIZE // 2 + 110))

def draw_menu():

    
    x_start = (width - 2 * IMAGE_SIZE[0]) //3  +90
    y_start = height // 3 

    for i, img in enumerate(loaded_images):
        row = i // 2
        col = i % 2
        
        x_pos = x_start + col * (IMAGE_SIZE[0] + x_start-270)  
        y_pos = y_start + row * (IMAGE_SIZE[1] + 50) 
        screen.blit(img, (x_pos, y_pos))

    

# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False  
    screen.blit(background_image, (0, 0))
    screen.blit(heading_surface, heading_rect.topleft)
    draw_menu()
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()


