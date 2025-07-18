import asyncio
import platform
import pygame
import random

# Initialize Pygame
pygame.init()
 
# Constants
WIDTH = 1540
HEIGHT = 774
FPS = 60
LANE_COUNT = 6
LANE_WIDTH = WIDTH // (LANE_COUNT)  # Adjusted for sidewalk + 5 lanes
TIME_LIMIT = 60  # 1 minute in seconds
other_lane = 1
voice_files = ["una.mp3", "yaha.mp3"]  # Add more voice files as needed

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
move_speed = 15  # Speed of movement
passed = 0
scroll_offset = 0  # For infinite scroll
bg_switched = False  # Track if we have switched to street2 permanently

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Cross Road")
clock = pygame.time.Clock()

# Load images
street_img = pygame.image.load("street.png").convert()
street_img = pygame.transform.scale(street_img, (WIDTH, HEIGHT))  # Match total street width
street2_img = pygame.image.load("street2.png").convert()
street2_img = pygame.transform.scale(street2_img, (WIDTH, HEIGHT))  # Match total street width
down = pygame.image.load("down.png").convert()
down = pygame.transform.scale(down, (LANE_WIDTH, HEIGHT))  # Match total street width
usagi = pygame.image.load("maincharacter.png").convert_alpha()  # Use convert_alpha for transparency
usagi = pygame.transform.scale(usagi, (200, 180))
# star = pygame.image.load("star.png").convert_alpha()  # Use convert_alpha for transparency
# star = pygame.transform.scale(star, (200, 180))
obstacle_img = pygame.image.load("momonga.png").convert_alpha()  # Placeholder for obstacle image
obstacle_img = pygame.transform.scale(obstacle_img, (100, 100))  # Adjust size as needed

# Chicken
chicken_x = WIDTH // 2  # Start on sidewalk
chicken_y = HEIGHT
target_x = chicken_x  # Target position for smooth movement
current_lane = 0  # 0 = sidewalk, 1-5 = street lanes

# Car
car_x = WIDTH
car_y = HEIGHT - 150
car_speed = 5

# Game state
score = 0
math_question = ""
math_answer = 0
user_input = ""
time_left = TIME_LIMIT
game_over = False

# Obstacles
obstacles = [
    {"x": 0, "y": HEIGHT - 150, "lane": 1, "speed_y": 0},  # One obstacle per lane
    {"x": 0, "y": HEIGHT - 150, "lane": 2, "speed_y": 0},
    {"x": 0, "y": HEIGHT - 150, "lane": 3, "speed_y": 0},
    {"x": 0, "y": HEIGHT - 150, "lane": 4, "speed_y": 0}
]

def play_random_voices():
    if voice_files:  # Ensure there are voice files
        selected_voices = random.sample(voice_files, min(1, len(voice_files)))  # Pick 1 random voice
        for voice in selected_voices:
            sound = pygame.mixer.Sound(voice)
            sound.play()

def generate_question():
    a = random.randint(1, 1)
    b = random.randint(1, 1)
    return f"{a} + {b} = ?", a + b

def setup():
    global chicken_x, chicken_y, current_lane, car_x, car_y, math_question, math_answer, user_input, score, time_left, game_over, target_x, passed, scroll_offset, bg_switched
    chicken_x = LANE_WIDTH // 2
    chicken_y = HEIGHT // 2
    passed = 0
    scroll_offset = 0 # reset scroll offset
    current_lane = 0  # Start on sidewalk
    car_x = WIDTH
    car_y = HEIGHT - 150
    math_question, math_answer = generate_question()
    user_input = ""
    score = 0
    time_left = TIME_LIMIT
    game_over = False
    target_x = chicken_x  # Reset target position
    bg_switched = False
    # Randomize obstacle positions and speeds
    for obs in obstacles:
        obs["lane"] = obs["lane"]  # Fixed to one obstacle per lane
        obs["x"] = obs["lane"] * LANE_WIDTH + LANE_WIDTH // 2 - 50  # Center in lane
        obs["y"] = HEIGHT - 150
        obs["speed_y"] = random.uniform(-4, 4)  # Increased speed range

def reset_for_scroll():
    global chicken_x, chicken_y, current_lane, target_x, obstacles
    chicken_x = LANE_WIDTH // 2
    chicken_y = HEIGHT // 2
    current_lane = 0
    target_x = chicken_x
    # Reset obstacles to new positions for the new section
    for obs in obstacles:
        obs["x"] = obs["lane"] * LANE_WIDTH + LANE_WIDTH // 2 - 50
        obs["y"] = HEIGHT - 150
        obs["speed_y"] = random.uniform(-4, 4)

