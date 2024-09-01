import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Courtroom Drama")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock for frame rate
clock = pygame.time.Clock()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frame_width, frame_height, num_frames, animation_speed, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.animation_speed = animation_speed
        self.frames = self.load_frames()
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def load_frames(self):
        frames = []
        for i in range(self.num_frames):
            frame = self.sprite_sheet.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height))
            frames.append(frame)
        return frames

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.image = self.frames[self.current_frame]

class CourtroomBackground(Sprite):
    def __init__(self, image_path):
        super().__init__(image_path, 0, 0)

class Lawyer(AnimatedSprite):
    pass

class Citizen(Sprite):
    pass

class Judge(Sprite):
    pass

# Load images
background = CourtroomBackground("background.png")
lawyer1 = Lawyer("lawyer1_spritesheet.png", 64, 64, 4, 150, 100, 400)
lawyer2 = Lawyer("lawyer2_spritesheet.png", 64, 64, 4, 150, 600, 400)
citizen1 = Citizen("citizen1.png", 150, 300)
citizen2 = Citizen("citizen2.png", 550, 300)
judge = Judge("judge.png", 350, 100)

# Group for updating all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(lawyer1)
all_sprites.add(lawyer2)
all_sprites.add(citizen1)
all_sprites.add(citizen2)
all_sprites.add(judge)

def display_question(question, options):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(question, True, BLACK)
    screen.blit(text_surface, (100, 100))

    for i, option in enumerate(options):
        option_surface = font.render(f"{i + 1}. {option}", True, BLACK)
        screen.blit(option_surface, (100, 150 + i * 40))

    pygame.display.flip()

def get_user_input():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2]:
                return event.key - pygame.K_1 + 1
    return None

def main():
    pygame.time.delay(10000)
    running = True
    clock = pygame.time.Clock()

    # Define question and options
    question = "Which lawyer should win the case?"
    options = ["Lawyer 1", "Lawyer 2"]
    correct_answer = 1  # Example answer, Lawyer 1 wins

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update all sprites
        all_sprites.update()

        # Draw everything
        screen.fill(WHITE)
        screen.blit(background.image, background.rect)
        all_sprites.draw(screen)

        # Display the judgment question and get input
        display_question(question, options)
        answer = get_user_input()
        
        if answer is not None:
            if answer == correct_answer:
                print("Lawyer 1 wins!")
            else:
                print("Lawyer 2 wins!")
            # Exit after decision
            running = False

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
