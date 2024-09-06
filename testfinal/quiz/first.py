import pygame
import sys
import os

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT_SIZE = 32

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
    {"question": "Which article of the Constitution guarantees equality before the law?", "options": ["A) Article 12", "B) Article 14", "C) Article 16", "D) Article 17"], "answer": "B) Article 14"},
    {"question": "The abolition of untouchability is mentioned in which article?", "options": ["A) Article 15", "B) Article 16", "C) Article 17", "D) Article 18"], "answer": "C) Article 17"},
    {"question": "Which article prohibits discrimination on grounds of religion, race, caste, sex, or place of birth?", "options": ["A) Article 14", "B) Article 15", "C) Article 16", "D) Article 18"], "answer": "B) Article 15"},
    {"question": "Article 16 guarantees equality of opportunity in matters of _____", "options": ["A) Education", "B) Public employment", "C) Freedom of speech", "D) Property"], "answer": "B) Public employment"},
    {"question": "Which article abolishes titles, except military and academic distinctions?", "options": ["A) Article 14", "B) Article 15", "C) Article 18", "D) Article 17"], "answer": "C) Article 18"},
    {"question": "Equality before law falls under which part of the Constitution?", "options": ["A) Part III", "B) Part IV", "C) Part V", "D) Part II"], "answer": "A) Part III"},
    {"question": "Article 15(3) allows special provisions for which of the following?", "options": ["A) Scheduled Castes", "B) Scheduled Tribes", "C) Women and children", "D) All citizens"], "answer": "C) Women and children"},
    {"question": "Which article provides for the abolition of titles in India?", "options": ["A) Article 16", "B) Article 18", "C) Article 15", "D) Article 14"], "answer": "B) Article 18"},
    {"question": "Reservation in public employment is provided under which article?", "options": ["A) Article 14", "B) Article 15", "C) Article 16(4)", "D) Article 18"], "answer": "C) Article 16(4)"},
    {"question": "Under which article can no citizen be discriminated against in the matter of employment?", "options": ["A) Article 17", "B) Article 14", "C) Article 16", "D) Article 18"], "answer": "C) Article 16"}
]

current_question = 0

def draw_text(text, pos, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, pos)

def start_screen():
    screen.blit(background, (0, 0))
    draw_text("Quiz Game", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
    draw_text("Start", (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
    pygame.display.flip()

def quiz_screen(question):
    screen.blit(background, (0, 0))
    draw_text(question["question"], (50, 50))
    for idx, option in enumerate(question["options"]):
        draw_text(option, (50, 150 + idx * 50))
    pygame.display.flip()

def wrong_answer_screen():
    screen.blit(background, (0, 0))
    draw_text("Wrong Answer", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
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
                        option_rect = pygame.Rect(50, 150 + idx * 50, 200, 40)
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
