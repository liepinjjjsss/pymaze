import pygame
import random

class PointOfInterest():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10  # Adjust the size as needed

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius)
