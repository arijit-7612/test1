import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
FONT_SIZE = 20
SCROLL_SPEED = 10

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Scrollable Text with Close Button')
background=pygame.image.load("back3.jpg")
background=pygame.transform.scale(background,(600,700))
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Set up fonts
font = pygame.font.Font("times_new.ttf", FONT_SIZE)

# Text to display
text_lines = [
    "Article 14 of the Indian Constitution states:",
    "‘The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.’",
    "",
    "1. Equality Before the Law: This means that every individual, regardless of their status, is entitled to be treated equally under the law.",
    "There should be no arbitrary discrimination by the state or its agencies against any individual or group.",
    "It emphasizes that all persons are subject to the same laws and are entitled to the same legal protection.",
    "",
    "2. Equal Protection of the Laws: This means that laws should apply equally to all individuals in similar circumstances.",
    "It requires that the law does not discriminate or treat individuals or groups differently without a valid, reasonable, and justifiable reason.",
    "It ensures that similar cases are treated similarly.",
    "",
    "Article 15 of the Indian Constitution states:",
    "‘State shall not discriminate against any citizen on grounds only of religion, race, caste, sex or place of birth.’",
    "",
    "1. Prohibition of Discrimination (Article 15(1)):",
    "The State cannot discriminate against any citizen solely on the basis of religion, race, caste, sex, or place of birth.",
    "This guarantees that no individual should face unfair treatment or exclusion due to these characteristics.",
    "",
    "2. Access to Public Places (Article 15(2)):",
    "Citizens are guaranteed equal access to public places such as shops, public restaurants, hotels, and places of public entertainment.",
    "Additionally, it ensures non-discrimination in the use of public utilities like wells, tanks, bathing ghats, roads, and other places maintained by the State or dedicated for general public use.",
    "",
    "3. Special Provisions for Women and Children (Article 15(3)):",
    "The State is permitted to make special provisions aimed at the welfare and advancement of women and children.",
    "This allows for targeted measures to address their specific needs and support their development.",
    "",
    "4. Affirmative Action for Backward Classes (Article 15(4)):",
    "The State can implement measures for the advancement of socially and educationally backward classes of citizens, including Scheduled Castes (SCs) and Scheduled Tribes (STs).",
    "This includes provisions like reservations in educational institutions and government jobs to help these groups overcome historical disadvantages and achieve social and economic equity.",
    "",
    "Article 21 of the Indian Constitution states:",
    "‘No person shall be deprived of his life or personal liberty except according to procedure established by law.’",
    "",
    "1. Right to Life:",
    "This fundamental right guarantees that every individual has the inherent right to live, which includes not just survival but living with dignity.",
    "It encompasses various aspects necessary for a dignified life, such as health, shelter, and a decent standard of living.",
    "",
    "2. Right to Personal Liberty:",
    "This right protects individuals from arbitrary arrest or detention.",
    "It ensures that personal freedom is not restricted without due legal process, requiring that any limitations on personal liberty follow fair and established legal procedures.",
    "",
    "3. Procedure Established by Law:",
    "Any deprivation of life or personal liberty must occur through a procedure that is legally established and conforms to principles of justice and fairness.",
    "This means the process must be clearly defined by law and adhere to the principles of natural justice.",
]

def render_text(text_lines, max_width):
    lines = []
    for line in text_lines:
        words = line.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + word + ' '
            test_surface = font.render(test_line, True, BLACK)
            if test_surface.get_width() > max_width:
                lines.append(current_line)
                current_line = word + ' '
            else:
                current_line = test_line
        lines.append(current_line)
    return lines

# Render text
text_lines_wrapped = render_text(text_lines, SCREEN_WIDTH - 40)

# Button
button_rect = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT)
button_color = GRAY

def draw_text_lines(scroll_y):
    y_offset = -scroll_y + 5
    for line in text_lines_wrapped:
        text_surface = font.render(line, True, BLACK)
        if y_offset > SCREEN_HEIGHT - BUTTON_HEIGHT - 20:
            break
        screen.blit(text_surface, (20, y_offset))
        y_offset += text_surface.get_height() + 2

scroll_y = 0

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            if event.button == 4:  # Scroll up
                scroll_y = max(scroll_y - SCROLL_SPEED, 0)
            elif event.button == 5:  # Scroll down
                max_scroll_y = max(0, len(text_lines_wrapped) * FONT_SIZE - (SCREEN_HEIGHT - BUTTON_HEIGHT))
                scroll_y = min(scroll_y + SCROLL_SPEED, max_scroll_y)

    # Clear screen
    screen.blit(background,(0,0))

    # Draw text and button
    draw_text_lines(scroll_y)
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render('Close', True, BLACK)
    screen.blit(button_text, (button_rect.x + BUTTON_WIDTH // 2 - button_text.get_width() // 2, button_rect.y + BUTTON_HEIGHT // 2 - button_text.get_height() // 2))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)



