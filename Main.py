import pygame, elements, ctypes

def main():
    pygame.mixer.init(44100, -16, 2, 512)
    pygame.init()

    FPS = 60
    fullscreen = True

    # Screen & Pygame Initialization
    SCREEN_SIZE = (1200, 720)
    if fullscreen:
        SCREEN_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        Screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    else:
        Screen = pygame.display.set_mode(SCREEN_SIZE)

    if float(pygame.display.Info().current_w) / float(pygame.display.Info().current_h) != 16.0/9.0:
        print ("You need a 16:9 resolution to play this game.")
        ctypes.windll.user32.MessageBoxA(0, "You need a 16:9 resolution to play this game.", "Error", 0)
        quit()

    pygame.display.set_caption("Scout's Pancake Factory")
    Clock = pygame.time.Clock()
    state_game = False
    TS = elements.TitleScreen(Screen)
    GAME = elements.Game(Screen)
    while True:
        if (state_game):
            GAME.eventLoop(Clock)
        else:
            TS.eventLoop(Clock)
            state_game = TS.startGame
            if (state_game):
                TS.quit()

        Clock.tick(FPS)


if __name__ == '__main__':
    main()
