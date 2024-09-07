import pygame
import sys
import requests

pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1350, 750
FPS = 28
DIALOGUE_BOX_HEIGHT = 150
FONT_SIZE = 25

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

# Translator API constants
TRANSLATOR_API_KEY = 'YOUR_API_KEY'
TRANSLATOR_ENDPOINT = 'https://api.cognitive.microsofttranslator.com'
TRANSLATOR_LOCATION = 'YOUR_RESOURCE_LOCATION'
TRANSLATE_URL = f'{TRANSLATOR_ENDPOINT}/translate?api-version=3.0'

# Font setup
font = pygame.font.Font("times_new.ttf", FONT_SIZE)
font1 = pygame.font.Font("times_new.ttf", 16)

# Dialogue data
dialogues = [
    "Judge Singh: This court is now in session. The case before us today is Tanisha vs. Principal Sharma. Ms. Dey, please proceed with your arguments.",
    "Ms. Dey: Thank you, Your Honor. My client, Tanisha, was denied admission to the school's science program based on her gender, despite others with similar credentials were granted admission.",
    "Mr. Jain: Objection, Your Honor! The decision was made due to limited seats and Amina's academic performance.",
    "Ms. Dey: But, Your Honor, Tanisha's grades were equal or sometimes more than those of her male peers who were admitted. This is a clear case of gender discrimination.",
    "Judge Singh: I'll hear both sides. Mr. Jain, can you explain the school's admission criteria?",
    "Mr. Jain: Yes, Your Honor. We consider grades, aptitude tests, and extracurricular activities. We have provided the court with the document of the same.",
    "Judge Singh: And did Tanisha meet these criteria?",
    "Mr. Jain: (hesitantly) She... uh... met some of them.",
    "Ms. Dey: (smiling) I think we have a case of bias here, Your Honor.",
    "Judge Singh: (sternly) Principal Sharma, can you explain why Tanisha was denied admission?",
    "Principal Sharma: (nervously) We... uh... wanted to maintain a high quality student body. Moreover, we admit the candidates that have higher chances of a bright future.",
    "Ms Dey: High quality student body? By denying a qualified female student admission?",
    "Ms Dey: Principal Sharma, what made you believe so strongly that my client Tanisha does not have a bright future, despite having the same or better credentials than her male counterpart?",
    "Principal Sharma: We believe that girls have a higher inclination towards the humanities subjects as compared to boys who excel in the field of STEM. Apart from that, girls and their families tend to shift their focus on marriage, after they have completed their education. Thus, we believe the top quality education we provide is better utilized by a male candidate.",
    "Ms Dey: Your Honour, that comment is based on outdated gender stereotypes, and an educated man who leads an institution, still practicing it, shouldn't be allowed to lead in the first place.",
    "Mr Jain: Objection, Your Honour, this is the plaintiff's attempt to defame my client and harm his reputation as an educator.",
    "Judge Singh: Objection overruled. Ms Dey, please continue.",
    "Ms Dey: Thank you, Your Honour. According to the constitution, Educational institutions or policies require to treat students equally based on gender, such as providing equal opportunities or resources for all genders. Thus Principal Sharma is in violation of Article 14 of the Indian Constitution on grounds of unequal treatment of my client, on gender-based biases leading to her exclusion from certain educational opportunities or programs.",
    "Judge Singh: Do you have any other arguments?",
    "Judge Singh: I find Principal Sharma and the institute guilty of violating Article 14, 15, and 21 of the Indian Constitution. The decision to deny admission based on gender is discriminatory and unacceptable. This court is issuing a directive to admit Ms Tanisha to the institution, in context of her credentials. Along with that, the court orders Mr Sharma and the institution to provide a compensation amount of rupees, 36000, for the harassment she faced.",
    "Judge Singh: (banging his gavel) Order! I'll have order in this court! Ms Dey, your client is entitled to admission to the science program and compensation for the discrimination she faced. The court is adjourned.",
    "Ms. Dey: Thank you, Your Honor.",
    "Judge Singh: (to himself) Education is the key to unlocking potential. No one should be denied that right based on their gender."
]
current_dialogue_index = 0
popup_displayed = False

def translate_text(text, target_language):
    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_API_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATOR_LOCATION,
        'Content-Type': 'application/json'
    }
    params = {
        'to': target_language
    }
    body = [{'text': text}]
    response = requests.post(TRANSLATE_URL, headers=headers, params=params, json=body)
    response.raise_for_status()
    translation = response.json()[0]['translations'][0]['text']
    return translation

def draw_language_button(surface, text, x, y, width, height, color, hover_color, font, selected_language):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, button_rect)
        if pygame.mouse.get_pressed()[0]:
            return button_rect, text
    else:
        pygame.draw.rect(surface, color, button_rect)
    text_surface = font.render(text, True, (255, 255, 255))
    surface.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
    return None, None

