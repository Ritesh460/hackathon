import pygame


class Player:
    def __init__(self):
        self.position = pygame.Vector2(80, 350)
        self.velocity = pygame.Vector2(0, 0)
        self.color = pygame.Color(100, 0, 0)

        self.radius = 30

        self.sprite = pygame.image.load("images/player.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.radius * 2, self.radius * 2))

    def move(self, posx, posy):
        self.position = pygame.Vector2(posx + self.position.x, posy + self.position.y)

    def updatePosition(self):
        self.move(self.velocity.x, self.velocity.y)

    def setPosition(self, posx, posy):
        self.position = pygame.Vector2(posx, posy)

    def draw(self, screen: pygame.Surface):
        draw_pos = (self.position.x - self.radius, self.position.y - self.radius)
        screen.blit(self.sprite, draw_pos)
        # pygame.draw.circle(screen, self.color, self.position, 30)

