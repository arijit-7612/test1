import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
POPUP_WIDTH, POPUP_HEIGHT = 500, SCREEN_HEIGHT  # Reduced width of the pop-up
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
FONT_SIZE = 23  # Increased font size
LINE_SPACING = 8  # Adjust line spacing
MARGIN = 30  # Horizontal margin for both sides of the text
TOP_MARGIN = 75  # Additional margin at the top
BOTTOM_MARGIN = 80  # Increased margin above the close button
CLOSE_BUTTON_HEIGHT = 50  # Height of the close button

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Landing Page with Scrollable Pop-up")

# Load the background image for the popup and the main screen
main_background_image = pygame.image.load("back3.jpg")
main_background_image = pygame.transform.scale(main_background_image, (1000, 1200))

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
                pygame.exit()
        return False

# Function to render multiline text with wrapping and scrolling
def render_multiline_text(surface, text, x, y, font, color, max_width, line_spacing=5):
    words = text.split()  # Split the paragraph by spaces (words)
    space_width, _ = font.size(' ')
    line = []
    line_width = 0
    y_offset = y

    screen_height = surface.get_height()  # Get the screen height
    restricted_area_start = screen_height - 150 # Define the restricted area height limit

    for word in words:
        word_surface = font.render(word, True, color)
        word_width, word_height = word_surface.get_size()

        # If the current y_offset is beyond the restricted area, stop rendering
        if y_offset + word_height > restricted_area_start:
            break

        # If adding the word exceeds max width, render the line and start a new one
        if line_width + word_width > max_width:
            surface.blit(font.render(' '.join(line), True, color), (x, y_offset))
            line = [word]
            line_width = word_width + space_width
            y_offset += word_height + line_spacing

            # Check again if we're beyond the restricted area after moving to a new line
            if y_offset + word_height > restricted_area_start:
                break
        else:
            line.append(word)
            line_width += word_width + space_width

    # Render the last line if it doesn't cross into the restricted area
    if line and y_offset + word_height <= restricted_area_start:
        surface.blit(font.render(' '.join(line), True, color), (x, y_offset))

    return y_offset + word_height  # Return the final Y position for scrolling

# Function to display pop-up with scrolling and close button
def show_popup():
    scroll_offset = 0  # This will keep track of how far we've scrolled
    max_scroll = 0  # Max scroll limit to prevent overscrolling

    # Close button setup (position it just above the bottom of the screen)
    close_button_y = POPUP_HEIGHT - CLOSE_BUTTON_HEIGHT - BOTTOM_MARGIN
    close_button = Button("Close", POPUP_WIDTH // 2 - 50, close_button_y, 100, 50, BLUE, BLACK)

    # Eligibility Criteria Text
    eligibility_text = """
     Article 14 of the Indian Constitution states: 
 
"The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India." 
 
1. Equality Before the Law: This means that every individual, regardless of their status, is entitled to be treated equally under the law.  
There should be no arbitrary discrimination by the state or its agencies against any individual or group.  
It emphasizes that all persons are subject to the same laws and are entitled to the same legal protection. 
 
2. Equal Protection of the Laws: This means that laws should apply equally to all individuals in similar circumstances.  
It requires that the law does not discriminate or treat individuals or groups differently without a valid, reasonable, and justifiable reason. 
It ensures that similar cases are treated similarly. 
 
 
Article 15 of the Indian Constitution states: 
 
"State shall not discriminate against any citizen on grounds only of religion, race, caste, sex or place of birth." 
 
1. Prohibition of Discrimination (Article 15(1)): 
 
The State cannot discriminate against any citizen solely on the basis of religion, race, caste, sex, or place of birth.  
This guarantees that no individual should face unfair treatment or exclusion due to these characteristics. 
 
2. Access to Public Places (Article 15(2)): 
 
Citizens are guaranteed equal access to public places such as shops, public restaurants, hotels, and places of public entertainment.  
Additionally, it ensures non-discrimination in the use of public utilities like wells, tanks, bathing ghats, roads, and other places maintained by the State or dedicated for general public use. 
 
3. Special Provisions for Women and Children (Article 15(3)): 
 
The State is permitted to make special provisions aimed at the welfare and advancement of women and children. 
This allows for targeted measures to address their specific needs and support their development. 
 
4. Affirmative Action for Backward Classes (Article 15(4)): 
 
The State can implement measures for the advancement of socially and educationally backward classes of citizens, including Scheduled Castes (SCs) and Scheduled Tribes (STs).  
This includes provisions like reservations in educational institutions and government jobs to help these groups overcome historical disadvantages and achieve social and economic equity. 
 
Article 21 of the Indian Constitution states: 
 
"No person shall be deprived of his life or personal liberty except according to procedure established by law." 
 
1. Right to Life: 
 
This fundamental right guarantees that every individual has the inherent right to live, which includes not just survival but living with dignity.  
It encompasses various aspects necessary for a dignified life, such as health, shelter, and a decent standard of living. 
 
2. Right to Personal Liberty: 
 
This right protects individuals from arbitrary arrest or detention.  
It ensures that personal freedom is not restricted without due legal process, requiring that any limitations on personal liberty follow fair and established legal procedures. 
 
3. Procedure Established by Law: 
 
Any deprivation of life or personal liberty must occur through a procedure that is legally established and conforms to principles of justice and fairness. 
This means the process must be clearly defined by law and adhere to the principles of natural justice.

    
    """

    # Main loop to handle the scrollable pop-up
    # Main loop to handle the scrollable pop-up
    while True:
        screen.blit(main_background_image, (-100, -160))  # Blit background first
        
        # Calculate the maximum height the text can occupy (without overlapping the close button)
        max_text_height = close_button_y - TOP_MARGIN - BOTTOM_MARGIN

        # Draw the eligibility text with the current scroll offset
        text_bottom = render_multiline_text(screen, eligibility_text, MARGIN, TOP_MARGIN - scroll_offset, font, BLACK, POPUP_WIDTH - 2 * MARGIN)

        # Update max_scroll based on the total text height
        max_scroll = max(0, text_bottom - (TOP_MARGIN - scroll_offset + max_text_height))

        # Draw the close button
        close_button.draw(screen)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.is_clicked(event):
                    return  # Close the pop-up and return to the main screen
            elif event.type == pygame.MOUSEWHEEL:
                # Apply the scroll event by modifying scroll_offset
                scroll_offset -= event.y * 10  # Adjust scroll sensitivity here if needed

                # Ensure scroll_offset is within bounds
                scroll_offset = max(0, min(scroll_offset, max_scroll))

        pygame.display.update()


# Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.is_clicked(event):
                    return  # Close the pop-up and return to the main screen
            elif event.type == pygame.MOUSEWHEEL:
                # Apply the scroll event by modifying scroll_offset
                scroll_offset -= event.y * 10  # Scroll by 20 pixels per wheel tick

                # Ensure scroll_offset is within bounds
                scroll_offset = max(0, min(scroll_offset, max_scroll))


        
        pygame.display.update()

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

