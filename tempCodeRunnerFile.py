import asyncio
import platform
import pygame
import random
import question  # Assuming question.py is in the same directory

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
BLACK = (0, 0, 0)
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
# Randomize obstacle image from 3 options (placeholders)
obstacle_images = [
    pygame.image.load("car1.png").convert_alpha(),  # Placeholder link 1
    pygame.image.load("car2.png").convert_alpha(),  # Placeholder link 2
    pygame.image.load("car3.png").convert_alpha()   # Placeholder link 3
]
for img in obstacle_images:
    img = pygame.transform.scale(img, (50, 50))  # Adjust size as needed

# Item image (placeholder)
item_img = pygame.image.load("item.png").convert_alpha()  # Replace with your item image
item_img = pygame.transform.scale(item_img, (100, 100))  # Set size to 100x100

# Load custom font
try:
    font = pygame.font.Font("DejaVuSans.ttf", 24)  # Reduced from 36 to 24
    stop_font = pygame.font.Font("DejaVuSans.ttf", 20)  # Reduced from 30 to 20
    congrats_font = pygame.font.Font("DejaVuSans.ttf", 50)  # Reduced from 74 to 50
except FileNotFoundError:
    print("Warning: DejaVuSans.ttf not found. Using default font.")
    font = pygame.font.Font(None, 24)  # Fallback to default font
    stop_font = pygame.font.Font(None, 20)
    congrats_font = pygame.font.Font(None, 50)

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
paused = False
multiplier = 1.1  # Initial multiplier for score calculation

