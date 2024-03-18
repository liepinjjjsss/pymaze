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

    def draw(self, screen, points):
        for point in points:
            x, y = point[0] * TILE_SIZE + TILE_SIZE // 2, point[1] * TILE_SIZE + TILE_SIZE // 2
            screen.blit(self.point_image, (x - POINT_SIZE // 2, y - POINT_SIZE // 2))

    def generate_points(self):
        for _ in range(NUMBER_OF_POINTS):
            self.point_tile.append((random.randint(0, self.cols - 1), random.randint(0, self.rows - 1)))
        return self.point_tile

    def decrease_cake_value(self):
        self.cake_value -= 1

    def reset_cake_value(self):
        self.cake_value = 1000

    def remove_point(self, point):
        if point in self.point_tile:
            self.point_tile.remove(point)
            self.cake_value = max(0, self.cake_value - 10)  # Decrease cake value by 10 points
            return 1000  # Return the points gained for picking up the cake
        return 0  # No points gained if the cake is not found
