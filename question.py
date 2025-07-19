import pygame
import random

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
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Game")
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 36)
tick_font = pygame.font.Font(None, 40)  # Font for tick mark

# Question and answer setup
questions = [
    ("Cây nào sống ở vùng ngập mặn?", ["CÂY CẶC BẦN(bần chua)", "Cây Xoài", "Cây Dừa", "Cây mít"], "CÂY CẶC BẦN(bần chua)"),
    ("Con gì đi bằng 3 chân?", ["Người ngoài hành tinh", "Chó cụt chân", "Gà công nghiệp", "Cụ già với gậy"], "Cụ già với gậy"),
    ("Thức ăn nào làm bạn khóc?", ["Không có gì ăn", "ớt", "Khoai tây", "Cơm khổ khoa"], "Không có gì ăn"),
    ("Cha của bé sol là ai", ["Trình Trần Phường Tuần", "Hiếu thứ hai", "j69", "Trịnh Trần Phương Tuấn"], "Trịnh Trần Phương Tuấn"),
    ("Tại sao con gà lai qua đường?", ["Vì nó thích", "Để qua phía bên kia", "Ước mở thuở nhỏ", "Để mưu sinh"], "Để qua phía bên kia"),
    ("LGBT là viết tắt của gì?", ["Lesbian Gay Bisexual Transgender", "Lấy Gió Bằng Turbo", "Lẩu Gà Bình Thuận", "Lắm Gái Bán Tình"], "Lesbian Gay Bisexual Transgender"),
    ("Game nào hay nhất Roblox?", ["Blox fruit", "Grow a garden", "Liên Blox Mobile", "Free fire"], "Blox fruit"),
    ("Trong Liên Quân vị tướng nào thấp nhất?", ["Aya", "Zip", "Nakroth", "Florentino"], "Zip"),
    ("Cái gì người nghèo có mà người giàu không có?", ["Tiền", "Hạnh Phúc", "Không Có Gì", "Gia Đình"], "Không Có Gì"),
    ("Sắp xếp các từ sau theo đúng thứ tự c/l/ọ/n/ồ", ["lộn cò", "cộn lò", "cọn lồ", "lọ cồn"], "lọ cồn")
]

current_question = 0
selected_answer = None
correct_count = 0  # Đếm số câu trả lời đúng

# Game loop
running = True
while running and current_question < len(questions):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, (_, rect) in enumerate(option_rects):
                if rect.collidepoint(mouse_pos):
                    selected_answer = options[i]
                    if selected_answer == correct_answer:
                        correct_count += 1  # Tăng số câu đúng nếu chọn đúng
                    current_question += 1
                    selected_answer = None
                    break

    # Draw background
    screen.fill(WHITE)

    # Draw question
    if current_question < len(questions):
        question_text = questions[current_question][0]
        options = questions[current_question][1]
        correct_answer = questions[current_question][2]

        question_render = font.render(question_text, True, BLACK)
        screen.blit(question_render, (WIDTH // 2 - question_render.get_width() // 2, 100))

        # Draw option buttons at four corners
        option_rects = []
        corner_positions = [
            (WIDTH//2-400, HEIGHT//2+120),  # Top-left
            (WIDTH//2+100, HEIGHT//2+120),  # Top-right
            (WIDTH//2-400, HEIGHT//2-120),  # Bottom-left
            (WIDTH//2+100, HEIGHT//2-120)   # Bottom-right
        ]
        for i, option in enumerate(options[:4]):  # Use only 4 options
            button_text = font.render(str(option), True, BLACK)
            button_width = max(400, button_text.get_width() + 40)  # Adjust width to fit text, minimum 400
            button_height = 120
            button_x, button_y = corner_positions[i]
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, GREEN if selected_answer == option else BLACK, button_rect, 2)
            screen.blit(button_text, (button_x + 20, button_y + (button_height - button_text.get_height()) // 2))
            
            # Draw tick mark if correct answer is selected
            if selected_answer == correct_answer and selected_answer == option:
                tick_render = tick_font.render("✓", True, GREEN)
                screen.blit(tick_render, (button_x + button_width - 40, button_y + (button_height - tick_render.get_height()) // 2))

            option_rects.append((option, button_rect))

        # Draw result if selected
        if selected_answer is not None:
            result_text = font.render(f"Result: {'Correct' if selected_answer == correct_answer else 'Wrong'}", True, GREEN if selected_answer == correct_answer else RED)
            screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 600))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Final result
print(f"Final result: {correct_count}/{len(questions)}")  # Print total correct answers
pygame.quit()