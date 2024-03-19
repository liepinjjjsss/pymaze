import pygame
from time import sleep
import sys
import json

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


class Main:
    def __init__(self, screen, total_pieces):
        self.screen = screen
        self.font = pygame.font.Font(FONT, 20)

        self.message_color = pygame.Color(GREEN_MINT)
        self.running = True
        self.game_over = False
        self.CLOCK = pygame.time.Clock()
        self.total_points = 0
        self.questions = load_questions("questions.json")
        self.question_popup = None
        self.cake_points = {}
        self.total_pieces = total_pieces  # Add total_pieces attribute

    def instructions(self):
        instructions1 = self.font.render('Use', True, self.message_color)
        instructions2 = self.font.render('Arrow Keys', True, self.message_color)
        instructions3 = self.font.render('to Move', True, self.message_color)
        self.screen.blit(instructions1, (655, 300))
        self.screen.blit(instructions2, (610, 331))
        self.screen.blit(instructions3, (630, 362))

    # draws all configs; maze, player, instructions, and time
    def _draw_score(self):
        score_text = self.font.render(f"Score: {self.total_points}", True, WHITE)
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
            self.screen.blit(game.message(), (610, 120))
        else:
            clock.update_timer()
        self.screen.blit(clock.display_timer(), (605, 200))

        for point in points:
            poi.draw(self.screen, point)

        self._draw_score()

        pygame.display.flip()

    def rules(self):
        screen.fill(ORANGE)
        intro = True

        play_button = Button(10, 60, 350, 50, BLACK, WHITE, 'Sākt spēli', 25)
        rules_title_text = self.font.render('Noteikumi', True, BLACK)
        rules_title_text_rect = rules_title_text.get_rect(x=10, y=10)
        rules_text1 = self.font.render('Šajā spēlē galvenais mērķis ir nokļūt līdz', True, BLACK)
        rules_text1_rect = rules_text1.get_rect(x=10, y=10)
        rules_text2 = self.font.render('vārtiem, bet lai to izdarītu, vispirms ir', True, BLACK)
        rules_text3 = self.font.render('jāiegūst visi tortes gabali. Lai iegūtu', True, BLACK)
        rules_text4 = self.font.render('tortes gabalu, ir jāatbild pareizi uz jautājumu', True, BLACK)
        rules_text5 = self.font.render('jautājumu. Ja ', True, BLACK)
        rules_text6 = self.font.render('Izmanto klaviatūras bultas lai pārvietots.', True, BLACK)

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
            self.screen.blit(rules_title_text, rules_title_text_rect)
            self.screen.blit(play_button.image, play_button.rect)

            self.CLOCK.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        screen.fill(ORANGE)
        intro = True
        title1 = self.font.render('Liepājas dzimšanas dienas torte 2024', True, BLACK)
        title1_rect = title1.get_rect(x=10, y=10)
        title2 = self.font.render('No Riharda Novada un Renāra Liepas.', True, BLACK)
        title2_rect = title2.get_rect(x=10, y=40)
        play_button = Button(10, 80, 350, 50, BLACK, WHITE, 'Sākt spēli', 25)
        rules_button = Button(10, 150, 350, 50, BLACK, WHITE, 'Par spēli', 25)

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
                        question = select_question(self.questions)
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
                        else:
                            self.total_points = max(0, self.total_points - 250)
                            new_point = poi.move_point_randomly()
                            points.append(new_point)

                        start_time = pygame.time.get_ticks()
                        while pygame.time.get_ticks() - start_time < 1000:  # Wait for 1000 milliseconds (1 second)
                            pass  # Do nothing during the delay

                        if is_correct:
                            print("Correct")
                        else:
                            print("Incorrect")

            poi.decrease_cake_value()

            # Check if all cake pieces are picked up
            if len(points) == 0 and not self.game_over:
                if game.is_game_over(player):
                    self.game_over = True
                    player.left_pressed = False
                    player.right_pressed = False
                    player.up_pressed = False
                    player.down_pressed = False
                    self.screen.blit(game.message(), (610, 120))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    self.running = False

            self._draw(maze, TILE_SIZE, player, game, clock, poi, [points])
            self.CLOCK.tick(FPS)


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

