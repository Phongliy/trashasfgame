import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 1540
HEIGHT = 774
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Cross Road - Menu")
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

# Button properties
button_width = 200
button_height = 60
play_button_x = (WIDTH - button_width) // 2
play_button_y = HEIGHT // 2 - 50
instructions_button_x = (WIDTH - button_width) // 2
instructions_button_y = HEIGHT // 2 + 50

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check Play button
            if (play_button_x <= mouse_pos[0] <= play_button_x + button_width and
                play_button_y <= mouse_pos[1] <= play_button_y + button_height):
                print("Game Started!")  # Placeholder for starting the game
                running = False  # Exit to start game

    background = pygame.image.load("road.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    # Draw title

    # Draw Play button
    pygame.draw.rect(screen,BLACK , (play_button_x, play_button_y-30, button_width, button_height))
    play_text = font.render("Play", True, WHITE)
    screen.blit(play_text, (play_button_x + button_width // 2 - play_text.get_width() // 2, play_button_y + button_height // 2 - play_text.get_height() // 2-30))

    # Draw Instructions button

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()