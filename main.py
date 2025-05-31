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
        self.color = (38,118,32)
        p = pyaudio.PyAudio()
        self.stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    def onStart(self):
        pygame.init()
        
    
    def onLoop(self):
        pygame.draw.rect(self.screen, self.color, (150,0,40,250))
        #self.rectangle.move(90,120)
        pygame.draw.rect(self.screen, self.color, (150,450,40,400))
        pygame.draw.rect(self.screen, self.color, (350,0,40,200))
        pygame.draw.rect(self.screen, self.color, (350,400,40,350))
        pygame.draw.rect(self.screen, self.color, (550,0,40,150))
        pygame.draw.rect(self.screen, self.color, (550,350,40,400))
        pygame.draw.rect(self.screen, self.color, (750,0,40,150))
        pygame.draw.rect(self.screen, self.color, (750,450,40,400))
        
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
