import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
POPUP_WIDTH, POPUP_HEIGHT = 500, SCREEN_HEIGHT  # Reduced width of the pop-up
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
FONT_SIZE = 23  # Increased font size
LINE_SPACING = 8  # Adjust line spacing
MARGIN = 20  # Margin for both sides of the text

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Landing Page with Scrollable Pop-up")

# Load the background image for the popup and the main screen
main_background_image = pygame.image.load("back3.jpg")
main_background_image = pygame.transform.scale(main_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

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

# Function to render multiline text with wrapping and scrolling
def render_multiline_text(surface, text, x, y, font, color, max_width):
    words = text.split()  # Split the paragraph by spaces (words)
    space_width, _ = font.size(' ')
    line = []
    line_width = 0
    y_offset = y

    for word in words:
        word_surface = font.render(word, True, color)
        word_width, word_height = word_surface.get_size()

        # If adding the word exceeds max width, render the line and start a new one
        if line_width + word_width > max_width:
            surface.blit(font.render(' '.join(line), True, color), (x, y_offset))
            line = [word]
            line_width = word_width + space_width
            y_offset += word_height + LINE_SPACING
        else:
            line.append(word)
            line_width += word_width + space_width

    # Render the last line
    if line:
        surface.blit(font.render(' '.join(line), True, color), (x, y_offset))

    return y_offset + word_height  # Return the final Y position for scrolling

# Function to display pop-up with scrolling
def show_popup():
    scroll_offset = 0  # This will keep track of how far we've scrolled
    max_scroll = 0  # Max scroll limit to prevent overscrolling

    # Close button setup
    close_button = Button("Close", POPUP_WIDTH // 2 - 50, POPUP_HEIGHT - 70, 100, 50, BLUE, BLACK)

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

    # Main loop to handle the scrollable pop-up
    while True:
        screen.blit(main_background_image, (0, 0))  # Blit background first
        
        # Draw the eligibility text with the current scroll offset
        text_bottom = render_multiline_text(screen, eligibility_text, MARGIN, MARGIN - scroll_offset, font, BLACK, POPUP_WIDTH - 2 * MARGIN)

        # Draw the close button
        close_button.draw(screen)
        
        # Update max_scroll based on the total text height
        max_scroll = max(0, text_bottom - POPUP_HEIGHT + 100)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.is_clicked(event):
                    return  # Close the pop-up and return to the main screen
            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y * 20  # Scroll by 20 pixels per wheel tick
                scroll_offset = max(0, min(scroll_offset, max_scroll))  # Ensure we don't scroll out of bounds

        pygame.display.update()

# Main loop for landing page
def main():
    running = True
    while running:
        screen.blit(main_background_image, (0, 0))  # Display the main screen background

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
