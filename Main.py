import pygame, elements, ctypes, logging

def main():
    FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logger = logging.getLogger("spf")

    logger.info("Initializing pygame")
    pygame.mixer.init(44100, -16, 2, 512)
    pygame.mixer.music.set_volume(elements.ConfigUtility.getConfigSetting("volume"))
    pygame.init()

    FPS = 60
    fullscreen = elements.ConfigUtility.getConfigSetting("fullscreen")

    # Screen & Pygame Initialization

    if fullscreen:
        SCREEN_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        Screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    else:
        SCREEN_SIZE = (elements.ConfigUtility.getConfigSetting("windowed_width"),
                       elements.ConfigUtility.getConfigSetting("windowed_height"))
        Screen = pygame.display.set_mode(SCREEN_SIZE)

    if float(pygame.display.Info().current_w) / float(pygame.display.Info().current_h) != 16.0/9.0:
        logger.critical("This game requires a 16:9 resolution to play.")
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
            done = GAME.endGame
            if (done):
                logger.info("GAME is done, initing TitleScreen")
                state_game = False
                GAME.quit()
                TS.__init__(Screen)
        else:
            TS.eventLoop(Clock)
            start = TS.startGame
            if (start):
                logger.info("TitleScreen is done, initing GAME")
                state_game = True
                GAME.__init__(Screen)
                TS.quit()

        Clock.tick(FPS)


if __name__ == '__main__':
    main()