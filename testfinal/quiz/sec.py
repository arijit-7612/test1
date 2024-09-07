import pygame
import sys
import os

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
#BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT_SIZE = 32
LINE_HEIGHT = FONT_SIZE + 5

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quiz Game")
font = pygame.font.Font(None, FONT_SIZE)

# Load background image with error handling
background_path = "cont.jpeg"
if not os.path.exists(background_path):
    print(f"Error: The background image '{background_path}' does not exist.")
    sys.exit()

try:
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    sys.exit()

# Questions and answers
questions = [
    {"question": "1. Which article of the Constitution guarantees equality before the law?", "options": ["A) Article 12", "B) Article 14", "C) Article 16", "D) Article 17"], "answer": "B) Article 14"},
    {"question": "2. The abolition of untouchability is mentioned in which article?", "options": ["A) Article 15", "B) Article 16", "C) Article 17", "D) Article 18"], "answer": "C) Article 17"},
    {"question": "3. Article 16 guarantees equality of opportunity in matters of _____", "options": ["A) Education", "B) Public employment", "C) Freedom of speech", "D) Property"], "answer": "B) Public employment"},
    {"question": "4. Which article abolishes titles, except military and academic distinctions?", "options": ["A) Article 14", "B) Article 15", "C) Article 18", "D) Article 17"], "answer": "C) Article 18"},
    {"question": "5. Equality before law falls under which part of the Constitution?", "options": ["A) Part III", "B) Part IV", "C) Part V", "D) Part II"], "answer": "A) Part III"},
    {"question": "6. Article 15(3) allows special provisions for which of the following?", "options": ["A) Scheduled Castes", "B) Scheduled Tribes", "C) Women and children", "D) All citizens"], "answer": "C) Women and children"},
    {"question": "7. Which article provides for the abolition of titles in India?", "options": ["A) Article 16", "B) Article 18", "C) Article 15", "D) Article 14"], "answer": "B) Article 18"},
    {"question": "8. Reservation in public employment is provided under which article?", "options": ["A) Article 14", "B) Article 15", "C) Article 16(4)", "D) Article 18"], "answer": "C) Article 16(4)"},
    {"question": "9. Under which article can no citizen be discriminated against in the matter of employment?", "options": ["A) Article 17", "B) Article 14", "C) Article 16", "D) Article 18"], "answer": "C) Article 16"}
]

current_question = 0

class TextAlign:
    def __init__(self, text, font, rect, h_align=1, v_align=1, color=WHITE):
        self.text = text
        self.font = font
        self.rect = rect
        self.h_align = h_align
        self.v_align = v_align
        self.color = color
        self.text_img = self.font.render(self.text, True, self.color)
        self.img0 = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.align_text()

    def align_text(self):
        w, h = self.rect.size
        w0, h0 = self.text_img.get_size()
        if self.h_align == 0:
            x = 0
        elif self.h_align == 1:
            x = (w - w0) // 2
        else:
            x = w - w0

        if self.v_align == 0:
            y = 0
        elif self.v_align == 1:
            y = (h - h0) // 2
        else:
            y = h - h0

        self.img0.blit(self.text_img, (x, y))
        self.img = self.img0.copy()

    def draw(self, surface):
        surface.blit(self.img, self.rect.topleft)

def draw_text(text, rect, max_width=None, h_align=1, v_align=1):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if max_width and font.size(test_line)[0] > max_width:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line
    lines.append(current_line)

    total_height = len(lines) * LINE_HEIGHT
    y = rect.y
    if v_align == 1:  # Center vertical alignment
        y = rect.y + (rect.height - total_height) // 2
    elif v_align == 2:  # Bottom vertical alignment
        y = rect.y + (rect.height - total_height)

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect()
        if h_align == 0:  # Left horizontal alignment
            text_rect.topleft = (rect.x, y + i * LINE_HEIGHT)
        elif h_align == 1:  # Center horizontal alignment
            text_rect.midtop = (rect.x + rect.width // 2, y + i * LINE_HEIGHT)
        else:  # Right horizontal alignment
            text_rect.topright = (rect.x + rect.width, y + i * LINE_HEIGHT)
        screen.blit(text_surface, text_rect.topleft)

def start_screen():
    screen.blit(background, (0, 0))
    draw_text("Quiz Game", pygame.Rect(0, 0, SCREEN_WIDTH, 100), h_align=1, v_align=1)
    draw_text("Start", pygame.Rect(0, SCREEN_HEIGHT // 2 - 10, SCREEN_WIDTH, 50), h_align=1, v_align=1)
    pygame.display.flip()

def quiz_screen(question):
    screen.blit(background, (0, 0))
    max_width = SCREEN_WIDTH - 400
    draw_text(question["question"], pygame.Rect(50, 50, SCREEN_WIDTH - 250, 150), max_width=max_width, h_align=1)
    for idx, option in enumerate(question["options"]):
        draw_text(option, pygame.Rect(135, 150 + idx * 50, SCREEN_WIDTH - 150, 150), max_width=max_width, h_align=0)
    pygame.display.flip()

def wrong_answer_screen():
    screen.blit(background, (0, 0))
    draw_text("Wrong Answer", pygame.Rect(0, SCREEN_HEIGHT // 2 - 25, SCREEN_WIDTH, 50), h_align=1, v_align=1)
    pygame.display.flip()
    pygame.time.wait(1000)

def main():
    global current_question
    running = True
    in_start_screen = True
    in_quiz_screen = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if in_start_screen:
                    start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 50)
                    if start_rect.collidepoint(mouse_pos):
                        in_start_screen = False
                        in_quiz_screen = True
                        current_question = 0
                        quiz_screen(questions[current_question])
                elif in_quiz_screen:
                    for idx, option in enumerate(questions[current_question]["options"]):
                        option_rect = pygame.Rect(135, 150 + idx * 50, SCREEN_WIDTH - 150, 50)  # Adjusted height to 50
                        if option_rect.collidepoint(mouse_pos):
                            if option == questions[current_question]["answer"]:
                                current_question += 1
                                if current_question >= len(questions):
                                    in_start_screen = True
                                    in_quiz_screen = False
                                    start_screen()
                                else:
                                    quiz_screen(questions[current_question])
                            else:
                                wrong_answer_screen()
                                quiz_screen(questions[current_question])
        
        if in_start_screen:
            start_screen()
        
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
