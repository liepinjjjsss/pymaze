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
        #for point in self.point_tile:
        
        self.x, self.y = tile[0] * TILE_SIZE, tile[-1] * TILE_SIZE
        pygame.draw.circle(screen, BLACK, (self.x, self.y), POINT_SIZE)
        #print(self.x, self.y)

    def generate_points(self):
        for point in range(NUMBER_OF_POINTS):
            self.point_tile.append((random.randint(0, self.cols), random.randint(0, self.rows)))
        #print(self.point_tile)
        #self._draw()
        return self.point_tile

    def remove_point(self, coordnates):
        pass
        