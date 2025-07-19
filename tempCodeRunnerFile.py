            number_text = font.render(f"Question {question_index}/{total_questions}", True, BLACK)
            screen.blit(number_text, (WIDTH // 2 - number_text.get_width() // 2, 50))