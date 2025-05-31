import pygame



class Player:
    def __init__(self):
        self.position = pygame.Vector2(0, 0)
        self.color = pygame.Color(255, 255, 255)

    def move(self, posx, posy):
        self.position = pygame.Vector2(posx, posy)


    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.position, 5)

