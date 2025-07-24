import pygame
import chicken_cross
import asyncio
import requests

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

# Button and input properties
button_width = 200
button_height = 60
play_button_x = (WIDTH - button_width) // 2
play_button_y = HEIGHT // 2 + 150
input_box_width = 300
input_box_height = 40
username_box_x = (WIDTH - input_box_width) // 2
username_box_y = HEIGHT // 2 - 100
password_box_x = (WIDTH - input_box_width) // 2
password_box_y = HEIGHT // 2 - 40
bet_box_x = (WIDTH - input_box_width) // 2
bet_box_y = HEIGHT // 2 + 20
background = pygame.image.load("road.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Login state
username = ""
password = ""
token = None
active_input = "username"  # Track which input field is active
bet_amount = 0  # To store the bet amount

# API Function
def login(username, password):
    global token
    response = requests.post("http://localhost:5000/auth/login", json={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json().get("jwt")
        return True
    return False

# Login Screen
def show_login_screen():
    global username, password, token, active_input, bet_amount
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if login(username, password):
                        return True
                elif event.key == pygame.K_BACKSPACE:
                    if active_input == "username" and username:
                        username = username[:-1]
                    elif active_input == "password" and password:
                        password = password[:-1]
                    elif active_input == "bet" and bet_amount > 0:
                        bet_amount //= 10
                elif event.key == pygame.K_TAB:
                    active_input = "password" if active_input == "username" else "bet" if active_input == "password" else "username"
                elif event.unicode.isdigit() and active_input == "bet":
                    bet_amount = bet_amount * 10 + int(event.unicode)
                elif event.unicode.isprintable():
                    if active_input == "username":
                        username += event.unicode
                    elif active_input == "password":
                        password += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (username_box_x <= mouse_pos[0] <= username_box_x + input_box_width and
                    username_box_y <= mouse_pos[1] <= username_box_y + input_box_height):
                    active_input = "username"
                elif (password_box_x <= mouse_pos[0] <= password_box_x + input_box_width and
                      password_box_y <= mouse_pos[1] <= password_box_y + input_box_height):
                    active_input = "password"
                elif (bet_box_x <= mouse_pos[0] <= bet_box_x + input_box_width and
                      bet_box_y <= mouse_pos[1] <= bet_box_y + input_box_height):
                    active_input = "bet"

        # Render screen
        screen.blit(background, (0, 0))
        # Draw title
        title_text = title_font.render("Chicken Cross Road", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Draw username input box with highlight if active
        username_color = GREEN if active_input == "username" else WHITE
        pygame.draw.rect(screen, username_color, (username_box_x, username_box_y, input_box_width, input_box_height), 2)
        username_text = font.render(f"Username: {username}", True, WHITE)
        screen.blit(username_text, (username_box_x + 5, username_box_y + 5))

        # Draw password input box with highlight if active
        password_color = GREEN if active_input == "password" else WHITE
        pygame.draw.rect(screen, password_color, (password_box_x, password_box_y, input_box_width, input_box_height), 2)
        password_text = font.render(f"Password: {'*' * len(password)}", True, WHITE)
        screen.blit(password_text, (password_box_x + 5, password_box_y + 5))

        # Draw bet input box with highlight if active
        bet_color = GREEN if active_input == "bet" else WHITE
        pygame.draw.rect(screen, bet_color, (bet_box_x, bet_box_y, input_box_width, input_box_height), 2)
        bet_text = font.render(f"Bet Amount: {bet_amount}", True, WHITE)
        screen.blit(bet_text, (bet_box_x + 5, bet_box_y + 5))

        # Draw Login button
        pygame.draw.rect(screen, WHITE, (play_button_x, play_button_y, button_width, button_height))
        play_text = font.render("Login", True, BLACK)
        screen.blit(play_text, (play_button_x + button_width // 2 - play_text.get_width() // 2, play_button_y + button_height // 2 - play_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

# Save bet amount to score.txt
def save_bet(bet_amount):
    with open("score.txt", "w") as file:
        file.write(str(bet_amount))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Show login screen first
    if show_login_screen():
        print(f"Login Successful! Starting Game with Bet Amount: {bet_amount}")
        save_bet(bet_amount)  # Save bet amount to score.txt
        asyncio.run(chicken_cross.main())  # Pass token and bet_amount if needed
        running = False
    else:
        running = False

# Quit Pygame
pygame.quit()