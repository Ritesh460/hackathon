# third party libs
from random import randint
import pygame
import pyaudio

# our libs
from player import Player
from pipe import Pipe


SCREEN_DIMENSIONS = (1280, 720)
SCREEN = pygame.display.set_mode((SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]))

CHUNK = 1024 # samples per frame
FORMAT = pyaudio.paInt16  # audio format (16-bit PCM)
CHANNELS = 1 # one channel
RATE = 44100 # samples per second

DARK_GREEN = (38, 118, 32)
PIPE_NUM = 10
PIPE_HORIZ_DISTANCE = 150
PIPE_VERT_DISTANCE = 50
GRAVITY_CONSTANT = 6

pipes = []


def generatePipes():
    pipes.clear()
    for i in range(PIPE_NUM):
        x = i * PIPE_HORIZ_DISTANCE
        center_y = randint(150, SCREEN_DIMENSIONS[1] - 150)

        top_height = center_y - (PIPE_VERT_DISTANCE // 2)
        bottom_y = center_y + (PIPE_VERT_DISTANCE // 2)
        bottom_height = SCREEN_DIMENSIONS[1] - bottom_y

        r = randint(0, 50) 
        g = randint(150, 255)
        b = randint(0, 50)
        col = (r, g, b)

        pipes.append(Pipe(col, top_height, x))
        pipes.append(Pipe(col, bottom_height, x, bottom_y)) 

def drawAllPipes():
    for pipe in pipes:
        pipe.draw(SCREEN)

class Game:
    def __init__(self) -> None:
        self.stopLoop = False
        generatePipes()

        self.player = Player()
        p = pyaudio.PyAudio()
        self.stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    def onStart(self):
        pygame.init()
        
    def onLoop(self):
        drawAllPipes()
        self.player.draw(SCREEN)
        self.player.move(0, -GRAVITY_CONSTANT)

        processEvents()
        processMicrophone()

        pygame.display.flip()
        return
    
    def onEnd(self):
        pygame.quit()

def processEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

def processMicrophone():
    return


def main():
    game = Game()
    game.onStart()
    while(game.stopLoop == False):
        game.onLoop();
    game.onEnd()

if __name__ == "__main__":
    main()
