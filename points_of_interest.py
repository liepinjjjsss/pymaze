import pygame
import random
from config import *

class PointsOfInterest:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.thickness = WALL_THICKNESS
        self.point_tile = []
        self.point_image = pygame.image.load("assets/cake_piece.png")  # Load the image
        self.point_image = pygame.transform.scale(self.point_image, (POINT_SIZE*2, POINT_SIZE*2))  # Scale the image
        self.cake_value = 1000  # Initial value of the cake
        self.last_decrease_time = pygame.time.get_ticks()  # Track the last time the cake value was decreased

    def draw(self, screen, points):
        for point in points:
            x, y = point[0] * TILE_SIZE + TILE_SIZE // 2, point[1] * TILE_SIZE + TILE_SIZE // 2
            screen.blit(self.point_image, (x - POINT_SIZE // 2, y - POINT_SIZE // 2))

    def generate_points(self):
        self.point_tile = []
        while len(self.point_tile) < NUMBER_OF_POINTS:
            new_point = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))
            if new_point not in self.point_tile:
                self.point_tile.append(new_point)
        return self.point_tile

    def decrease_cake_value(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_decrease_time >= 50:  # Decrease cake value every 50 milliseconds
            self.cake_value -= 1
            self.last_decrease_time = current_time

    def reset_cake_value(self):
        self.cake_value = 1000

    def remove_point(self, point):
        if point in self.point_tile:
            self.point_tile.remove(point)
            return self.cake_value  # Return the points gained for picking up the cake
        return 0

    def move_point_randomly(self):
        new_position = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))
        while new_position in self.point_tile:
            new_position = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))
        return new_position
