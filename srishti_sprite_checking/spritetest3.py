import pygame
import sys

pygame.init()
pygame.mixer.init()
# Constants
WIDTH, HEIGHT = 1350, 750  # Screen dimensions
FPS = 28  # Frames per second
DIALOGUE_BOX_HEIGHT = 150  # Height of the dialogue box
FONT_SIZE = 25 # Font size for dialogue text

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
    dialogue_box_rect = pygame.Rect(5, 585, WIDTH - 40, DIALOGUE_BOX_HEIGHT)  # Dialogue box dimensions
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







# Screen constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1350, 750
FPS = 28

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Sheet Animation")

# Load assets for the popup
popup_background_image = pygame.image.load("popup_back.jpg")
popup_background_image = pygame.transform.scale(popup_background_image, (600, 600))

font1 = pygame.font.Font("times_new.ttf", 16)

# Button class for the close button inside the pop-up
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_surface = font1.render(text, True, (255, 255, 255))

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surface, (self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2,
                                         self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Function to render multiline text in the popup
def render_multiline_text(surface, text, x, y, font, color, line_spacing=5):
    lines = text.splitlines()  # Split the paragraph by new lines
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * (16 + line_spacing)))  # Adjust the y position for each line
def show_popup():
    POPUP_WIDTH, POPUP_HEIGHT = 600, 600
    GREY = (100, 100, 100)
    BLUE = (70, 130, 180)
    BLACK = (0, 0, 0)
    
    popup_surface = pygame.Surface((POPUP_WIDTH, POPUP_HEIGHT))
    popup_surface.blit(popup_background_image, (0, 0))

    popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2

    eligibility_text = """
    Eligibility Criteria for Grade 11 Science Stream:
    1. Academic Performance:
       - Minimum Percentage in Class 10: Students must have a minimum aggregate 
         score of 90% in Class 10 board exams.
       - Subject-wise Performance:
       - Mathematics: Minimum 90 or higher
       - Science: Minimum 90 or higher
       - Language Requirement: A passing grade (minimum 60%) in English.

    2. Interview/Personal Counseling:
       - Students are required to attend a personal interview or counseling session 
         to evaluate their interest in the Science stream and career aspirations.

    3. Availability of Seats:
       - Admission is subject to seat availability and the student's position in the 
         merit list.

    4. Extracurricular Achievements:
       - Additional points may be awarded for students excelling in science-related 
         activities such as Olympiads, competitions, or projects.

    5. Conduct and Behavior:
       - A positive conduct report from the previous school is typically required.
    """
    
    render_multiline_text(popup_surface, eligibility_text, 20, 20, font1, BLACK)

    close_button = Button("Close", POPUP_WIDTH // 2 + 320 , POPUP_HEIGHT , 100, 50, BLUE, BLACK)

    popup_active = True
    while popup_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if close_button.is_clicked(event):
                popup_active = False

        screen.blit(background_image, (0, 0))  # Redraw the background
        screen.blit(popup_surface, (popup_x, 75))
        close_button.draw(screen)  # Draw the button on the screen, not the popup surface
        pygame.display.flip()  
        clock.tick(FPS)

    return 












current_frame = 0  # Current frame index for animation
frame_timer = 0  # Timer to control frame rate

fadeout_complete = False
new_audio_ready = False
fadeout_start_time = 0
audioplay=False
popup_displayed=False
# Main game loop
running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                current_dialogue_index = (current_dialogue_index + 1) % len(dialogues) 
                if current_dialogue_index == 6 and not popup_displayed:
                    show_popup()
                    popup_displayed = True
            if event.key==pygame.K_LEFT:
                current_dialogue_index = (current_dialogue_index - 1) % len(dialogues) 
    frame_timer += 1
    if frame_timer >= FPS:
        frame_timer = 0
        current_frame = (current_frame + 1) % len(frames)  
    

    if current_dialogue_index == 11 and not fadeout_complete:
        pygame.mixer.music.fadeout(1500)
        fadeout_start_time = current_time
        fadeout_complete = True

    if current_dialogue_index == 17 and fadeout_complete and not new_audio_ready:
        if current_time - fadeout_start_time > 1500:  # Check if fadeout is complete
            pygame.mixer.music.load("loudmurmur.mp3")
            pygame.mixer.music.play(-1)
            audio_start_time = current_time
            new_audio_ready = True
    if current_dialogue_index == 22 and not audioplay :
        pygame.mixer.music.load("loudmurmur.mp3")
        pygame.mixer.music.play(-1)
        audioplay = True
        audioplay1=True
    if current_dialogue_index == 23 and audioplay1:
        pygame.mixer.music.fadeout(300) 
        sprite_x = WIDTH // 2 - frames[0].get_width() // 2
        sprite_y = HEIGHT // 2 - frames[0].get_height() // 2
        screen.blit(frames1[current_frame], (sprite_x + 25 , sprite_y - 153))
        clock.tick(20)
        t=1
        if t==1:
            pygame.mixer.music.load("hammer.mp3")
            pygame.mixer.music.play(-1)
            pygame.time.wait(500)
            pygame.mixer.music.stop()
            audioplay1 = False
        
    screen.blit(background_image, (0, 0))  # Draw the background

    sprite_x = WIDTH // 2 - frames[0].get_width() // 2
    sprite_y = HEIGHT // 2 - frames[0].get_height() // 2
    screen.blit(frames[0], (sprite_x -160, sprite_y - 75))
    if current_dialogue_index != 18:
        screen.blit(frames1[0], (sprite_x+25 , sprite_y - 153))

    
    dialogue_lines = render_dialogue(dialogues[current_dialogue_index])
    draw_dialogue_box(dialogue_lines)

    if current_dialogue_index == 18 :
        sprite_x = WIDTH // 2 - frames[0].get_width() // 2
        sprite_y = HEIGHT // 2 - frames[0].get_height() // 2
        screen.blit(frames1[current_frame], (sprite_x+25 , sprite_y - 153))
        clock.tick(20)
        if current_time - audio_start_time >= 1000 and new_audio_ready:  # Check if 1 second has passed
            pygame.mixer.music.load("hammer.mp3")
            pygame.mixer.music.play(-1)
            pygame.time.wait(500)  # Optional: Wait for a short time to ensure audio is playing
            pygame.mixer.music.stop()
            new_audio_ready = False


    pygame.display.flip()  # Update the display
    clock.tick(FPS)  # Control the frame rate

pygame.quit()
sys.exit()
