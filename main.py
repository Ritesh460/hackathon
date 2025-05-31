import pygame
import pyaudio


CHUNK = 1024 # samples per frame
FORMAT = pyaudio.paInt16  # audio format (16-bit PCM)
CHANNELS = 1 # one channel
RATE = 44100 # samples per second


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1280,720))
        self.stopLoop = False
        self.rectangle = pygame.Rect(30,60,90,60)
        p = pyaudio.PyAudio()
        self.stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    def onStart(self):
        pygame.init()
        
    
    def onLoop(self):
        pygame.draw.rect(self.screen, (0,0,255), (5,10,20,40))
        #self.rectangle.move(90,120)
        pygame.draw.rect(self.screen, (0,255,255), (200,300,5,10))
        pygame.display.flip()
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
