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
PIPE_VERT_DISTANCE = 250
GRAVITY_ACCEL = 6.5
MIC_SENSITIVITY = 200
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
        self.font = None # Will be initialized in onStart
        self.small_font = None # Will be initialized in onStart
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
        self.font = pygame.font.Font(None, 74) # Initialize font
        self.small_font = pygame.font.Font(None, 36) # For "Play Again"
        generatePipes()

    def reset_game(self):
        global offset
        self.player.setPosition(80, 350) # Reset player position
        self.player.velocity = pygame.Vector2(0, 0) # Reset player velocity
        generatePipes() # Regenerate pipes
        offset = 0 # Reset pipe offset
        self.stopLoop = False # Allow the game loop to run again

    def collision_detection(self, playerx, playery, radius, pipe: Pipe):
        rect = pipe.rectangle
        
        closest_x = max(rect.left, min(playerx, rect.right))
        closest_y = max(rect.top,  min(playery, rect.bottom))
    
        distance_x = playerx - closest_x
        distance_y = playery - closest_y
        distance_squared = distance_x**2 + distance_y**2
    
        return distance_squared <= radius**2

    def onLoop(self):
        global offset
        off = offset
        deltaTime = clock.tick(60) / 50

        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))
        for pipe_obj in pipes: # Renamed pipe to pipe_obj to avoid conflict with the imported Pipe class
            pipe_obj.move(off) # Assuming pipe_obj has a move method
        drawAllPipes()
        offset += PIPE_SPEED * deltaTime
        
        raw_audio = self.mic.read(PERIOD_SIZE_IN_FRAME, exception_on_overflow=False)
        samples = num.fromstring(raw_audio, dtype=aubio.float_type)
        volume = num.sum(samples**2)/len(samples)
        # volume = "{:6f}".format(volume)
        #print(str(pitch) + "\n" + str(volume) + "\n")
        if volume<=0.8: # User changed this from 0.1
            volume=0
 
        lift = volume * MIC_SENSITIVITY
        
        self.player.velocity.y += GRAVITY_ACCEL * deltaTime
        self.player.velocity.y -= lift * deltaTime
        self.player.velocity.y = max(min(self.player.velocity.y, 15), -15)
        
        self.player.position.y += self.player.velocity.y * deltaTime
        self.player.draw(screen)

        # Player-Pipe collision
        for pipe_instance in pipes: # Changed back to pipe_instance for clarity
            if self.collision_detection(self.player.position.x, self.player.position.y, 30, pipe_instance): # 30 is player radius
                self.stopLoop = True
                break # Exit loop once a collision is detected
        
        # Player-Screen bounds collision
        if not self.stopLoop: # Only check if no pipe collision yet
            if self.player.position.y - 30 < 0 or self.player.position.y + 30 > SCREEN_DIMENSIONS[1]: # 30 is player radius
                self.stopLoop = True

        if self.stopLoop: # If collision detected
            self.show_game_over_screen() # Show game over screen
            # The game loop in main() will handle restarting or quitting based on show_game_over_screen's outcome
            return # Return to main loop to handle stopLoop state

        processEvents() # processEvents currently only handles QUIT during gameplay
  
        pygame.display.flip()
        return

    def show_game_over_screen(self):
        screen.fill((0,0,0)) # Black background for game over
        game_over_text = self.font.render("Game Over", True, (255, 255, 255))
        play_again_text = self.small_font.render("Press R to Play Again", True, (255, 255, 255))
        quit_text = self.small_font.render("Press Q to Quit", True, (255,255,255))

        game_over_rect = game_over_text.get_rect(center=(SCREEN_DIMENSIONS[0]//2, SCREEN_DIMENSIONS[1]//2 - 50))
        play_again_rect = play_again_text.get_rect(center=(SCREEN_DIMENSIONS[0]//2, SCREEN_DIMENSIONS[1]//2 + 20))
        quit_rect = quit_text.get_rect(center=(SCREEN_DIMENSIONS[0]//2, SCREEN_DIMENSIONS[1]//2 + 60))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(play_again_text, play_again_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit # Exit the whole application
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game() # This sets self.stopLoop = False
                        waiting_for_input = False # Exit this loop to restart the game in the main loop
                    if event.key == pygame.K_q:
                        pygame.quit()
                        raise SystemExit # Exit the whole application
            clock.tick(15) # Keep the loop from running too fast
    
    def onEnd(self):
        pygame.quit()

def processEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit


def main():
    game = Game()
    game.onStart()
    running = True # Control the main game loop
    while running:
        if not game.stopLoop:
            game.onLoop()
        else:
            # When stopLoop is true, it means a game over condition was met.
            # onLoop would have called show_game_over_screen.
            # If the player chose to restart, reset_game() was called, setting game.stopLoop to False.
            # If the player chose to quit, SystemExit would have been raised.
            # If game.stopLoop is still True here, it means show_game_over_screen was somehow bypassed or an error occurred.
            # However, with the current logic, show_game_over_screen handles its own loop and will either reset stopLoop or quit.
            # If reset_game was called, stopLoop becomes false, and the next iteration of this outer loop will call onLoop().
            pass # Explicitly do nothing, waiting for stopLoop to change or program to exit.

        # Check for quit event in the main loop as a fallback,
        # although onLoop -> processEvents and show_game_over_screen also handle QUIT.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    game.onEnd()

if __name__ == "__main__":
    main()
