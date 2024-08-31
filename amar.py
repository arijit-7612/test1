import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pygame Game")

# Set up colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up the player
player_size = 50
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5

# Clock to control the frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Fill the background with white
    window.fill(WHITE)

    # Draw the player (a red rectangle)
    pygame.draw.rect(window, RED, (player_pos[0], player_pos[1], player_size, player_size))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

