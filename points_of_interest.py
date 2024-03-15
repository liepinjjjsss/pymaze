import pygame

import random

from config import *


class PointsOfInterest:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.thickness = WALL_THICKNESS
        self.point_tile = []
        #self.screen = screen

    def draw(self, screen, tile):
        self.x = tile[0] * TILE_SIZE + TILE_SIZE / 2
        self.y = tile[-1] * TILE_SIZE + TILE_SIZE / 2
        pygame.draw.circle(screen, BLACK, (self.x, self.y), POINT_SIZE)


    def generate_points(self):
        for point in range(NUMBER_OF_POINTS):
            self.point_tile.append((random.randint(0, self.cols - 1), random.randint(0, self.rows - 1)))
        return self.point_tile

    def remove_point(self, coordnates):
        pass
        