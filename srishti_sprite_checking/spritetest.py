import pygame
import sys

pygame.init()

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
background_image = pygame.image.load("court.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
sprite_sheetl1 = pygame.image.load("sprite14_1.png").convert_alpha()
sprite_sheetj = pygame.image.load("judge.png").convert_alpha()

# Dialogue data
dialogues = [
    "Judge Singh: This court is now in session. The case before us today is Tanisha vs. Principal Sharma. Ms. Dey, please proceed with your arguments.",
    "Ms. Dey: Thank you, Your Honor. My client, Tanisha, was denied admission to the school's science program based on her gender, despite others with similar credentials were granted admission.",
    "Mr. Jain: Objection, Your Honor! The decision was made due to limited seats and Amina's academic performance",
    "Ms. Dey: But, Your Honor, Tanisha grades were equal or sometimes more to those of her male peers who were admitted. This is a clear case of gender discrimination",
    "Judge Singh: I'll hear both sides. Mr. Jain, can you explain the school's admission criteria?",
    "Mr. Jain: Yes, Your Honor. We consider grades, aptitude tests, and extracurricular activities. We have provided the court with the document of the same",
    "Judge Singh: And did Tanisha meet these criteria?",
    "Mr. Jain: (hesitantly) She... uh... met some of them",
    "Ms. Dey: (smiling) I think we have a case of bias here, Your Honor",
    "Judge Singh: (sternly) Principal Sharma, can you explain why Tanisha was denied admission?",
    "Principal Sharma: (nervously) We... uh... wanted to maintain a high quality student body. Moreover, we admit the candidates that have higher chances of a bright future",
    "Ms Dey: High quality student body? By denying a qualified female student admission?",
    "Ms Dey: Principal Sharma, what made you believe so strongly that my client Tanisha does not have a bright future, despite having the same or better credentials than her male counterpart.",
    "Principal Sharma: We believe that girls have a higher inclination towards the humanities subjects as compared to boys who excel in the field of STEM. Apart from that, girls and their families tend to shift their focus on marriage, after they have completed their education. Thus, we believe the top quality education we provide, is better utilized by a male candidate.",
    "Ms Dey: Your Honour, that comment is based on outdated gender stereotypes, and an educated man who leads an institution, still practicing it, shouldn't be allowed to lead in the first place.",
    "Mr Jain: Objection, Your Honour, this is the plaintiff's attempt to defame my client and harm his reputation as an educator.",
    "Judge Singh: Objection overruled. Ms Dey, please continue",
    "Ms Dey: Thank you, Your Honour.  According to the constitution, Educational institutions or policies require to treat students equally based on gender, such as providing equal opportunities or resources for all genders. Thus Principal Sharma is in violation of Article 14 of the Indian Constitution on grounds of unequal treatment of my client, on gender-based biases leading to her exclusion from certain educational opportunities or programs",
    "Judge Singh: Order, order. Silence in my court. Continue, Ms Dey",
    "Ms Dey: Your Honour, if educational institutions or the State discriminate against students based on gender, such as by denying admission, scholarships, or other educational benefits to one gender, it constitutes a violation of Article 15(1), which Mr Sharma is clearly in violation of. Apart from that, he is also in violation of Article 21 for practicing discrimination on the basis of gender bias at his educational institution, in turn violating her fundamental right to education.",
    "Ms Dey: Thus, your Honour, I request the court to issue a directive to the institution to admit my client, Ms Tanisha, with all due respect with appropriate compensation for the harassment she faced.",
    "Judge Singh: Do you have any other arguments?",
    "Judge Singh: I find Principal Sharma and the institute guilty of violating Article 14, 15, and 21 of the Indian Constitution The decision to deny admission based on gender is discriminatory and unacceptable. This court is issuing a directive to admit Ms Tanisha to the institution, in context of her credentials. Along with that, the court orders, Mr Sharma and the institution to provide a compensation amount of rupees, 36000, for the harassment she faced.",
    "Judge Singh: (banging his gavel) Order! I'll have order in this court! Ms Dey, your client is entitled to admission to the science program and compensation for the discrimination she faced.The court is adjourned.",
    "Ms. Dey : Thank you, Your Honor.",
    "Judge Singh: (to himself) Education is the key to unlocking potential. No one should be denied that right based on their gender."
]
current_dialogue_index = 0  # Index to track current dialogue

# Font setup
font = pygame.font.Font("times_new.ttf", FONT_SIZE)  # Load default font

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
        text_rect = text_surface.get_rect(center=(dialogue_box_rect.centerx, dialogue_box_rect.y+ y_offset + FONT_SIZE // 2 ))
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
frame_timer = 0  # Timer to control frame rate

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

    frame_timer += 1
    if frame_timer >= FPS:
        frame_timer = 0
        current_frame = (current_frame + 1) % len(frames)  # Update frame index

    screen.blit(background_image, (0, 0))  # Draw the background

    # Calculate sprite positions and draw sprites
    sprite_x = WIDTH // 2 - frames[0].get_width() // 2
    sprite_y = HEIGHT // 2 - frames[0].get_height() // 2
    screen.blit(frames[0], (sprite_x -160, sprite_y - 75))
    screen.blit(frames1[0], (sprite_x+25 , sprite_y - 153))

    # Draw dialogue box with text
    dialogue_lines = render_dialogue(dialogues[current_dialogue_index])
    draw_dialogue_box(dialogue_lines)

    pygame.display.flip()  # Update the display
    clock.tick(FPS)  # Control the frame rate

pygame.quit()
sys.exit()


