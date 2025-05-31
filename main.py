import pygame



def main():
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    continueLoop = True
    while (continueLoop):
        rect = pygame.Rect(10, 10, 20, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

if __name__ == "__main__":
    main()
