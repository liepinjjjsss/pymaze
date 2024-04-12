import pygame
from time import sleep
import sys
import json
import random

from clock import Clock
from maze import Maze
from player import Player
from game import Game, Button
from points_of_interest import PointsOfInterest
from config import *
from question_data import *
from question_popup import QuestionPopup


pygame.init()
pygame.font.init()


def load_questions(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Assign each question an ID
    questions = [{"id": i, **question} for i, question in enumerate(data["questions"])]

    return questions


# Function to select a unique question
def select_unique_question(questions, asked_questions):
    # Get the IDs of questions that haven't been asked
    available_questions = [question for question in questions if question["id"] not in asked_questions]

    if not available_questions:
        # All questions have been asked
        return None

    # Select a random question from the available pool
    return random.choice(available_questions)


def wrap_text(text, font, max_width):
    words = text.split(' ')
    wrapped_lines = []
    current_line = ''

    for word in words:
        test_line = current_line + ' ' + word if current_line else word
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word

    wrapped_lines.append(current_line)

    return wrapped_lines


class Main:
    def __init__(self, screen, total_pieces):
        self.screen = screen
        self.font = pygame.font.Font(FONT, 20)

        self.message_color = pygame.Color(GREEN_MINT)
        self.running = True
        self.game_over = False
        self.CLOCK = pygame.time.Clock()
        self.total_points = 0
        self.questions = load_questions("pymaze/questions.json")
        self.question_popup = None
        self.cake_points = {}
        self.total_pieces = total_pieces  # Add total_pieces attribute
        self.asked_questions = set()
        self.asked_questions_ids = set()


    def instructions(self):
        instructions1 = self.font.render('Izmanto', True, self.message_color)
        instructions2 = self.font.render('Bultiņu taustiņus', True, self.message_color)
        instructions3 = self.font.render('lai kustētos', True, self.message_color)
        self.screen.blit(instructions1, (655, 300))
        self.screen.blit(instructions2, (610, 331))
        self.screen.blit(instructions3, (630, 362))

    # draws all configs; maze, player, instructions, and time
    def _draw_score(self):
        score_text = self.font.render(f"Punkti: {self.total_points}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (610, 10)  # Set the top-left corner of the text to (10, 10)
        self.screen.blit(score_text, score_rect)
    def _draw(self, maze, tile, player, game, clock, poi, points):
        # draw maze
        [cell.draw(self.screen, tile) for cell in maze.grid_cells]

        # Draw either cake counter or gate image based on the number of cake pieces picked up
        if game.collected_pieces < game.total_pieces:
            counter_text = self.font.render(f"{game.collected_pieces}/{game.total_pieces}", True, ORANGE)
            self.screen.blit(counter_text, (game.goal_cell.x * tile, game.goal_cell.y * tile))
        else:
            # All pieces of cake are picked up, so draw the gate image
            game.add_goal_point(self.screen)

        # draw every player movement
        player.draw(self.screen)
        player.update()

        # instructions, clock, winning message
        self.instructions()
        if self.game_over:
            clock.stop_timer()
            self.end_screen()
        else:
            clock.update_timer()
        self.screen.blit(clock.display_timer(), (605, 200))

        for point in points:
            poi.draw(self.screen, point)

        self._draw_score()

        pygame.display.flip()

    def wrap_text(text, font, max_width):
        words = text.split(' ')
        wrapped_lines = []
        current_line = ''

        for word in words:
            test_line = current_line + ' ' + word if current_line else word
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line)
                current_line = word

        wrapped_lines.append(current_line)
        return wrapped_lines


    def end_screen(self):
        self.screen.fill(ORANGE)
        end_screen = True
        thank_you_message = self.font.render('Tu uzvarēji!', True, BLACK)
        thank_you_message_rect = thank_you_message.get_rect(x=10, y=10)
        score_message = self.font.render(f'Tu ieguvi {self.total_points} punktus.', True, BLACK)
        score_message_rect = score_message.get_rect(x=10, y=40)
        exit_button = Button(10, 80, 350, 50, BLACK, WHITE, 'Iziet', 25)

        while end_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()

            self.screen.blit(thank_you_message, thank_you_message_rect)
            self.screen.blit(score_message, score_message_rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.CLOCK.tick(FPS)
            pygame.display.update()

    def rules(self):
        screen.fill(ORANGE)
        intro = True

        play_button = Button(10, 60, 350, 50, BLACK, WHITE, 'Sākt spēli', 25)  # Define the play_button here

        rules_title_text = self.font.render('Noteikumi', True, BLACK)
        rules_title_text_rect = rules_title_text.get_rect(
            x=screen.get_width() // 2 - rules_title_text.get_width() // 2,
            y=10
        )
        margin = 30
        rules_text = ('Šajā spēlē galvenais mērķis ir nokļūt līdz vārtiem, bet lai to izdarītu, '
                      'vispirms ir jāiegūst visi tortes gabali. Vārti parādīsies apakšējā labajā stūrī, kad visi tortes gabaliņi būs savākti. Lai iegūtu tortes gabalu, ir '
                      'jāatbild pareizi uz jautājumu. Izmanto klaviatūras bultiņu taustiņus, lai pārvietotos.')

        wrapped_lines = wrap_text(rules_text, self.font, screen.get_width() - 2 * margin)

        line_height = self.font.size('T')[1]  # Get the height of one line of text

        # Calculate the total height of the wrapped text
        total_text_height = len(wrapped_lines) * line_height

        # Calculate the y-coordinate for the center of the screen
        center_y = screen.get_height() // 2

        # Calculate the starting y-coordinate for the wrapped text to be centered
        text_start_y = center_y - total_text_height // 2

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(rules_title_text, rules_title_text_rect)
            # Display wrapped text centered horizontally
            y_position = text_start_y
            for line in wrapped_lines:
                line_surface = self.font.render(line, True, BLACK)
                line_rect = line_surface.get_rect(x=margin, y=y_position)
                self.screen.blit(line_surface, line_rect)
                y_position += line_height  # Move to the next line

            # Center the button horizontally and place it below the text
            button_width, button_height = play_button.rect.size
            button_x = screen.get_width() // 2 - button_width // 2
            button_y = text_start_y + total_text_height + 20  # Add some spacing between text and button
            play_button.rect.topleft = (button_x, button_y)
            self.screen.blit(play_button.image, play_button.rect)

            self.CLOCK.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        screen.fill(ORANGE)
        intro = True
        title1 = self.font.render('Liepājas dzimšanas dienas torte 2024', True, BLACK)
        title1_rect = title1.get_rect(center=(screen.get_width() // 2, 100))
        title2 = self.font.render('No Riharda Novada un Renāra Liepas.', True, BLACK)
        title2_rect = title2.get_rect(center=(screen.get_width() // 2, 150))
        play_button = Button(screen.get_width() // 2 - 175, 250, 350, 50, BLACK, WHITE, 'Sākt spēli', 25)
        rules_button = Button(screen.get_width() // 2 - 175, 320, 350, 50, BLACK, WHITE, 'Par spēli', 25)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            if rules_button.is_pressed(mouse_pos, mouse_pressed):
                self.rules()
                intro = False

            self.screen.blit(title1, title1_rect)
            self.screen.blit(title2, title2_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(rules_button.image, rules_button.rect)
            self.CLOCK.tick(FPS)
            pygame.display.update()

    def check_answer(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for index, answer_rect in enumerate(self.answer_rects):
                    if answer_rect.collidepoint(mouse_pos):
                        return chr(ord('a') + index)  # Convert index to corresponding letter ('a', 'b', 'c', 'd')

        return None  # Return None if no answer option was clicked




    # main game loop
    def main(self, frame_size, tile):
        cols, rows = frame_size[0] // tile, frame_size[-1] // tile
        maze = Maze(cols, rows)
        poi = PointsOfInterest(cols, rows)
        total_pieces = len(poi.generate_points())  # Get the total number of cake pieces
        game = Game(maze.grid_cells[-1], tile, total_pieces)  # Pass total_pieces to the Game constructor
        player = Player(tile // 3, tile // 3)
        clock = Clock()

        maze.generate_maze()
        points = poi.generate_points()
        clock.start_timer()
        decrease_timer = pygame.time.get_ticks()

        displaying_question = False

        while self.running:
            self.screen.fill(WHITE)
            self.screen.fill(pygame.Color(BROWN), (603, 0, 752, 752))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if displaying_question:
                # Handle events specific to the question popup
                # For example, check for mouse clicks on answer variants
                # and call the check_answer method of the question popup
                # Also, handle events to close the popup if needed
                    pass
                else:
                # Handle events for player movement and other main game events
                    if event.type == pygame.KEYDOWN:
                        if not self.game_over:
                        # Handle player movement key events
                            pass
                    elif event.type == pygame.KEYUP:
                        if not self.game_over:
                        # Handle player movement key release events
                            pass


                # Handle key events for player movement
                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_LEFT:
                            player.left_pressed = True
                        if event.key == pygame.K_RIGHT:
                            player.right_pressed = True
                        if event.key == pygame.K_UP:
                            player.up_pressed = True
                        if event.key == pygame.K_DOWN:
                            player.down_pressed = True
                        player.check_move(tile, maze.grid_cells, maze.thickness)

                if event.type == pygame.KEYUP:
                    if not self.game_over:
                        if event.key == pygame.K_LEFT:
                            player.left_pressed = False
                        if event.key == pygame.K_RIGHT:
                            player.right_pressed = False
                        if event.key == pygame.K_UP:
                            player.up_pressed = False
                        if event.key == pygame.K_DOWN:
                            player.down_pressed = False
                        player.check_move(tile, maze.grid_cells, maze.thickness)

            # Check collision with maze walls
            player.check_collision(maze.grid_cells, maze.thickness)

            current_time = pygame.time.get_ticks()
            if current_time - decrease_timer >= 50:  # Decrease every 1000 milliseconds (1 second)
                decrease_timer = current_time
                poi.decrease_cake_value()

            # Check collision with points of interest
            for point in points:
                if player.rect.colliderect(
                        pygame.Rect(point[0] * TILE_SIZE, point[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)):
                    points_gained = poi.remove_point(point)

                    if points_gained > 0:
                        question = self.select_unique_question(self.asked_questions)
                        self.question_popup = QuestionPopup(self.screen, question)
                        player_answer = None  # Reset player's answer
                        
                        while player_answer is None:
                            self.question_popup.show()  # Display the question popup
                            pygame.display.flip()  # Update the display to show the question popup
                            player_answer = self.question_popup.check_answer()  # Wait for player's answer

                        is_correct = player_answer == self.question_popup.correct_answer
                        self.question_popup.set_answer_state(is_correct)
                        self.question_popup.show()  # Display the feedback based on the answer state
                        pygame.display.flip()  # Update the display to show the feedback

                        if is_correct:
                            self.total_points += self.question_popup.points_awarded
                            poi.reset_cake_value()
                            self.total_points += points_gained
                            game.collected_pieces += 1
                            self.asked_questions.add(question["id"])
                            self.asked_questions_ids.add(question["id"])
                        else:
                            self.total_points = max(0, self.total_points - 250)
                            new_point = poi.move_point_randomly()
                            points.append(new_point)
                        self.asked_questions.add(question["id"])


                        start_time = pygame.time.get_ticks()
                        while pygame.time.get_ticks() - start_time < 1000:  # Wait for 1000 milliseconds (1 second)
                            pass  # Do nothing during the delay

            poi.decrease_cake_value()

            # Check if all cake pieces are picked up
            if len(points) == 0 and not self.game_over:
                if game.is_game_over(player):
                    self.game_over = True
                    player.left_pressed = False
                    player.right_pressed = False
                    player.up_pressed = False
                    player.down_pressed = False
                    self.running = False

            self._draw(maze, TILE_SIZE, player, game, clock, poi, [points])
            self.CLOCK.tick(FPS)

    def select_unique_question(self, asked_questions):
        available_question_ids = [question["id"] for question in self.questions if
                                  question["id"] not in asked_questions]

        if not available_question_ids:
            # All questions have been asked
            return None

        # Select a random question ID from the available pool
        selected_question_id = random.choice(available_question_ids)

        # Find the corresponding question object
        selected_question = next(question for question in self.questions if question["id"] == selected_question_id)


        return selected_question


if __name__ == "__main__":
    window_size = (602, 602)
    screen = (window_size[0] + 250, window_size[-1])

    screen = pygame.display.set_mode(screen)
    pygame.display.set_caption("Maze")

    total_pieces = NUMBER_OF_POINTS  # Use the value from the configs file
    game = Main(screen, total_pieces)
    game.intro_screen()
    sleep(0.2)
    game.main(window_size, TILE_SIZE)

