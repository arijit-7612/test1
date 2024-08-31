import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1350, 780
box_width, box_height = 325, 150
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Learning Constitution')
background_image = pygame.image.load("cont.jpeg")
background_image = pygame.transform.scale(background_image, (1600,height))
rights_images = [pygame.image.load(f'right{i}.jpg') for i in range(1, 7)]
for i in range(6):
    rights_images[i] = pygame.transform.scale(rights_images[i], (box_width, box_height))
# Load background image
def create_rounded_image(image, radius):
    rect = image.get_rect()
    
    # Create a surface for the rounded image with an alpha channel (transparency)
    rounded_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Draw rounded rectangle on this surface
    pygame.draw.rect(rounded_surface, (255, 255, 255), rect, border_radius=radius)
    
    # Create a mask from the rounded rectangle surface
    mask = pygame.mask.from_surface(rounded_surface)
    
    # Apply the mask to the image by setting transparent pixels
    for x in range(rect.width):
        for y in range(rect.height):
            if not mask.get_at((x, y)):
                image.set_at((x, y), (0, 0, 0, 0))  # Make pixels outside the rounded area transparent
    
    # Blit the original image onto the rounded surface
    rounded_surface.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    return rounded_surface

# Main game loop
class Text():
    def __init__(self,font):
        self.font=font
        self.heading_font = pygame.font.Font(self.font, 74)     
    def draw_text(self,text, font, color, surface, x, y):
        self.textobj = font.render(text, True, color)
        self.textrect = self.textobj.get_rect()
        self.textrect.center = (x, y)
        surface.blit(self.textobj, self.textrect)

text=Text('times_new.ttf')
run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    screen.blit(background_image, (-125, 0))

    text.draw_text('Learning Constitution of INDIA',text.heading_font,(255,255,255), screen, width // 2, 120)
    margin = 20
    x_start = (width - (box_width + margin) * 3) // 2
    y_start = 240
    for i, image in enumerate(rights_images):
        x = x_start + (i % 3) * (box_width + margin)
        y = y_start + (i // 3) * (box_height + margin)
        image = create_rounded_image(image, 30)
        screen.blit(image, (x , y))
    
    pygame.display.update()