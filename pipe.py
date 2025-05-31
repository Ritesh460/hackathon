import pygame

import random

PIPE_WIDTH = 40

class Pipe:
    def __init__(self, color, height, absPosX = 0, absPosY = 0) -> None:
        self.color = color
        self.rectangle = pygame.Rect(absPosX, absPosY, PIPE_WIDTH, height)

    def move(self, posx, posy = 0):
        self.rectangle.x = self.rectangle.x + posx
        self.rectangle.y = self.rectangle.y + posy

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rectangle)

    def checkBounds(self, bounds):
        pass