def show_language_menu():
    LANGUAGES = {
        'Hindi': 'hi',
        'Bengali': 'bn',
        'Telugu': 'te',
        'Marathi': 'mr',
        'Tamil': 'ta',
        'Urdu': 'ur'
    }
    
    menu_surface = pygame.Surface((300, 300))
    menu_surface.fill((200, 200, 200))
    
    font = pygame.font.Font(None, 24)
    buttons = []
    
    y = 50
    for lang, code in LANGUAGES.items():
        button, lang_code = draw_language_button(menu_surface, lang, 50, y, 200, 40, (0, 0, 255), (0, 128, 255), font, code)
        if button:
            return lang_code
        buttons.append((button, code))
        y += 50

    screen.blit(menu_surface, (WIDTH // 2 - 150, HEIGHT // 2 - 150))
    pygame.display.flip()
    
    selected_language = None
    menu_active = True
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, code in buttons:
                    if button.collidepoint(event.pos):
                        selected_language = code
                        menu_active = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu_active = False
                
    return selected_language

def render_dialogue(dialogue):
    words = dialogue.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < WIDTH - 40:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    
    return lines

def draw_dialogue_box(lines):
    dialogue_box_rect = pygame.Rect(5, HEIGHT - DIALOGUE_BOX_HEIGHT - 5, WIDTH - 40, DIALOGUE_BOX_HEIGHT)
    pygame.draw.rect(screen, (92, 64, 51), dialogue_box_rect)
    pygame.draw.rect(screen, (0, 0, 0), dialogue_box_rect, 2)

    y_offset = (DIALOGUE_BOX_HEIGHT - len(lines) * (FONT_SIZE + 5)) // 2
    for line in lines:
        text_surface = font.render(line, True, (245, 245, 220))
        text_rect = text_surface.get_rect(center=(dialogue_box_rect.centerx, dialogue_box_rect.y + y_offset + FONT_SIZE // 2))
        screen.blit(text_surface, text_rect)
        y_offset += FONT_SIZE + 5

def load_frames(sprite_sheet, frame_width, frame_height, num_frames, scale_factor):
    frames = []
    for i in range(num_frames):
        frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (int(frame_width * scale_factor), int(frame_height * scale_factor)))
        frames.append(frame)
    return frames

def show_popup():
    POPUP_WIDTH, POPUP_HEIGHT = 600, 600
    GREY = (100, 100, 100)
    BLUE = (70, 130, 180)
    BLACK = (0, 0, 0)
    
    popup_surface = pygame.Surface((POPUP_WIDTH, POPUP_HEIGHT))
    popup_surface.fill(GREY)
    
    popup_x = (WIDTH - POPUP_WIDTH) // 2

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

    close_button = pygame.Rect(POPUP_WIDTH // 2 - 50, POPUP_HEIGHT - 60, 100, 50)
    pygame.draw.rect(popup_surface, BLUE, close_button)
    close_text = font1.render("Close", True, BLACK)
    popup_surface.blit(close_text, (close_button.x + (close_button.width - close_text.get_width()) // 2, 
                                    close_button.y + (close_button.height - close_text.get_height()) // 2))

    popup_active = True
    while popup_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    popup_active = False

        screen.blit(background_image, (0, 0))
        screen.blit(popup_surface, (popup_x, 75))
        pygame.display.flip()
        clock.tick(FPS)

frames = load_frames(sprite_sheetl1, 32, 32, 14, 6)
frames1 = load_frames(sprite_sheetj, 80, 64, 20, 2.5)

sprite_index = 0
frame_rate = 5
last_update = pygame.time.get_ticks()

selected_language = None
translate_text_cache = {}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_dialogue_index = (current_dialogue_index + 1) % len(dialogues)
                if current_dialogue_index == 6 and not popup_displayed:
                    show_popup()
                    popup_displayed = True
            elif event.key == pygame.K_t:
                selected_language = show_language_menu()
                if selected_language:
                    translate_text_cache = {}
                    for i, dialogue in enumerate(dialogues):
                        if dialogue not in translate_text_cache:
                            translate_text_cache[dialogue] = translate_text(dialogue, selected_language)

    screen.blit(background_image, (0, 0))
    
    # Draw sprites
    screen.blit(frames[sprite_index], (100, 100))
    screen.blit(frames1[sprite_index % len(frames1)], (400, 300))
    
    # Update sprite animation
    now = pygame.time.get_ticks()
    if now - last_update > 1000 / frame_rate:
        sprite_index = (sprite_index + 1) % len(frames)
        last_update = now

    # Render dialogue
    dialogue = dialogues[current_dialogue_index]
    translated_dialogue = translate_text_cache.get(dialogue, dialogue)
    lines = render_dialogue(translated_dialogue)
    draw_dialogue_box(lines)

    pygame.display.flip()
    clock.tick(FPS)


