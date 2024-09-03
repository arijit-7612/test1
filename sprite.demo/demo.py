import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 14
BACKGROUND_COLOR = (200, 200, 200)  # Background color if needed

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-Sprite Animation")

background_image = pygame.image.load("court.jpg").convert()
sprite_sheets = [
    pygame.image.load("lawyer1.png").convert_alpha(),  # Sprite sheet for sprite 1
    pygame.image.load("lawyer2.png").convert_alpha(),  # Sprite sheet for sprite 2
    pygame.image.load("judge.png").convert_alpha(),  # Sprite sheet for sprite 3
    pygame.image.load("citizen1.png").convert_alpha(),  # Sprite sheet for sprite 4
    pygame.image.load("citizen2.png").convert_alpha()   # Sprite sheet for sprite 5
]

# Sprite data
sprite_data = [
    {"frame_width": 64, "frame_height": 64, "num_frames": 13, "scale_factor": 4},
    {"frame_width": 64, "frame_height": 64, "num_frames": 13, "scale_factor": 4},
    {"frame_width": 64, "frame_height": 64, "num_frames": 20, "scale_factor": 4},
    {"frame_width": 32, "frame_height": 32, "num_frames": 14, "scale_factor": 4},
    {"frame_width": 32, "frame_height": 32, "num_frames": 14, "scale_factor": 4}
]

# Load frames for each sprite
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

# Create a list to store frames for each sprite
sprite_frames = []
for i, data in enumerate(sprite_data):
    frames = load_frames(sprite_sheets[i], data["frame_width"], data["frame_height"], data["num_frames"], data["scale_factor"])
    sprite_frames.append(frames)

# Initialize sprite states
current_frames = [0] * len(sprite_frames)
frame_delay = 0.2
frame_timers = [0] * len(sprite_frames)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update frames for each sprite
    for i in range(len(sprite_frames)):
        frame_timers[i] += 1
        if frame_timers[i] >= frame_delay * FPS:
            frame_timers[i] = 0
            current_frames[i] = (current_frames[i] + 1) % len(sprite_frames[i])

    # Draw everything
    screen.blit(background_image, (0, 0))

    for i in range(len(sprite_frames)):
        # Calculate sprite position
        frame_width = sprite_data[i]["frame_width"] * sprite_data[i]["scale_factor"]
        frame_height = sprite_data[i]["frame_height"] * sprite_data[i]["scale_factor"]
        sprite_x = WIDTH // (len(sprite_frames) + 1) * (i + 1) - frame_width // 2
        sprite_y = HEIGHT // 2 - frame_height // 2
        screen.blit(sprite_frames[i][current_frames[i]], (sprite_x, sprite_y))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
