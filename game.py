import pygame

from config import *

pygame.font.init()

class Game:
    def __init__(self, goal_cell, tile, total_pieces):
        self.font = pygame.font.Font(FONT, 35)

        self.goal_cell = goal_cell
        self.tile = tile
        self.total_pieces = total_pieces
        self.collected_pieces = 0
        self.lock_font = pygame.font.Font(FONT, 20)

    def add_goal_point(self, screen):
        # Display the lock counter until all pieces are collected
        if self.collected_pieces < self.total_pieces:
            lock_text = self.lock_font.render(f"{self.collected_pieces}/{self.total_pieces}", True, BLACK)
            lock_rect = lock_text.get_rect()
            lock_rect.topleft = (self.goal_cell.x * self.tile, self.goal_cell.y * self.tile)
            screen.blit(lock_text, lock_rect)
        else:
            # Add the gate image when all pieces are collected
            img_path = 'pymaze/assets/full_cake.png'
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (self.tile, self.tile))
            screen.blit(img, (self.goal_cell.x * self.tile, self.goal_cell.y * self.tile))

    def message(self):
        return self.font.render('Uzvara!', True, ORANGE)

    def is_game_over(self, player):
        goal_cell_abs_x, goal_cell_abs_y = self.goal_cell.x * self.tile, self.goal_cell.y * self.tile
        if player.x >= goal_cell_abs_x and player.y >= goal_cell_abs_y and self.collected_pieces >= self.total_pieces:
            return True
        else:
            return False

    def activate_end_gate(self):
        # Increment the collected pieces counter to unlock the gate
        self.collected_pieces += 1


class Button:
	def __init__(self, x, y, width, height, fg, bg, contnet, fontsize):
		self.font = pygame.font.Font(FONT, fontsize)
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