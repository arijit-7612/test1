import pygame
import sys
from moviepy.editor import VideoFileClip
import numpy as np
import pygame.surfarray as surfarray

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1350, 780
box_width, box_height = 325, 150
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Learning Constitution')
background_image = pygame.image.load("cont.jpeg")
background_image = pygame.transform.scale(background_image, (1600, height))
rights_images = [pygame.image.load(f'right{i}.jpg') for i in range(1, 7)]
for i in range(6):
    rights_images[i] = pygame.transform.scale(rights_images[i], (box_width, box_height))

def create_rounded_image(image, radius):
    rect = image.get_rect()
    rounded_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(rounded_surface, (255, 255, 255), rect, border_radius=radius)
    mask = pygame.mask.from_surface(rounded_surface)
    for x in range(rect.width):
        for y in range(rect.height):
            if not mask.get_at((x, y)):
                image.set_at((x, y), (0, 0, 0, 0))
    rounded_surface.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return rounded_surface

class Text():
    def __init__(self, font):
        self.font = font
        self.heading_font = pygame.font.Font(self.font, 74)
    
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

text = Text('times_new.ttf')

def play_intro_video(video_path):
    clip = VideoFileClip(video_path)
    for frame in clip.iter_frames(fps=24, dtype='uint8'):
        frame_surface = pygame.surfarray.make_surface(np.swapaxes(frame, 0, 1))  # Convert to Pygame surface
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        pygame.time.wait(int(1000 / 24))  # Wait for the duration of one frame

# Play intro video
play_intro_video("intro.mp4")

# Main game loop
run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(background_image, (-125, 0))
    text.draw_text('Learning Constitution of INDIA', text.heading_font, (255, 255, 255), screen, width // 2, 120)
    margin = 20
    x_start = (width - (box_width + margin) * 3) // 2
    y_start = 240
    for i, image in enumerate(rights_images):
        x = x_start + (i % 3) * (box_width + margin)
        y = y_start + (i // 3) * (box_height + margin)
        image = create_rounded_image(image, 30)
        screen.blit(image, (x, y))
    
    pygame.display.update()

pygame.quit()
