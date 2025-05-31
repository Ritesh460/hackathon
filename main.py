# third party libs
import aubio
import numpy as num
import pyaudio
import pygame
import sys

# our libs
from player import Player


BUFFER_SIZE = 2048
CHANNELS = 1
FORMAT = pyaudio.paFloat32
METHOD = "default"
SAMPLE_RATE = 44100
HOP_SIZE = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME = HOP_SIZE

DARK_GREEN = (38, 118, 32)

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1280,720))
        self.stopLoop = False
        self.rectangle = pygame.Rect(30,60,90,60)

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
        
    
    def onLoop(self):
        
        raw_audio = self.mic.read(PERIOD_SIZE_IN_FRAME)
        samples = num.fromstring(raw_audio,
            dtype=aubio.float_type)
        pitch = self.pDetection(samples)[0]
        volume = num.sum(samples**2)/len(samples)
        volume = "{:6f}".format(volume)
        print(str(pitch) + "\n" + str(volume) + "\n")


        pygame.draw.rect(self.screen, DARK_GREEN, (150,0,40,250))
        #self.rectangle.move(90,120)
        pygame.draw.rect(self.screen, DARK_GREEN, (150,450,40,400))
        pygame.draw.rect(self.screen, DARK_GREEN, (350,0,40,200))
        pygame.draw.rect(self.screen, DARK_GREEN, (350,400,40,350))
        pygame.draw.rect(self.screen, DARK_GREEN, (550,0,40,150))
        pygame.draw.rect(self.screen, DARK_GREEN, (550,350,40,400))
        pygame.draw.rect(self.screen, DARK_GREEN, (750,0,40,150))
        pygame.draw.rect(self.screen, DARK_GREEN, (750,450,40,400))
        pygame.draw.rect(self.screen, DARK_GREEN, (950,450,40,400))
        pygame.display.flip()
        self.player.draw(self.screen)

        self.player.move(0, -5)
        processEvents()
        processMicrophone()
        return
    
    
    def onEnd(self):
        return

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