def update_loop():
    global chicken_x, chicken_y, current_lane, car_x, car_y, math_question, math_answer, user_input, score, time_left, game_over, other_lane, target_x, passed, scroll_offset, bg_switched

    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                setup()
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over! Press R to Restart", True, WHITE)
        screen.blit(text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()
        return True

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if user_input.isdigit() and int(user_input) == math_answer:
                    if other_lane == 1:
                        target_x += LANE_WIDTH
                    else:
                        target_x -= LANE_WIDTH
                    play_random_voices()  # Play random voices after correct answer
                    current_lane += 1
                    score += 10
                    passed += 1
                    math_question, math_answer = generate_question()
                    user_input = ""
                    # Reset obstacles when passing a lane
                    for obs in obstacles:
                        if other_lane == 1:
                            if obs["lane"] == current_lane - 1:  # Reset obstacle for the lane just passed
                                obs["y"] = HEIGHT - 150
                                obs["speed_y"] = random.uniform(-4, 4)  # Randomize direction and speed
                        else:
                            if obs["lane"] == 5 - current_lane + 1:  # Reset obstacle for the lane just passed
                                obs["y"] = HEIGHT - 150
                                obs["speed_y"] = random.uniform(-4, 4)  # Randomize direction and speed
                else:
                    game_over = True
            elif event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                user_input += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
    if abs(chicken_x - target_x) > move_speed:
        chicken_x += move_speed if chicken_x < target_x else -move_speed
    # Update time
    time_left -= 1 / FPS
    if time_left <= 0:
        game_over = True

    # Move car
    car_x -= car_speed
    if car_x < -50:
        car_x = WIDTH

    # Move obstacles up and down
    for obs in obstacles:
        obs["y"] += obs["speed_y"]
        if obs["y"] < 100 or obs["y"] > HEIGHT - 150:  # Keep within screen bounds
            obs["speed_y"] *= -1  # Reverse direction when hitting bounds

    # Infinite scroll effect: after 4 lanes, shift everything and reset
    if passed >= 6:
        scroll_offset += WIDTH  # Move background by one screen width
        passed = 0
        reset_for_scroll()
        bg_switched = True  # After first scroll, always use street2_img

    # Draw
    # Background
    if current_lane == 7:
        other_lane *= -1
        current_lane = 0

    # Gradually blend street_img and street2_img based on scroll progress
    scroll_progress = (scroll_offset % WIDTH) / WIDTH  # 0.0 to 1.0

    if not bg_switched and scroll_progress > 0:
        # Blend from street_img to street2_img during the first scroll
        blended_bg = pygame.Surface((WIDTH, HEIGHT)).convert()
        street_img_alpha = max(0, 255 - int(scroll_progress * 255))
        street2_img_alpha = min(255, int(scroll_progress * 255))
        temp_street = street_img.copy()
        temp_street2 = street2_img.copy()
        temp_street.set_alpha(street_img_alpha)
        temp_street2.set_alpha(street2_img_alpha)
        blended_bg.blit(temp_street, (0, 0))
        blended_bg.blit(temp_street2, (0, 0))
        screen.blit(blended_bg, (0, 0))
    elif not bg_switched:
        # Before first scroll, show street_img
        screen.blit(street_img, (0, 0))
    else:
        # After first scroll, always show street2_img
        screen.blit(street2_img, (0, 0))
    
    # Draw lanes with scroll offset
    for i in range(1, 8):
        lane_x = (LANE_WIDTH * i + 5) - (scroll_offset % WIDTH)
        screen.blit(down, (lane_x, 0))

    # Draw chicken and star with scroll offset
    screen.blit(usagi, (chicken_x - 75, chicken_y - 90))
    # if other_lane == 1:
    #     screen.blit(star, (WIDTH - LANE_WIDTH - (scroll_offset % WIDTH), HEIGHT // 2 - 50))
    # else:
    #     screen.blit(star, (LANE_WIDTH // 2 - 50 - (scroll_offset % WIDTH), HEIGHT // 2 - 50))
    font = pygame.font.Font(None, 36)
    question_text = font.render(math_question, True, WHITE)
    input_text = font.render(user_input, True, WHITE)
    time_text = font.render(f"Time: {int(time_left)}s", True, WHITE)
    screen.blit(question_text, (10, 10))
    screen.blit(input_text, (10, 50))
    screen.blit(time_text, (WIDTH - 150, 10))

    # Draw obstacles with scroll offset
    for obs in obstacles:
        if other_lane == 1:
            if obs["lane"] != current_lane:  # Do not draw obstacle in current lane
                screen.blit(obstacle_img, (obs["x"] - (scroll_offset % WIDTH), obs["y"]))
        else:
            if obs["lane"] != 5 - current_lane:  # Do not draw obstacle in current lane
                screen.blit(obstacle_img, (obs["x"] - (scroll_offset % WIDTH), obs["y"]))

    pygame.display.flip()
    return True

async def main():
    setup()
    while True:
        if not update_loop():
            break
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())