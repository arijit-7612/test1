import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
FONT_SIZE = 28
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 60
FPS = 30

# Setup screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MCQ Popup Example")
font = pygame.font.SysFont(None, FONT_SIZE)

def draw_text(text, font, color, surface, x, y, max_width=None):
    if max_width:
        words = text.split(' ')
        lines = []
        line = ''
        for word in words:
            test_line = f"{line} {word}".strip()
            test_surface = font.render(test_line, True, color)
            if max_width and test_surface.get_width() > max_width:
                lines.append(line)
                line = word
            else:
                line = test_line
        lines.append(line)
        text_height = sum(font.get_linesize() for _ in lines)
        y -= text_height // 2
        for line in lines:
            textobj = font.render(line, True, color)
            textrect = textobj.get_rect()
            textrect.midtop = (x, y)
            surface.blit(textobj, textrect)
            y += font.get_linesize()
    else:
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

def draw_button(text, font, color, surface, x, y, max_width):
    pygame.draw.rect(surface, color, pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
    draw_text(text, font, WHITE, surface, x + BUTTON_WIDTH / 2, y + BUTTON_HEIGHT / 2, max_width)

def main():
    clock = pygame.time.Clock()
    
    question = "What is the capital of France?"
    options = [
        "A. Berlin is the capital of Germany",
        "B. Madrid is the capital of Spain",
        "C. Paris is the capital of France",
        "D. Rome is the capital of Italy"
    ]
    correct_option = "C"
    
    selected_option = None
    result_message = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                if 100 <= mouse_x <= 100 + BUTTON_WIDTH:
                    if 200 <= mouse_y <= 200 + BUTTON_HEIGHT:
                        selected_option = "A"
                    elif 270 <= mouse_y <= 270 + BUTTON_HEIGHT:
                        selected_option = "B"
                    elif 340 <= mouse_y <= 340 + BUTTON_HEIGHT:
                        selected_option = "C"
                    elif 410 <= mouse_y <= 410 + BUTTON_HEIGHT:
                        selected_option = "D"
                    
                    if selected_option:
                        if selected_option == correct_option:
                            result_message = "Correct!"
                        else:
                            result_message = "Incorrect!"

        screen.fill(WHITE)

        draw_text(question, font, BLACK, screen, WINDOW_WIDTH / 2, 100)
        
        y_pos = 200
        for option in options:
            draw_button(option, font, BLUE, screen, 100, y_pos, BUTTON_WIDTH - 20)
            y_pos += BUTTON_HEIGHT + 10
        
        if result_message:
            draw_text(result_message, font, BLACK, screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
