import pygame
import sys
import time

pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1350, 750  # Screen dimensions
FPS = 14  # Frames per second
DIALOGUE_BOX_HEIGHT = 150  # Height of the dialogue box
FONT_SIZE = 25  # Font size for dialogue text

# Setup screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Sheet Animation")
clock = pygame.time.Clock()

# Load assets (background and sprite sheets)
pygame.mixer.music.load("murmur1.mp3")
pygame.mixer.music.play(-1)
background_image = pygame.image.load("court.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
sprite_sheetl1 = pygame.image.load("sprite14_1.png").convert_alpha()
sprite_sheetj = pygame.image.load("judge.png").convert_alpha()

# Dialogue data
dialogues = [
    # Your dialogue data here
]
current_dialogue_index = 0  # Index to track current dialogue

# Font setup
font = pygame.font.Font(None, FONT_SIZE)  # Load default font

# Function to render dialogue text into multiple lines if necessary
def render_dialogue(dialogue):
    words = dialogue.split(' ')  # Split the dialogue into words
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < WIDTH - 40:  # Check if the line fits within the dialogue box
            current_line = test_line
        else:
            lines.append(current_line)  # Start a new line if it doesn't fit
            current_line = word + " "
    lines.append(current_line)  # Add the last line
    
    return lines

# Function to draw the dialogue box and text
def draw_dialogue_box(lines):
    dialogue_box_rect = pygame.Rect(5, 5, WIDTH - 40, DIALOGUE_BOX_HEIGHT)  # Dialogue box dimensions
    pygame.draw.rect(screen, (92, 64, 51), dialogue_box_rect)  # Draw the background of the dialogue box
    pygame.draw.rect(screen, (0, 0, 0), dialogue_box_rect, 2)  # Draw the border

    y_offset = (DIALOGUE_BOX_HEIGHT - len(lines) * (FONT_SIZE + 5)) // 2  # Center the text vertically
    for line in lines:
        text_surface = font.render(line, True, (245, 245, 220))  # Render text in white
        text_rect = text_surface.get_rect(center=(dialogue_box_rect.centerx, dialogue_box_rect.y + y_offset + FONT_SIZE // 2))
        screen.blit(text_surface, text_rect)
        y_offset += FONT_SIZE + 5  # Adjust for next line

# Function to load frames from a sprite sheet
def load_frames(sprite_sheet, frame_width, frame_height, num_frames, scale_factor):
    frames = []
    for i in range(num_frames):
        frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))  # Extract a frame
        frame = pygame.transform.scale(frame, (int(frame_width * scale_factor), int(frame_height * scale_factor)))  # Scale the frame
        frames.append(frame)
    return frames

# Load frames from the sprite sheets
frames = load_frames(sprite_sheetl1, 32, 32, 14, 6)
frames1 = load_frames(sprite_sheetj, 80, 64, 20, 2.5)

current_frame = 0  # Current frame index for animation
frame_timer = pygame.time.get_ticks()  # Timer to control frame rate

# For audio playback timing
audio_start_time = pygame.time.get_ticks()
new_audio_ready = True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            dialogue_box_rect = pygame.Rect(20, 20, WIDTH - 40, DIALOGUE_BOX_HEIGHT)
            if dialogue_box_rect.collidepoint(mouse_pos):  # Check if the dialogue box was clicked
                current_dialogue_index = (current_dialogue_index + 1) % len(dialogues)  # Move to the next dialogue

    # Handle animation
    current_time = pygame.time.get_ticks()
    if current_time - frame_timer >= 1000 // FPS:
        frame_timer = current_time
        current_frame = (current_frame + 1) % len(frames)  # Update frame index

    screen.blit(background_image, (0, 0))  # Draw the background

    if current_dialogue_index == 18:
        sprite_x = WIDTH // 2 - frames1[0].get_width() // 2
        sprite_y = HEIGHT // 2 - frames1[0].get_height() // 2
        screen.blit(frames1[current_frame], (sprite_x + 25, sprite_y - 153))
        
        if new_audio_ready:
            if current_time - audio_start_time >= 1000:  # Check if 1 second has passed
                pygame.mixer.music.load("hammer.mp3")
                pygame.mixer.music.play(-1)
                pygame.time.wait(500)  # Optional: Wait for a short time to ensure audio is playing
                pygame.mixer.music.stop()
                new_audio_ready = False

    # Draw dialogue box with text
    dialogue_lines = render_dialogue(dialogues[current_dialogue_index])
    draw_dialogue_box(dialogue_lines)

    pygame.display.flip()  # Update the display
    clock.tick(FPS)  # Control the frame rate

pygame.quit()
sys.exit()
