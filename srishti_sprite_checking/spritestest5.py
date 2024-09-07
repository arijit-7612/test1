import pygame
import sys
import requests
import uuid
import json

pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1350, 750
FPS = 28
DIALOGUE_BOX_HEIGHT = 150
FONT_SIZE = 22

# Setup screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multilingual Court Game")
clock = pygame.time.Clock()

# Microsoft Translate API setup
subscription_key = "YOUR_SUBSCRIPTION_KEY_HERE"
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "YOUR_RESOURCE_LOCATION"

# Supported Indian languages
languages = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa"
}

current_language = "English"

# Function to translate text
def translate_text(text, target_language):
    if target_language == "en":  # No need to translate if target is English
        return text
    
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    try:
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        result = response.json()
        
        if result and isinstance(result, list) and len(result) > 0:
            translations = result[0].get('translations', [])
            if translations and len(translations) > 0:
                return translations[0].get('text', text)
        
        print(f"Unexpected API response format: {result}")
        return text  # Return original text if translation fails
    except requests.exceptions.RequestException as e:
        print(f"Translation API error: {e}")
        return text  # Return original text if API call fails

# Load assets
pygame.mixer.music.load("murmur1.mp3")
pygame.mixer.music.play(-1)

background_image = pygame.image.load("court.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
sprite_sheetl1 = pygame.image.load("sprite14_1.png").convert_alpha()
sprite_sheetj = pygame.image.load("judge.png").convert_alpha()
sprite_sheetld = pygame.image.load("lawyer_dey.png").convert_alpha()
sprite_sheetl = pygame.image.load("lawyer_sprite.png").convert_alpha()

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
    # ... (add the rest of the dialogues here)
]

translated_dialogues = dialogues.copy()
current_dialogue_index = 0

font = pygame.font.Font("times_new.ttf", FONT_SIZE)

# Function to render dialogue text into multiple lines if necessary
def render_dialogue(dialogue):
    words = dialogue.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < WIDTH - 200:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    
    return lines

# Function to draw the dialogue box and text
def draw_dialogue_box(lines):
    dialogue_box_rect = pygame.Rect(100, 585, WIDTH - 200, DIALOGUE_BOX_HEIGHT)
    pygame.draw.rect(screen, (92, 64, 51), dialogue_box_rect)
    pygame.draw.rect(screen, (0, 0, 0), dialogue_box_rect, 2)

    y_offset = (DIALOGUE_BOX_HEIGHT - len(lines) * (FONT_SIZE + 5)) // 2
    for line in lines:
        text_surface = font.render(line, True, (245, 245, 220))
        text_rect = text_surface.get_rect(center=(dialogue_box_rect.centerx, dialogue_box_rect.y + y_offset + FONT_SIZE // 2))
        screen.blit(text_surface, text_rect)
        y_offset += FONT_SIZE + 5

# Function to load frames from a sprite sheet
def load_frames(sprite_sheet, frame_width, frame_height, num_frames, scale_factor):
    frames = []
    for i in range(num_frames):
        frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (int(frame_width * scale_factor), int(frame_height * scale_factor)))
        frames.append(frame)
    return frames

# Load frames from the sprite sheets
frames = load_frames(sprite_sheetl1, 32, 32, 14, 6)
frames1 = load_frames(sprite_sheetj, 80, 64, 20, 2.5)
frames2 = load_frames(sprite_sheetld, 64, 64, 15, 2.8)
frames3 = load_frames(sprite_sheetl, 64, 64, 13, 2.8)

# Button class for language selection
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, 24)
        self.text_surface = self.font.render(text, True, (255, 255, 255))

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

# Create language selection buttons
language_buttons = []
for i, lang in enumerate(languages.keys()):
    button = Button(lang, 10, 10 + i * 40, 150, 30, (70, 130, 180), (100, 160, 210))
    language_buttons.append(button)

# Main game loop
running = True
current_frame = 0
frame_timer = 0
fadeout_complete = False
new_audio_ready = False
fadeout_start_time = 0
audioplay = False
popup_displayed = False

while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_dialogue_index = (current_dialogue_index + 1) % len(dialogues)
                if current_dialogue_index == 6 and not popup_displayed:
                    show_popup()
                    popup_displayed = True
            if event.key == pygame.K_LEFT:
                current_dialogue_index = (current_dialogue_index - 1) % len(dialogues)
        
        # Handle language selection
        for button in language_buttons:
            if button.is_clicked(event):
                new_language = button.text
                if new_language != current_language:
                    current_language = new_language
                    # Translate all dialogues
                    for i, dialogue in enumerate(dialogues):
                        translated_dialogues[i] = translate_text(dialogue, languages[current_language])
                    print(f"Switched to {current_language}")

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
    screen.blit(frames2[0], (sprite_x +250, sprite_y ))
    screen.blit(frames3[0], (sprite_x -280, sprite_y))
    if current_dialogue_index != 18:
        screen.blit(frames1[0], (sprite_x+25 , sprite_y - 153))

    
    dialogue_lines = render_dialogue(dialogues[current_dialogue_index])
    draw_dialogue_box(dialogue_lines)

    for button in language_buttons:
        button.draw(screen)

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