import pygame
import sys
import subprocess
from moviepy.editor import VideoFileClip
import numpy as np
import pygame.surfarray as surfarray

def show_menu(height, width):
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
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.blit(rotated_image, (0, 0))
        text.draw_text('Learning Constitution of INDIA', text.heading_font, (255, 255, 255), screen, width // 2, 170)
        margin = 20
        x_start = ((width - (box_width + margin) * 3) // 2) + 20
        y_start = 250
        for i, image in enumerate(rights_images):
            x = x_start + (i % 3) * (box_width + margin)
            y = y_start + (i // 3) * (box_height + margin)
            image = create_rounded_image(image, 30)
            screen.blit(image, (x, y))

        pygame.display.update()

    pygame.quit()

def show_preamble(height, width):
    screen = pygame.display.set_mode((width, height))
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

                popup_rect = popup_surface.get_rect(center=(rect.x + 300, rect.y - 140))
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
            run = False  # Exit the preamble loop

    
    show_menu(height, width)  # Call the menu function after quitting the preamble

pygame.init()

width, height = 1350, 750
show_preamble(height, width)

