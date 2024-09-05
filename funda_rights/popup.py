import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
POPUP_WIDTH, POPUP_HEIGHT = 600, SCREEN_HEIGHT  # Full vertical height, narrower horizontal width
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
BLUE = (70, 130, 180)
FONT_SIZE = 16

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Landing Page with Pop-up")

# Fonts
font = pygame.font.Font("times_new.ttf", FONT_SIZE)

# Button class for the close button inside the pop-up
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_surface = font.render(text, True, WHITE)

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

# Function to render multiline text
def render_multiline_text(surface, text, x, y, font, color, line_spacing=5):
    lines = text.splitlines()  # Split the paragraph by new lines
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * (FONT_SIZE + line_spacing)))  # Adjust the y position for each line

# Function to display pop-up
def show_popup():
    # Create the pop-up surface covering full vertical height and part of horizontal width
    popup_surface = pygame.Surface((POPUP_WIDTH, POPUP_HEIGHT))
    popup_surface.fill(GREY)
    
    # Center the pop-up horizontally
    popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
    
    # Eligibility Criteria Text
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
    
    # Render eligibility text
    render_multiline_text(popup_surface, eligibility_text, 20, 20, font, BLACK)

    # Close button
    close_button = Button("Close", POPUP_WIDTH // 2 - 50, POPUP_HEIGHT - 70, 100, 50, BLUE, BLACK)
    
    # Draw pop-up in the middle of the screen horizontally and covering full vertical height
    screen.blit(popup_surface, (popup_x, 0))
    close_button.draw(popup_surface)
    pygame.display.update()

    # Wait for pop-up events
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if close_button.is_clicked(event):
                return  # Close the pop-up and return to the main screen

# Main loop for landing page
def main():
    running = True
    while running:
        screen.fill(WHITE)
        
        # Trigger pop-up for demonstration (This can be triggered conditionally in a real application)
        show_popup()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()
    sys.exit()

# Run the main loop
if __name__ == "__main__":
    main()
