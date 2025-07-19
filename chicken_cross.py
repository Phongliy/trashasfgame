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
all_Lane=34
voice_files = ["una.mp3", "yaha.mp3"]  # Add more voice files as needed

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
move_speed = 15  # Speed of movement
passed = 0
check = 0

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Cross Road")
clock = pygame.time.Clock()

# Load images
street_img = pygame.image.load("street.png").convert()
street_img = pygame.transform.scale(street_img, (WIDTH * 5.8, HEIGHT))  # Match total street width
down = pygame.image.load("down.png").convert()
down = pygame.transform.scale(down, (LANE_WIDTH, HEIGHT))  # Match total street width
usagi = pygame.image.load("maincharacter.png").convert_alpha()  # Use convert_alpha for transparency
usagi = pygame.transform.scale(usagi, (200, 180))
star = pygame.image.load("star.png").convert_alpha()  # Use convert_alpha for transparency
star = pygame.transform.scale(star, (200, 180))
obstacle_img = pygame.image.load("momonga.png").convert_alpha()  # Placeholder for obstacle image
obstacle_img = pygame.transform.scale(obstacle_img, (100, 100))  # Adjust size as needed

# Chicken
chicken_x = WIDTH // 2  # Start on sidewalk
chicken_y = HEIGHT
target_x = chicken_x  # Target position for smooth movement
current_lane = 0  # 0 = sidewalk, 1-5 = street lanes
lane_x = 0
targetlane_x = 0

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
    {"x": lane * LANE_WIDTH + LANE_WIDTH // 2 - 50, "y": HEIGHT - 150, "lane": lane, "speed_y": 0} for lane in range(1, 34)
]

def play_random_voices():
    if voice_files:  # Ensure there are voice files
        selected_voices = random.sample(voice_files, min(1, len(voice_files)))  # Pick 2 random voices
        for voice in selected_voices:
            sound = pygame.mixer.Sound(voice)
            sound.play()

def generate_question():
    a = random.randint(1, 1)
    b = random.randint(1, 1)
    return f"{a} + {b} = ?", a + b

def setup():
    global chicken_x, chicken_y, current_lane, car_x, car_y, math_question, math_answer, user_input, score, time_left, game_over, target_x, passed, lane_x, targetlane_x, check
    chicken_x = LANE_WIDTH // 2
    chicken_y = HEIGHT // 2
    passed = 0
    lane_x = 0
    current_lane = 0  # Start on sidewalk
    car_x = WIDTH
    car_y = HEIGHT - 150
    math_question, math_answer = generate_question()
    user_input = ""
    score = 0
    time_left = TIME_LIMIT
    game_over = False
    target_x = chicken_x  # Reset target position
    # Randomize obstacle positions and speeds
    for obs in obstacles:
        obs["x"] = obs["lane"] * LANE_WIDTH + LANE_WIDTH // 2 - 50  # Center in lane
        obs["y"] = HEIGHT - 150
        obs["speed_y"] = random.uniform(-4, 4)  # Increased speed range

def update_loop():
    global chicken_x, chicken_y, current_lane, car_x, car_y, math_question, math_answer, user_input, score, time_left, game_over, other_lane, target_x, passed, lane_x, targetlane_x, check,tickk

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
                    if passed >= 2:
                        target_x -= LANE_WIDTH
                        check = 1
                    else:
                        target_x += LANE_WIDTH
                    play_random_voices()  # Play random voices after correct answer
                    current_lane += 1
                    score += 10
                    passed += 1
                    if passed >= 3:
                        targetlane_x -= LANE_WIDTH
                    math_question, math_answer = generate_question()
                    user_input = ""
                    # Reset obstacles when passing a lane
                    for obs in obstacles:
                        if other_lane == 1:
                            if obs["lane"] == passed - 1:  # Reset obstacle for the lane just passed
                                obs["y"] = HEIGHT - 150
                                obs["speed_y"] = random.uniform(-4, 4)  # Randomize direction and speed
                        else:
                            if obs["lane"] == 5 - passed + 1:  # Reset obstacle for the lane just passed
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
        if passed >= 3 and abs(chicken_x - target_x) <= 20 and check == 1:
            target_x += LANE_WIDTH
            check = 0
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

    # Cycle obstacle from lane 1 to lane 5 with repositioning behind map
    tickk=0
    for obs in obstacles[:]:  # Use a copy to modify list during iteration
        if(passed>=3 and tickk<=passed-3):
            tickk+=1
            continue
        if obs["lane"] == 1 and (obs["x"] + lane_x < -100):  # Check if out of screen left
            obs["lane"] = 5  # Move to lane 5
            obs["x"] = 4 * LANE_WIDTH + LANE_WIDTH // 2 - 50 + WIDTH * 5  # Reposition behind map (far right)
            obs["y"] = HEIGHT - 150  # Reset y position
            obs["speed_y"] = random.uniform(-4, 4)  # Randomize speed

    if abs(lane_x - targetlane_x) > move_speed:
        lane_x += move_speed if lane_x < targetlane_x else -move_speed

    # Draw
    # Background
    screen.blit(street_img, (lane_x, 0))

    # Draw lanes
    screen.blit(usagi, (chicken_x - 75, chicken_y - 90))  # Chicken (adjusted for center)
    font = pygame.font.Font(None, 36)
    question_text = font.render(math_question, True, WHITE)
    input_text = font.render(user_input, True, WHITE)
    time_text = font.render(f"Time: {int(time_left)}s", True, WHITE)
    screen.blit(question_text, (10, 10))
    screen.blit(input_text, (10, 50))
    screen.blit(time_text, (WIDTH - 150, 10))

    # Draw obstacles
    for obs in obstacles:
        if(passed>=3 and tickk<=3-passed):
            tickk+=1
            continue
        draw_x = obs["x"] + lane_x  # Adjust x position with lane_x for drawing
        if other_lane == 1:
            if obs["lane"] != current_lane:  # Do not draw obstacle in current lane
                screen.blit(obstacle_img, (draw_x, obs["y"]))
        else:
            if obs["lane"] != 5 - current_lane:  # Do not draw obstacle in current lane
                screen.blit(obstacle_img, (draw_x, obs["y"]))

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