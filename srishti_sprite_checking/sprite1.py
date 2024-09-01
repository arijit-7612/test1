import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 14

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Sheet Animation")

sprite_sheet = pygame.image.load("sprite14_1.png").convert_alpha()

clock = pygame.time.Clock()



def load_frames(sprite_sheet, frame_width, frame_height, num_frames, scale_factor):
    sheet_width, sheet_height = sprite_sheet.get_size()
    
    
    if frame_width * num_frames > sheet_width or frame_height > sheet_height:
        raise ValueError("Frame dimensions or number of frames exceeds sprite sheet size")
    
    frames = []
    for i in range(num_frames):
        
        x_position = i * frame_width
        if x_position + frame_width > sheet_width:
            raise ValueError(f"Frame {i} is outside the sprite sheet bounds")
        
        frame = sprite_sheet.subsurface(pygame.Rect(x_position, 0, frame_width, frame_height))
        
        if scale_factor != 1:
            scaled_width = int(frame_width * scale_factor)
            scaled_height = int(frame_height * scale_factor)
            frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
        
        
        frames.append(frame)
    return frames


frame_width = 32 
frame_height = 32 
num_frames = 14  
scale_factor = 4

frames = load_frames(sprite_sheet, frame_width, frame_height, num_frames, scale_factor)


current_frame = 0
frame_delay = 0.2
frame_timer = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_timer += 1
    if frame_timer >= frame_delay:
        frame_timer = 0
        current_frame = (current_frame + 1) % num_frames 

    screen.fill((0, 0, 0))

    
    screen.blit(frames[current_frame], (WIDTH // 2 - frame_width // 2, HEIGHT // 2 - frame_height // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
