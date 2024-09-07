import pygame
import sys
import subprocess
from moviepy.editor import VideoFileClip
import numpy as np
import pygame.surfarray as surfarray
import time
import requests
import json


def sprite(height,width):
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
    frames2 = load_frames(sprite_sheetld, 64, 64, 15, 2.8)
    frames3 = load_frames(sprite_sheetl, 64, 64, 13, 2.8)






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
                fundr_menu(height, width)
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    current_dialogue_index = (current_dialogue_index + 1)  
                    if current_dialogue_index == 6 and not popup_displayed:
                        show_popup()
                        popup_displayed = True
                if event.key==pygame.K_LEFT:
                    current_dialogue_index = (current_dialogue_index - 1)  
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
        if current_dialogue_index==21:
            summary(height,width)
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
    
def summary(height,width):
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

    return    
    


def fundr_menu(height, width):
    box_width, box_height = 325, 150
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Learning Constitution')
    background_image = pygame.image.load("cont.jpeg")
    rotated_image = pygame.transform.rotate(background_image, 90)
    rotated_image = pygame.transform.scale(rotated_image, (width, height))
    rights_images = [pygame.image.load(f'right{i}.jpg') for i in range(1, 7)]
    for i in range(6):
        rights_images[i] = pygame.transform.scale(rights_images[i], (box_width, box_height))

    def create_rounded_image(image, radius):
        rect = image.get_rect()
        rounded_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(rounded_surface, (255, 255, 255), rect, border_radius=radius)
        mask = pygame.mask.from_surface(rounded_surface)
        for x in range(rect.width):
            for y in range(rect.height):
                if not mask.get_at((x, y)):
                    image.set_at((x, y), (0, 0, 0, 0))
        rounded_surface.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return rounded_surface

    class Text:
        def __init__(self, font):
            self.font = font
            self.heading_font = pygame.font.Font(self.font, 65)

        def draw_text(self, text, font, color, surface, x, y):
            self.textobj = font.render(text, True, color)
            self.textrect = self.textobj.get_rect()
            self.textrect.center = (x, y)
            surface.blit(self.textobj, self.textrect)

    text = Text('times_new.ttf')
    run = True
    
    # Create a list to store the rectangular areas for each icon
    icon_rects = []
    margin = 20
    x_start = ((width - (box_width + margin) * 3) // 2) + 20
    y_start = 250

    for i in range(6):
        x = x_start + (i % 3) * (box_width + margin)
        y = y_start + (i // 3) * (box_height + margin)
        image = create_rounded_image(rights_images[i], 30)
        icon_rects.append(pygame.Rect(x, y, box_width, box_height))
        
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for index, rect in enumerate(icon_rects):
                    if rect.collidepoint(mouse_pos):
                        if index == 0:  # Check if the clicked icon is the first one
                            sprite(height, width)
        
        screen.blit(rotated_image, (0, 0))
        text.draw_text('Learning Constitution of INDIA', text.heading_font, (255, 255, 255), screen, width // 2, 170)
        
        for i, rect in enumerate(icon_rects):
            screen.blit(create_rounded_image(rights_images[i], 30), rect.topleft)

        pygame.display.update()

    pygame.quit()

def show_preamble(height, width):
    
    pygame.display.set_caption('Preamble Typewriter Effect')

    background_image = pygame.image.load("cont.jpeg")
    rotated_image = pygame.transform.rotate(background_image, 90)
    rotated_image = pygame.transform.scale(rotated_image, (width, height))

    font = pygame.font.Font("times_new.ttf", 21)
    popup_font = pygame.font.Font("times_new.ttf", 16)

    preamble_lines = [
        "PREAMBLE",
        "We, THE PEOPLE OF INDIA, having solemnly resolved to constitute",
        "India into a SOVEREIGN SOCIALIST SECULAR DEMOCRATIC",
        "REPUBLIC and to secure to all its citizens:",
        "JUSTICE, Social, Economic and Political;",
        "LIBERTY of thought, expression, belief, faith and worship;",
        "EQUALITY of status and of opportunity; and to promote among them all;",
        "FRATERNITY assuring the dignity of the individual and the unity and integrity of the Nation;",
        "IN OUR CONSTITUENT ASSEMBLY this twenty-sixth day of",
        "November, 1949, do HEREBY ADOPT, ENACT AND GIVE TO",
        "OURSELVES THIS CONSTITUTION."
    ]

    displayed_lines = [""] * len(preamble_lines)
    line_index = 0
    char_index = 0
    delay = 35
    last_update = pygame.time.get_ticks()

    line_height = font.get_linesize() * 1.7
    skip = False
    next_button = False

    skip_button_text = font.render("Skip", True, (150, 75, 0))
    skip_button_rect = skip_button_text.get_rect(bottomright=(width - 150, height - 130))

    popup_texts = {
        "SOVEREIGN": "sov.jpg",
        "REPUBLIC": "republic.jpg",
        "SOCIALIST": "SOCIALIST.jpg",
        "SECULAR": "Secular.jpg",
        "DEMOCRATIC": "democratic.jpg",
        "JUSTICE, Social, Economic and Political;": "JUSTICE.jpg",
        "LIBERTY": "LIBERTY.jpg",
        "EQUALITY": "equality.jpg",
        "FRATERNITY": "FRATERNITY.jpg",
        "CONSTITUENT ASSEMBLY": "IN OUR CONSTITUENT ASSEMBLY.jpg",
        "HEREBY ADOPT, ENACT AND GIVE TO": "LAST PHRASE.jpg",
    }

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if skip_button_rect.collidepoint(event.pos):
                    if not skip:
                        skip = True
                        skip_button_text = font.render("Next", True, (150, 75, 0))
                    else:
                        next_button = True

        current_time = pygame.time.get_ticks()
        if not skip:
            if current_time - last_update > delay:
                if line_index < len(preamble_lines):
                    if char_index < len(preamble_lines[line_index]):
                        displayed_lines[line_index] += preamble_lines[line_index][char_index]
                        char_index += 1
                    else:
                        line_index += 1
                        char_index = 0
                    last_update = current_time
        else:
            displayed_lines = preamble_lines[:]

        screen.blit(rotated_image, (0, 0))

        word_rects = []
        y_offset = 175
        for i, line in enumerate(displayed_lines):
            words = line.split()
            text_surface = font.render(line, True, (245, 245, 220))
            text_rect = text_surface.get_rect(center=(width // 2, y_offset + i * line_height))
            screen.blit(text_surface, text_rect.topleft)

            start_x = text_rect.left
            for word in words:
                word_surface = font.render(word, True, (245, 245, 220))
                word_rect = word_surface.get_rect(topleft=(start_x, text_rect.top))
                word_rects.append((word, word_rect))
                start_x += word_surface.get_width() + 5

            for phrase, popup in popup_texts.items():
                if phrase in line:
                    phrase_surface = font.render(phrase, True, (245, 245, 220))
                    phrase_start = line.find(phrase)
                    phrase_end = phrase_start + len(phrase)
                    phrase_rect = pygame.Rect(text_rect.left + font.size(line[:phrase_start])[0],
                                              text_rect.top,
                                              font.size(phrase)[0],
                                              text_rect.height)
                    word_rects.append((phrase, phrase_rect))

        mouse_pos = pygame.mouse.get_pos()

        for word, rect in word_rects:
            if rect.collidepoint(mouse_pos) and word in popup_texts:
                if popup_texts[word].endswith(".jpg") or popup_texts[word].endswith(".png"):
                    popup_image = pygame.image.load(popup_texts[word])
                    popup_image = pygame.transform.scale(popup_image, (450, 250))
                    popup_surface = pygame.Surface((450, 250))
                    popup_surface.blit(popup_image, (0, 0))
                else:
                    popup_surface = pygame.Surface((300, 100))
                    popup_surface.fill((50, 50, 50))
                    popup_text = popup_font.render(popup_texts[word], True, (255, 255, 255))
                    popup_text_rect = popup_text.get_rect(center=popup_surface.get_rect().center)
                    popup_surface.blit(popup_text, popup_text_rect.topleft)

                popup_rect = popup_surface.get_rect(center=(rect.x + 300, rect.y - 125))
                screen.blit(popup_surface, popup_rect.topleft)

                pygame.draw.rect(screen, (255, 0, 0), rect, 2)

        pygame.draw.rect(screen, (245, 245, 220), skip_button_rect.inflate(10, 10))
        screen.blit(skip_button_text, skip_button_rect.topleft)

        pygame.display.update()

        if line_index >= len(preamble_lines) and char_index == 0:
            skip = True
            skip_button_text = font.render("Next", True, (150, 75, 0))
            screen.blit(skip_button_text, skip_button_rect.topleft)

        if next_button:
            pygame.time.delay(50)
            menu1(height,width)
            run = False  # Exit the preamble loop
    pygame.quit()
    

def menu1(height,width):
    IMAGE_SIZE = (250, 150)
    HEADING_FONT_SIZE = 72
    HEADING_COLOR = (139, 69, 19)

    file_paths = [show_preamble, "comingsoon.jpg",fundr_menu, "comingsoon.jpg"]
    image_paths = ["preamble.jpg", "PRINCIPLES.jpg", "RIGHTS.jpg", "DUTIES.jpg"]

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MENU')

    # Load images
    background_image = pygame.image.load("background.jpeg").convert()
    background_image = pygame.transform.scale(background_image, (width, height))
    loaded_images = [pygame.transform.scale(pygame.image.load(img), IMAGE_SIZE) for img in image_paths]

# Load font
    heading_font = pygame.font.Font("times_new.ttf", HEADING_FONT_SIZE)
    heading_surface = heading_font.render("MENU", True, HEADING_COLOR)
    heading_rect = heading_surface.get_rect(center=(width // 2, HEADING_FONT_SIZE // 2 + 110))

    def draw_menu():

    
        x_start = (width - 2 * IMAGE_SIZE[0]) //3  +90
        y_start = height // 3 

        for i, img in enumerate(loaded_images):
            row = i // 2
            col = i % 2
        
            x_pos = x_start + col * (IMAGE_SIZE[0] + x_start-270)  
            y_pos = y_start + row * (IMAGE_SIZE[1] + 50) 
            screen.blit(img, (x_pos, y_pos))

    

# Main loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                x_start = (width - 2 * IMAGE_SIZE[0]) //3  +90
                y_start = height // 3 

                for i, img in enumerate(loaded_images):
                    row = i // 2
                    col = i % 2
        
                    x_pos = x_start + col * (IMAGE_SIZE[0] + x_start-270)  
                    y_pos = y_start + row * (IMAGE_SIZE[1] + 50)
                    rect=pygame.Rect(x_pos,y_pos,IMAGE_SIZE[0],IMAGE_SIZE[1])
                    if (rect).collidepoint(mousepos):
                        file_paths[i](height,width)
                    


        screen.blit(background_image, (0, 0))
        screen.blit(heading_surface, heading_rect.topleft)
        draw_menu()
        pygame.display.flip()






pygame.init()

API_KEY = '6e42b5ece252438c89ae74eb71162319'
ENDPOINT = 'https://api.cognitive.microsofttranslator.com/'
LOCATION = 'southeastasia'


width, height = 1350, 750
screen = pygame.display.set_mode((width, height))

WIDTH, HEIGHT = 1350, 750
FONT_SIZE = 48
TEXT_SPEED = 0.4

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Intro')
font = pygame.font.Font(None, FONT_SIZE)

def draw_text(text, x, y):

    screen.fill((0, 0, 0))  # Fill the screen with black
    current_text = ""
    
    for char in text:
        current_text += char
        rendered_text = font.render(current_text, True, (255, 255, 255))  # Render text
        screen.blit(rendered_text, (x, y))  # Draw text on the screen
        pygame.display.flip()  # Update the display
        time.sleep(TEXT_SPEED)  # Wait for a short period

intro_text = "BINEXE"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_text(intro_text, WIDTH // 2 - font.size(intro_text)[0] // 2, HEIGHT // 2 - font.size(intro_text)[1] // 2)
    pygame.time.wait(int(len(intro_text) * TEXT_SPEED * 250) )
    running = False  # Exit after displaying the text
menu1(height, width)