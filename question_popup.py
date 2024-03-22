import pygame
import config

class QuestionPopup:
    def __init__(self, screen, question):
        self.message_color = pygame.Color(config.GREEN_MINT)
        self.screen = screen
        self.font = pygame.font.Font(config.FONT, 20)
        self.question = question
        self.answer = None
        self.correct_answer = question["correct_answer"]
        self.answer_rects = []  # Rects for each answer variant
        self.is_correct = None  # Track if the answer is correct or incorrect
        self.points_awarded = 0
        self.margin = 30  # Margin for wrapping text

    def wrap_text(self, text, max_width):
        # Split text into words
        words = text.split()

        # Initialize wrapped lines
        wrapped_lines = []
        current_line = ""

        # Iterate through words
        for word in words:
            # Check if adding the word exceeds the max width
            if self.font.size(current_line + word)[0] < max_width - 2 * self.margin:
                # Add word to the current line
                current_line += word + " "
            else:
                # Add current line to wrapped lines
                wrapped_lines.append(current_line)
                # Start a new line with the current word
                current_line = word + " "

        # Add the last line
        if current_line:
            wrapped_lines.append(current_line)

        return wrapped_lines

    def show(self):
        # Clear the screen with white
        self.screen.fill(config.WHITE)

        tip = self.font.render("Klikšķini uz pareizās atbildes", True, self.message_color)
        tip_rect = tip.get_rect(center=(400, 550))
        self.screen.blit(tip, tip_rect)

        # Wrap question text
        wrapped_question = self.wrap_text(self.question["question"], 740)  # Adjust the max width as needed

        # Render the wrapped question text
        y_position = 200
        for line in wrapped_question:
            question_text = self.font.render(line, True, (0, 0, 0))
            question_rect = question_text.get_rect(center=(400, y_position))
            self.screen.blit(question_text, question_rect)
            y_position += self.font.get_linesize()

        # Render the answer variants
        answer_y = 250
        for index, answer_variant in enumerate(self.question["answers"]):
            wrapped_answer_variant = self.wrap_text(answer_variant, 800)
            for line in wrapped_answer_variant:
                answer_text = self.font.render(line, True, (0, 0, 0))
                answer_rect = answer_text.get_rect(center=(400, answer_y))
                self.screen.blit(answer_text, answer_rect)
                answer_y += 40  # Adjust vertical position for the next line  # Adjust vertical position for the next answer variant

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
