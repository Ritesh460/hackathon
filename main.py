# third party libs
from random import randint
import pygame
import aubio
import numpy as num
import pyaudio
import math

# our libs
from player import Player
from pipe import Pipe


SCREEN_DIMENSIONS = (620, 820)
screen = pygame.display.set_mode((SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]))
clock = pygame.time.Clock()

CHUNK = 1024 # samples per frame
FORMAT = pyaudio.paInt16  # audio format (16-bit PCM)
CHANNELS = 1 # one channel
RATE = 44100 # samples per second
BUFFER_SIZE = 2048
CHANNELS = 1
FORMAT = pyaudio.paFloat32
METHOD = "default"
SAMPLE_RATE = 44100
HOP_SIZE = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME = HOP_SIZE

DARK_GREEN = (38, 118, 32)
PIPE_NUM = 10
PIPE_HORIZ_DISTANCE = 200
PIPE_VERT_DISTANCE = 200
GRAVITY_ACCEL = 6.5
MIC_SENSITIVITY = 50
PIPE_SPEED = -0.01

background_image = pygame.image.load("./images/flappy-bird-background.jpg").convert()
pipes = []
offset = 0

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
        pipe.draw(screen)

class Game:
    def __init__(self) -> None:
        self.stopLoop = False

        self.player = Player()

        pA = pyaudio.PyAudio()
        self.mic = pA.open(format=FORMAT, channels=CHANNELS,
            rate=SAMPLE_RATE, input=True,
            frames_per_buffer=PERIOD_SIZE_IN_FRAME)
        self.pDetection = aubio.pitch(METHOD, BUFFER_SIZE,
            HOP_SIZE, SAMPLE_RATE)
        self.pDetection.set_unit("Hz")
        self.pDetection.set_silence(-40)

    def onStart(self):
        pygame.init()
        pygame.display.set_caption('PhoneBird')
        generatePipes()

    def collision_detection(self,playerx,playery,pipes):
        closest_x = max(pipes.rectangle.left, pipes.rectangle.right)
        closest_y = max(pipes.rectangle.top,  pipes.rectangle.bottom)

        distance_x = playerx - closest_x
        distance_y = playery - closest_y

        distance = math.hypot(distance_x,distance_y)

        return distance <= playerx and distance <= playery
    def onLoop(self):
        global offset
        off = offset
        deltaTime = clock.tick(60) / 50

        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))
        for pipe in pipes:
            pipe.move(off)
        drawAllPipes()
        offset += PIPE_SPEED * deltaTime
        
        raw_audio = self.mic.read(PERIOD_SIZE_IN_FRAME, exception_on_overflow=False)
        samples = num.fromstring(raw_audio, dtype=aubio.float_type)
        pitch = self.pDetection(samples)[0]
        volume = num.sum(samples**2)/len(samples)
        # volume = "{:6f}".format(volume)
        print(str(pitch) + "\n" + str(volume) + "\n")
        if volume<=0.8:
            volume=0
 
        lift = volume * MIC_SENSITIVITY
        
        self.player.velocity.y += GRAVITY_ACCEL * deltaTime
        self.player.velocity.y -= lift * deltaTime
        self.player.velocity.y = max(min(self.player.velocity.y, 15), -15)
        
        self.player.position.y += self.player.velocity.y * deltaTime
        self.player.draw(screen)
        for pipe in pipes:
            if self.collision_detection(self.player.position.x, self.player.position.y, pipe):
                pass
                #self.stopLoop = True
                #pygame.quit()
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
