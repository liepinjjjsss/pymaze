import pygame

class QuestionPopup:
    def __init__(self, screen, question):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.question = question
        self.answer = ""
        self.correct_answer = None

    def show(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (100, 100, 600, 400))  # Draw a white rectangle
        question_text = self.font.render(self.question["question"], True, (0, 0, 0))  # Render the question text
        self.correct_answer = self.question["correct_answer"]
        self.screen.blit(question_text, (150, 150))  # Display the question text on the screen
        pygame.display.flip()

    def check_answer(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.answer = "a"
                elif event.key == pygame.K_b:
                    self.answer = "b"
                elif event.key == pygame.K_c:
                    self.answer = "c"
                elif event.key == pygame.K_d:
                    self.answer = "d"

        if self.answer:
            if self.answer == self.correct_answer:
                return True
            else:
                return False
