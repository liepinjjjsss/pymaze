import pygame

class QuestionPopup:
    def __init__(self, screen, question):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.question = question
        self.answer = None
        self.correct_answer = question["correct_answer"]
        self.answer_rects = []  # Rects for each answer variant
        self.is_correct = None  # Track if the answer is correct or incorrect
        self.points_awarded = 0

    def show(self):
        # Clear the screen with white
        self.screen.fill((255, 255, 255))

        # Render the question text
        question_text = self.font.render(self.question["question"], True, (0, 0, 0))
        question_rect = question_text.get_rect(center=(400, 200))
        self.screen.blit(question_text, question_rect)

        # Render the answer variants
        answer_y = 250
        for index, answer_variant in enumerate(self.question["answers"]):
            answer_text = self.font.render(answer_variant, True, (0, 0, 0))
            answer_rect = answer_text.get_rect(center=(400, answer_y))
            self.screen.blit(answer_text, answer_rect)
            self.answer_rects.append(answer_rect)
            answer_y += 40  # Adjust vertical position for the next answer variant

        # Render feedback text based on the answer state
        if self.is_correct is not None:
            # Determine feedback color and fill the entire screen with it
            feedback_color = (0, 255, 0) if self.is_correct else (255, 0, 0)
            self.screen.fill(feedback_color)

            # Render feedback text
            feedback_text = self.font.render("Correct!" if self.is_correct else "Incorrect!", True, (255, 255, 255))
            feedback_rect = feedback_text.get_rect(center=(400, 380))
            self.screen.blit(feedback_text, feedback_rect)

            points_text = self.font.render(f"Points awarded: {self.points_awarded}", True, (0, 0, 0))
            points_rect = points_text.get_rect(center=(400, 400))
            self.screen.blit(points_text, points_rect)

        pygame.display.flip()

    def check_answer(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for index, answer_rect in enumerate(self.answer_rects):
                    if answer_rect.collidepoint(mouse_pos):
                        return chr(ord('a') + index)  # Convert index to corresponding letter ('a', 'b', 'c', 'd')

        return None  # Return None if no answer option was clicked

    # Return None if no answer option was clicked

    def set_answer_state(self, is_correct):
        self.is_correct = is_correct  # Set the answer state (correct or incorrect)
        if is_correct:
            self.points_awarded += 1000
            return self.points_awarded
