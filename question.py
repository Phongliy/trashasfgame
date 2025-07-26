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
    0: ("Mật khẩu nào sau đây được xem là an toàn nhất?", ["123456", "password", "Anhyeuem123", "Jk#3vL9!xZ"], "Jk#3vL9!xZ"),
1: ("Khi nhận được email từ người lạ kèm liên kết đáng ngờ, bạn nên làm gì?", ["Bấm vào thử xem là gì", "Tải tệp đính kèm", "Báo cáo là spam và xóa ngay", "Trả lời lại để hỏi thông tin"], "Báo cáo là spam và xóa ngay"),
2: ("Mã độc (malware) là gì?", ["Phần mềm giúp máy tính chạy nhanh hơn", "Phần mềm độc hại gây hại cho máy tính", "Hệ điều hành miễn phí", "Phần mềm diệt virus"], "Phần mềm độc hại gây hại cho máy tính"),
3: ("Tường lửa (firewall) có tác dụng gì?", ["Làm đẹp giao diện máy tính", "Ngăn chặn truy cập trái phép vào hệ thống", "Tăng tốc mạng Internet", "Xóa phần mềm độc hại"], "Ngăn chặn truy cập trái phép vào hệ thống"),
4: ("Ransomware là gì?", ["Phần mềm diệt virus", "Loại mã độc tống tiền", "Hệ điều hành mã nguồn mở", "Phần mềm kiểm tra RAM"], "Loại mã độc tống tiền"),
5: ("Bộ phận nào của máy tính dùng để lưu dữ liệu tạm thời khi máy đang chạy?", ["Ổ cứng (HDD)", "ROM", "RAM", "GPU"], "RAM"),
6: ("CPU còn được gọi là gì?", ["Bộ nhớ ngoài", "Bộ xử lý trung tâm", "Màn hình hiển thị", "Ổ đĩa cứng"], "Bộ xử lý trung tâm"),
7: ("Ổ cứng SSD nhanh hơn HDD vì lý do nào?", ["Có thể phát nhạc to hơn", "Không có bộ phận chuyển động cơ học", "Dung lượng lớn hơn", "Sử dụng hệ điều hành khác"], "Không có bộ phận chuyển động cơ học"),
8: ("Thiết bị nào dùng để hiển thị thông tin?", ["Chuột", "Loa", "Màn hình", "CPU"], "Màn hình"),
9: ("ROM có đặc điểm gì?", ["Ghi và xóa dữ liệu liên tục", "Lưu trữ tạm thời", "Lưu trữ lâu dài, không bị mất khi tắt máy", "Chỉ dùng trong game"], "Lưu trữ lâu dài, không bị mất khi tắt máy"),
10: ("Trí tuệ nhân tạo (AI) là gì?", ["Một loại phần mềm chat", "Khả năng máy tính mô phỏng trí tuệ con người", "Một thiết bị phần cứng đặc biệt", "Một hệ điều hành mới"], "Khả năng máy tính mô phỏng trí tuệ con người"),
11: ("Ứng dụng nào sau đây có sử dụng AI?", ["Máy tính cầm tay", "Đồng hồ báo thức", "Trợ lý ảo như Siri, Google Assistant", "Máy in"], "Trợ lý ảo như Siri, Google Assistant"),
12: ("AI được ứng dụng trong lĩnh vực nào sau đây?", ["Chỉ trong game", "Chỉ trong toán học", "Rất nhiều lĩnh vực như y tế, giáo dục, công nghiệp", "Không ứng dụng được thực tế"], "Rất nhiều lĩnh vực như y tế, giáo dục, công nghiệp"),
13: ("Một điểm cần chú ý khi sử dụng AI là gì?", ["AI luôn đúng", "AI không cần dữ liệu", "AI có thể tạo ra sai sót và thiên lệch nếu học từ dữ liệu không tốt", "AI tự động cập nhật hệ điều hành"], "AI có thể tạo ra sai sót và thiên lệch nếu học từ dữ liệu không tốt"),
14: ("ChatGPT là ví dụ của ứng dụng AI nào?", ["Trí tuệ cảm xúc", "Học máy không giám sát", "Xử lý ngôn ngữ tự nhiên", "Thị giác máy tính"], "Xử lý ngôn ngữ tự nhiên"),
15: ("AI cần gì để học và đưa ra quyết định?", ["RAM mạnh", "Dữ liệu huấn luyện", "Kết nối Wi-Fi", "Màn hình cảm ứng"], "Dữ liệu huấn luyện"),
16: ("Học sâu (Deep Learning) là một phần của lĩnh vực nào?", ["Tin học văn phòng", "Mạng máy tính", "Học máy (Machine Learning)", "Cơ sở dữ liệu"], "Học máy (Machine Learning)"),
17: ("Mạng nơ-ron nhân tạo hoạt động giống với cơ quan nào của con người?", ["Tim", "Phổi", "Não", "Dạ dày"], "Não"),
18: ("Hành vi nào dưới đây có thể dẫn đến việc AI đưa ra kết quả sai?", ["Nhập dữ liệu chính xác", "Dữ liệu thiếu đa dạng và thiên lệch", "Tăng RAM máy tính", "Dùng phần mềm diệt virus"], "Dữ liệu thiếu đa dạng và thiên lệch"),
19: ("Hệ thống AI có thể tự động học từ dữ liệu mới gọi là gì?", ["Hệ thống tĩnh", "Hệ thống mở rộng", "Hệ thống học máy", "Hệ thống mã hóa"], "Hệ thống học máy")
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