# Obstacles
obstacles = [
    {"x": lane * LANE_WIDTH + LANE_WIDTH // 2 - 50, "y": HEIGHT - 150, "lane": lane, "speed_y": random.uniform(2, 6), "image_idx": random.randint(0, 2)} for lane in range(1, 34)
]

# Items (multiple, similar to obstacles, fixed y at HEIGHT // 2)
items = [
    {"x": lane * LANE_WIDTH + LANE_WIDTH // 2 - 70, "y": HEIGHT // 2, "lane": lane, "speed_y": 0} for lane in range(1, 34)
]

# Multipliers (similar to items, for display, fixed values per lane)
multipliers = [
    {"x": lane * LANE_WIDTH + LANE_WIDTH // 2 - 70, "y": HEIGHT // 2, "lane": lane, "speed_y": 0, "value": round(1.1 ** (lane - 1), 2)} for lane in range(1, 34)
]

q_asked = []
question_gen = question.question_generator()

def play_random_voices():
    if voice_files:  # Ensure there are voice files
        selected_voices = random.sample(voice_files, min(1, len(voice_files)))  # Pick 2 random voices
        for voice in selected_voices:
            sound = pygame.mixer.Sound(voice)
            sound.play()

def generate_question():
    # a = random.randint(1, 1)
    # b = random.randint(1, 1)
    # return f"{a} + {b} = ?", a + b

    q_key, is_correct = question.main()
    # while q_key in q_asked:
    #      q_key, is_correct = question.main()
    q_asked.append(q_key)
    # # Check if the answer is correct
    return q_key, is_correct
    # try:
    #     key, answer = next(question_gen)
    #     q_asked.append(key)
    #     return key, answer
    # except StopIteration:
    #     print("No more questions!")
    #     return None, None, None, None

    
    

def setup():
    global chicken_x, chicken_y, current_lane, car_x, car_y, math_question, math_answer, user_input, score, time_left, game_over, target_x, passed, lane_x, targetlane_x, check, paused, obstacles, items, multipliers, multiplier
    chicken_x = LANE_WIDTH // 2
    chicken_y = HEIGHT // 2
    passed = 0
    lane_x = 0
    current_lane = 0  # Start on sidewalk
    target_x=0
    targetlane_x = 0  # Reset target lane position
    # Reset car position
    car_x = WIDTH
    car_y = HEIGHT - 150
    # math_question, math_answer = generate_question()
    user_input = ""
    score = 0
    time_left = TIME_LIMIT
    game_over = False
    paused = False
    target_x = chicken_x  # Reset target position
    multiplier = 1.1  # Reset multiplier
    # Randomize obstacle positions and speeds
    for obs in obstacles:
        obs["x"] = obs["lane"] * LANE_WIDTH + LANE_WIDTH // 2 - 100  # Center in lane
        obs["y"] = HEIGHT - 150
        obs["speed_y"] = random.uniform(2, 6)  # Positive speed for upward movement
        obs["image_idx"] = random.randint(0, 2)  # Randomize image index
    # Initialize item positions and reset
    for item in items:
        item["x"] = item["lane"] * LANE_WIDTH + LANE_WIDTH // 2 - 70  # Center in lane
        item["y"] = HEIGHT // 2  # Fixed y position
        item["speed_y"] = 0  # No vertical movement
    # Initialize multiplier positions and values (fixed per lane)
    for m in multipliers:
        m["x"] = m["lane"] * LANE_WIDTH + LANE_WIDTH // 2 - 70  # Center in lane
        m["y"] = HEIGHT // 2  # Fixed y position
        m["speed_y"] = 0  # No vertical movement

def update_loop():
    global chicken_x, chicken_y, current_lane, car_x, car_y, math_question, math_answer, user_input, score, time_left, game_over, other_lane, target_x, passed, lane_x, targetlane_x, check, tickk, paused, obstacles, items, multipliers, multiplier

    if game_over or paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 10 > mouse_pos[0] > 0 and HEIGHT // 20 > mouse_pos[1] > 0 and paused:  # Resume button
                    paused = False
                elif WIDTH//2-WIDTH//20 < mouse_pos[0] < WIDTH//2+WIDTH//20 and HEIGHT // 2+100 < mouse_pos[1] < HEIGHT // 2+100+HEIGHT//15 and (paused or game_over):  # Play Again button
                    setup()
        if paused:
            congrats_text = congrats_font.render(f"Chúc mừng bạn đã dừng lại với số điểm {score:.1f}", True, BLACK)
            congrats_box_width = congrats_text.get_width() + 40  # Reduced padding from 60 to 40
            congrats_box_height = congrats_text.get_height() + 20  # Reduced padding from 40 to 20
            congrats_box_x = (WIDTH // 2 - congrats_box_width // 2)
            congrats_box_y = HEIGHT // 2 - congrats_box_height // 2
            congrats_box_rect = pygame.Rect(congrats_box_x, congrats_box_y, congrats_box_width, congrats_box_height)
            pygame.draw.rect(screen, (255, 255, 255), congrats_box_rect)  # White background
            pygame.draw.rect(screen, BLACK, congrats_box_rect, 2)        # Black border
            screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, congrats_box_y + 10))  # Adjusted y offset
            pygame.display.flip()
            return True
        if game_over:
            game_over_text = congrats_font.render("Mất hết rồi :(((", True, BLACK)
            game_over_box_width = game_over_text.get_width() + 40  # Reduced padding from 60 to 40
            game_over_box_height = game_over_text.get_height() + 20  # Reduced padding from 40 to 20
            game_over_box_x = (WIDTH // 2 - game_over_box_width // 2)
            game_over_box_y = HEIGHT // 2 - game_over_box_height // 2
            game_over_box_rect = pygame.Rect(game_over_box_x, game_over_box_y, game_over_box_width, game_over_box_height)
            pygame.draw.rect(screen, (255, 255, 255), game_over_box_rect)  # White background
            pygame.draw.rect(screen, BLACK, game_over_box_rect, 2)        # Black border
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, game_over_box_y + 10))  # Adjusted y offset
            pygame.display.flip()
            return True

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                key, is_correct = generate_question()
                print(q_asked)
                if is_correct:
                    if passed >= 2:
                        target_x -= (LANE_WIDTH)
                        check = 1
                    else:
                        target_x += (LANE_WIDTH-20)
                    play_random_voices()  # Play random voices after correct answer
                    current_lane += 1
                    score += 10 * multiplier  # Apply multiplier to score
                    passed += 1
                    if passed >= 3:
                        targetlane_x -= LANE_WIDTH
                    # Update multiplier based on current lane
                    multiplier = round(1.1 ** (current_lane), 2)  # Update multiplier dynamically
                    # math_question, math_answer = generate_question()
                    # user_input = ""
                    
                    # Reset obstacles when passing a lane
                    for obs in obstacles:
                        if other_lane == 1:
                            if obs["lane"] == passed - 1:  # Reset obstacle for the lane just passed
                                obs["y"] = HEIGHT - 150
                                obs["speed_y"] = random.uniform(2, 6)
                                obs["image_idx"] = random.randint(0, 2)
                        else:
                            if obs["lane"] == 5 - passed + 1:  # Reset obstacle for the lane just passed
                                obs["y"] = HEIGHT - 150
                                obs["speed_y"] = random.uniform(2, 6)
                                obs["image_idx"] = random.randint(0, 2)
                else:
                    game_over = True
            elif event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                user_input += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
        if event.type == pygame.MOUSEBUTTONDOWN and not (game_over or paused):
            mouse_pos = pygame.mouse.get_pos()
            if WIDTH // 10 > mouse_pos[0] > 0 and HEIGHT // 20 > mouse_pos[1] > 0:  # Stop button area
                paused = True

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

    # Move obstacles upward
    for obs in obstacles:
        obs["y"] -= obs["speed_y"]  # Move upward (negative y direction)
        if obs["y"] < -100:  # When obstacle moves off the top
            obs["y"] = HEIGHT  # Reset to initial position (bottom)
            obs["speed_y"] = random.uniform(2, 6)  # Randomize positive speed again
            obs["image_idx"] = random.randint(0, 2)

    # Cycle obstacle from lane 1 to lane 5 with repositioning behind map
    tickk=0
    for obs in obstacles[:]:  # Use a copy to modify list during iteration
        if(passed>=3 and tickk<=passed-3):
            tickk+=1
            continue
        if obs["lane"] == 1 and (obs["x"] + lane_x < -500):  # Check if out of screen left
            obs["lane"] = 5  # Move to lane 5
            obs["x"] = 4 * LANE_WIDTH + LANE_WIDTH // 2 - 50 + WIDTH * 5  # Reposition behind map (far right)
            obs["y"] = HEIGHT   # Reset y position
            obs["speed_y"] = random.uniform(2, 6)  # Randomize speed
            obs["image_idx"] = random.randint(0, 2)

    # Move items (similar to obstacles, fixed y)
    for item in items[:]:
        if item["lane"] == 1 and (item["x"] + lane_x < -100):  # Check if out of screen left
            item["lane"] = 5  # Move to lane 5
            item["x"] = 4 * LANE_WIDTH + LANE_WIDTH // 2 - 70 + WIDTH * 5  # Reposition behind map (far right)
            item["y"] = HEIGHT // 2  # Fixed y position
            item["x"] += move_speed if lane_x < targetlane_x else -move_speed  # Move with lane

    # Move multipliers (similar to items)
    for m in multipliers[:]:
        if m["lane"] == 1 and (m["x"] + lane_x < -100):  # Check if out of screen left
            m["lane"] = 5  # Move to lane 5
            m["x"] = 4 * LANE_WIDTH + LANE_WIDTH // 2 - 70 + WIDTH * 5  # Reposition behind map (far right)
            m["y"] = HEIGHT // 2  # Fixed y position
            m["x"] += move_speed if lane_x < targetlane_x else -move_speed  # Move with lane

    if abs(lane_x - targetlane_x) > move_speed:
        lane_x += move_speed if lane_x < targetlane_x else -move_speed

    # Draw
    # Background
    screen.blit(street_img, (lane_x, 0))

    # Draw items
    for item in items:
        draw_x = item["x"] + lane_x  # Adjust x position with lane_x for drawing
        screen.blit(item_img, (draw_x, item["y"]))

    # Draw multipliers
    for m in multipliers:
        draw_x = m["x"] + lane_x  # Adjust x position with lane_x for drawing
        multiplier_text = font.render(f"x{round(m['value'], 2)}", True, BLACK)
        text_rect = multiplier_text.get_rect(center=(draw_x + 50, m["y"] + 50))
        screen.blit(multiplier_text, text_rect)

    # Draw obstacles
    for obs in obstacles:
        if(passed>=3 and tickk<=3-passed):
            tickk+=1
            continue
        draw_x = obs["x"] + lane_x  # Adjust x position with lane_x for drawing
        if other_lane == 1:
            if obs["lane"] != current_lane:  # Do not draw obstacle in current lane
                screen.blit(obstacle_images[obs["image_idx"]], (draw_x, obs["y"]))
        else:
            if obs["lane"] != 5 - current_lane:  # Do not draw obstacle in current lane
                screen.blit(obstacle_images[obs["image_idx"]], (draw_x, obs["y"]))

    # Draw lanes
    screen.blit(usagi, (chicken_x - 75, chicken_y - 90))  # Chicken (adjusted for center)
    question_text = font.render(math_question, True, WHITE)
    input_text = font.render(user_input, True, WHITE)
    time_text = font.render(f"Time: {int(time_left)}s", True, WHITE)
    score_text = font.render(f"Score: {score:.1f}", True, WHITE)  # Display score with 1 decimal place

    # Time box
    time_render = font.render(f"Time: {int(time_left)}s", True, BLACK)
    time_box_width = time_render.get_width() + 40  # Reduced padding from 60 to 40
    time_box_height = time_render.get_height() + 20  # Reduced padding from 40 to 20
    time_box_x = (WIDTH - time_box_width - 20)  # Position near top-right
    time_box_y = 10
    time_box_rect = pygame.Rect(time_box_x, time_box_y, time_box_width, time_box_height)
    pygame.draw.rect(screen, (255, 255, 255), time_box_rect)  # White background
    pygame.draw.rect(screen, BLACK, time_box_rect, 2)        # Black border
    screen.blit(time_render, (time_box_x + 20, time_box_y + 10))  # Adjusted offset

    # Score box
    score_render = font.render(f"Score: {score:.1f}", True, BLACK)
    score_box_width = score_render.get_width() + 40  # Reduced padding from 60 to 40
    score_box_height = score_render.get_height() + 20  # Reduced padding from 40 to 20
    score_box_x = (WIDTH - score_box_width - 20)  # Position near top-right, below time
    score_box_y = 40  # Adjusted to avoid overlap
    score_box_rect = pygame.Rect(score_box_x, score_box_y+50 ,score_box_width, score_box_height)
    pygame.draw.rect(screen, (255, 255, 255), score_box_rect)  # White background
    pygame.draw.rect(screen, BLACK, score_box_rect, 2)        # Black border
    screen.blit(score_render, (score_box_x + 20, score_box_y + 10+50))  # Adjusted offset

    # Draw input text
    screen.blit(input_text, (10, 50))

    # Draw stop button
    stop_button_rect = pygame.Rect(0, 0, WIDTH // 10, HEIGHT // 20)
    pygame.draw.rect(screen, WHITE, stop_button_rect)  # White button
    pygame.draw.rect(screen, BLACK, stop_button_rect, 2)  # Black border
    stop_text = stop_font.render("Point Out", True, BLACK)
    screen.blit(stop_text, (WIDTH // 20 - stop_text.get_width() // 2, HEIGHT // 40 - stop_text.get_height() // 2))

    # Draw play again button (only when paused or game_over)
    if paused or game_over:
        play_again_button_rect = pygame.Rect(WIDTH//2-WIDTH//20, HEIGHT // 2+100, WIDTH // 10, HEIGHT // 15)
        pygame.draw.rect(screen, WHITE, play_again_button_rect)  # White button
        pygame.draw.rect(screen, BLACK, play_again_button_rect, 2)  # Black border
        play_again_text = stop_font.render("Play Again", True, BLACK)
        screen.blit(play_again_text, (WIDTH//2-WIDTH//20+25, HEIGHT // 2+115))

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