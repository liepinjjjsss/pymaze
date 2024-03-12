import pygame

from config import *

pygame.font.init()

class Game:
	def __init__(self, goal_cell, tile):
		self.font = pygame.font.Font(FONT, 35)

		self.goal_cell = goal_cell
		self.tile = tile

	# add goal point for player to reach
	def add_goal_point(self, screen):
		# adding gate for the goal point
		img_path = 'img/gate.png'
		img = pygame.image.load(img_path)
		img = pygame.transform.scale(img, (self.tile, self.tile))
		screen.blit(img, (self.goal_cell.x * self.tile, self.goal_cell.y * self.tile))

	# winning message
	def message(self):
		msg = self.font.render('You Win!!', True, ORANGE)
		return msg

	# checks if player reached the goal point
	def is_game_over(self, player):
		goal_cell_abs_x, goal_cell_abs_y = self.goal_cell.x * self.tile, self.goal_cell.y * self.tile
		if player.x >= goal_cell_abs_x and player.y >= goal_cell_abs_y:
			return True
		else:
			return False


class Button:
	def __init__(self, x, y, width, height, fg, bg, contnet, fontsize):
		self.font = pygame.font.Font('PressStart.ttf', fontsize)
		self.contnet = contnet

		self.x = x
		self.y = y

		self.bg = bg
		self.fg = fg

		self.width = width
		self.height = height
		
		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(self.bg)
		self.rect = self.image.get_rect()

		self.rect.x = self.x
		self.rect.y = self.y

		self.text = self.font.render(self.contnet, True, self.fg)
		self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
		self.image.blit(self.text, self.text_rect)

	def is_pressed(self, pos, pressed):
		if self.rect.collidepoint(pos):
			if pressed[0]:
				return True
			return False
		return False