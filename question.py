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
font = pygame.font.Font("DejaVuSans.ttf", 36)
tick_font = pygame.font.Font("DejaVuSans.ttf", 40)

# Question and answer setup
questions = {
    0 : ("Cây nào sống ở vùng ngập mặn?", ["CÂY CẶC BẦN(bần chua)", "Cây Xoài", "Cây Dừa", "Cây mít"], "CÂY CẶC BẦN(bần chua)"),
    1 : ("Con gì đi bằng 3 chân?", ["Người ngoài hành tinh", "Chó cụt chân", "Gà công nghiệp", "Cụ già với gậy"], "Cụ già với gậy"),
    2 : ("Thức ăn nào làm bạn khóc?", ["Không có gì ăn", "ớt", "Khoai tây", "Cơm khổ khoa"], "Không có gì ăn"),
    3 : ("Cha của bé sol là ai", ["Trình Trần Phường Tuần", "Hiếu thứ hai", "j69", "Trịnh Trần Phương Tuấn"], "Trịnh Trần Phương Tuấn"),
    4 : ("Tại sao con gà lai qua đường?", ["Vì nó thích", "Để qua phía bên kia", "Ước mở thuở nhỏ", "Để mưu sinh"], "Để qua phía bên kia"),
    5 : ("LGBT là viết tắt của gì?", ["Lesbian Gay Bisexual Transgender", "Lấy Gió Bằng Turbo", "Lẩu Gà Bình Thuận", "Lắm Gái Bán Tình"], "Lesbian Gay Bisexual Transgender"),
    6 : ("Game nào hay nhất Roblox?", ["Blox fruit", "Grow a garden", "Liên Blox Mobile", "Free fire"], "Blox fruit"),
    7 : ("Trong Liên Quân vị tướng nào thấp nhất?", ["Aya", "Zip", "Nakroth", "Florentino"], "Zip"),
    8 : ("Cái gì người nghèo có mà người giàu không có?", ["Tiền", "Hạnh Phúc", "Không Có Gì", "Gia Đình"], "Không Có Gì"),
    9 : ("Sắp xếp các từ sau theo đúng thứ tự c/l/ọ/n/ồ", ["lộn cò", "cộn lò", "cọn lồ", "lọ cồn"], "lọ cồn")
}

# Global variables for question state
question_keys = list(questions.keys())
random.shuffle(question_keys)
current_question = 0
selected_answer = None
correct_count = 0

def get_next_question():
    """Get the next question without showing the UI"""
    global current_question
    
    if current_question >= len(questions):
        # Reset if we've used all questions
        current_question = 0
        random.shuffle(question_keys)
    
    q_key = question_keys[current_question]
    current_question += 1  # Move to next question for next time
    
    return q_key

def main():
    """Interactive question display (for standalone testing)"""
    global current_question, selected_answer, correct_count
    selected_answer = None
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
                        is_correct = selected_answer == correct_answer
                        if is_correct:
                            correct_count += 1
                        key_to_return = question_keys[current_question - 1]  # Get current question key
                        current_question += 1  # Move to next question
                        return key_to_return, is_correct

        # Draw background
        # screen.fill(WHITE)

        # Draw question
        if current_question < len(questions):
            question_index = current_question + 1
            total_questions = len(questions)
            number_text = font.render(f"Question {question_index}/{total_questions}", True, BLACK)
            screen.blit(number_text, (WIDTH // 2 - number_text.get_width() // 2, 50))

            q_key = question_keys[current_question]
            question_text = questions[q_key][0]
            options = questions[q_key][1]
            correct_answer = questions[q_key][2]

                        # Draw a box behind the question text
            question_render = font.render(question_text, True, BLACK)
            question_box_width = question_render.get_width() + 60
            question_box_height = question_render.get_height() + 40
            question_box_x = (WIDTH // 2 - question_box_width // 2) 
            question_box_y = 90
            question_box_rect = pygame.Rect(question_box_x, question_box_y, question_box_width, question_box_height)
            pygame.draw.rect(screen, (255, 255, 255), question_box_rect)  # Grey background
            pygame.draw.rect(screen, BLACK, question_box_rect, 2)        # Black border
            screen.blit(question_render, (WIDTH // 2 - question_render.get_width() // 2, question_box_y + 20))

        

            option_rects = []
            corner_positions = [
                (WIDTH//2-450, HEIGHT//2+120),
                (WIDTH//2+50, HEIGHT//2+120),
                (WIDTH//2-450, HEIGHT//2-120),
                (WIDTH//2+50, HEIGHT//2-120)
            ]
            for i, option in enumerate(options[:4]):
                button_text = font.render(str(option), True, BLACK)
                button_width = max(400, button_text.get_width() + 40)
                button_height = 120
                button_x, button_y = corner_positions[i]
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                pygame.draw.rect(screen, (255, 255, 255), button_rect) 
                pygame.draw.rect(screen, GREEN if selected_answer == option else BLACK, button_rect, 2)
                screen.blit(button_text, (button_x + 20, button_y + (button_height - button_text.get_height()) // 2))
                option_rects.append((option, button_rect))

        pygame.display.flip()
        clock.tick(FPS)

def question_generator():
    """Generator function that yields questions in random order"""
    keys = list(questions.keys())
    random.shuffle(keys)
    for key in keys:
        q = questions[key]
        yield key, q[2]

if __name__ == "__main__":
    key, is_correct = main()
    print(f"Key: {key}, Is Correct: {is_correct}")