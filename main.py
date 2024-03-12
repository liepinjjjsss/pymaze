import pygame, sys

from time import sleep

from clock import Clock
from maze import Maze
from player import Player
from game import Game, Button
from config import *

pygame.init()
pygame.font.init()

class Main():
	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.Font(FONT, 20)
		
		self.message_color = pygame.Color(GREEN_MINT)
		self.running = True
		self.game_over = False
		self.CLOCK = pygame.time.Clock()

	def instructions(self):
		instructions1 = self.font.render('Use', True, self.message_color)
		instructions2 = self.font.render('Arrow Keys', True, self.message_color)
		instructions3 = self.font.render('to Move', True, self.message_color)
		self.screen.blit(instructions1,(655,300))
		self.screen.blit(instructions2,(610,331))
		self.screen.blit(instructions3,(630,362))

	# draws all configs; maze, player, instructions, and time
	def _draw(self, maze, tile, player, game, clock):
		# draw maze
		[cell.draw(self.screen, tile) for cell in maze.grid_cells]
		# add a goal point to reach
		game.add_goal_point(self.screen)
		# draw every player movement
		player.draw(self.screen)
		player.update()
		# instructions, clock, winning message
		self.instructions()
		if self.game_over:
			clock.stop_timer()
			self.screen.blit(game.message(),(610,120))
		else:
			clock.update_timer()
		self.screen.blit(clock.display_timer(), (605,200))
	
		pygame.display.flip()

	def rules(self):
		screen.fill(ORANGE)
		intro = True
		title = self.font.render('Hlo', True, BLACK)
		title_rect = title.get_rect(x=10, y=10)
		play_button = Button(10, 60, 350, 50, BLACK, WHITE, 'Sākt spēli', 25)

		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()
			if play_button.is_pressed(mouse_pos, mouse_pressed):
				intro = False

			self.screen.blit(title, title_rect)
			self.screen.blit(play_button.image, play_button.rect)

			self.CLOCK.tick(FPS)
			pygame.display.update()

	def intro_screen(self):
		screen.fill(ORANGE)
		intro = True
		title = self.font.render('Liepājas dzimšanas dienas torte 2024', True, BLACK)
		title_rect = title.get_rect(x=10, y=10)
		play_button = Button(10, 60, 350, 50, BLACK, WHITE, 'Sākt spēli', 25)
		rules_button = Button(10, 130, 350, 50, BLACK, WHITE, 'Par spēli', 25)

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
			
			self.screen.blit(title, title_rect)
			self.screen.blit(play_button.image, play_button.rect)
			self.screen.blit(rules_button.image, rules_button.rect)
			self.CLOCK.tick(FPS)
			pygame.display.update()

	# main game loop
	def main(self, frame_size, tile):
		cols, rows = frame_size[0] // tile, frame_size[-1] // tile
		maze = Maze(cols, rows)
		game = Game(maze.grid_cells[-1], tile)
		player = Player(tile // 3, tile // 3)
		clock = Clock()

		maze.generate_maze()
		clock.start_timer()

		while self.running:
			self.screen.fill(WHITE)
			self.screen.fill( pygame.Color(BROWN), (603, 0, 752, 752))
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			# if keys were pressed still
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
		
			# if pressed key released
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

			if game.is_game_over(player):
				self.game_over = True
				player.left_pressed = False
				player.right_pressed = False
				player.up_pressed = False
				player.down_pressed = False

			self._draw(maze, tile, player, game, clock)
			self.CLOCK.tick(FPS)




if __name__ == "__main__":
	window_size = (602, 602)
	screen = (window_size[0] + 250, window_size[-1])
	tile_size = 60 # For debuging purposes tile size is not 30
	screen = pygame.display.set_mode(screen)
	pygame.display.set_caption("Maze")

	game = Main(screen)
	game.intro_screen()
	sleep(0.2) # TODO: Fix a bug where programm crashes when the start button is pressed longer than few frames
	game.main(window_size, tile_size)
