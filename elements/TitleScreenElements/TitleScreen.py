import pygame, os, random, webbrowser, json, elements.ConfigUtility, time, logging
from elements.TitleScreenElements.TSButton import TSButton
from elements.TitleScreenElements.TSButtonContainer import TSButtonContainer
from elements.TitleScreenElements.TSOptionsWindow import TSWindow
from elements.HUDElements.FloatText import FloatText
import elements.HUDElements.ScaleUtility as ScaleUtility
class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_W = pygame.display.Info().current_w
        self.SCREEN_H = pygame.display.Info().current_h
        self.didQuit = False
        self.showFPS = elements.ConfigUtility.getConfigSetting("fps_counter")
        self.FPS_SURFACE = pygame.Surface(ScaleUtility.scalePos(100, 50))
        self.version = "0.1.0"
        pygame.mouse.set_visible(True)

        self.logger = logging.getLogger('spf')
        self.logger.info("Initializing TitleScreen Class")

        self.FloatText = FloatText(screen, ScaleUtility.scaleValue(25))
        pygame.mouse.set_visible(True)

        self.languageFile = json.load(open(self.getLocalFile('../../resource/language/en_US.json'), 'r'))

        self.randomBackground = self.returnRandomBackground()
        self.blitBackground(self.randomBackground)

        if elements.ConfigUtility.getConfigSetting("ts_music_enable"):
            self.playRandomMusic()

        self.addFooter()
        self.buttonSurface = self.screen #pygame.Surface((self.SCREEN_W, self.SCREEN_H))

        # non-containers, actual buttons
        quitButtonRes = self.scaleResSurface(50, 975, 400, 75)
        settingsButtonRes = self.scaleResSurface(500, 975, 400, 75)

        # container buttons
        playContainerRes = ScaleUtility.scaleResSurface(50, 350, 520, 70)
        htpContainerRes = ScaleUtility.scaleResSurface(50, 800, 520, 70)
        customizeContainerRes = ScaleUtility.scaleResSurface(50, 500, 520, 100)
        supportContainerRes = ScaleUtility.scaleResSurface(50, 725, 520, 70)

        self.quitButton = TSButton(self.screen, quitButtonRes[0], quitButtonRes[1], quitButtonRes[2], quitButtonRes[3], self.getLanguageString('#SPF_Quit_Button_Title'), footerButton=True)
        self.settingsButton = TSButton(self.screen, settingsButtonRes[0], settingsButtonRes[1], settingsButtonRes[2], settingsButtonRes[3], self.getLanguageString('#SPF_Settings_Button_Title'), footerButton=True)

        self.playButton = TSButton(self.buttonSurface, 50, 300, 500, 75, self.getLanguageString('#SPF_Play_Button_Title'))
        self.htpButton = TSButton(self.buttonSurface, 50, 600, 500, 75, self.getLanguageString('#SPF_HowToPlay_Button_Title'))
        self.loadoutButton = TSButton(self.buttonSurface, 50, 400, 275, 75, self.getLanguageString('#SPF_Loadout_Button_Title'))
        self.codeButton = TSButton(self.buttonSurface, 350, 400, 200, 75, self.getLanguageString('#SPF_Code_Button_Title'))
        self.supportButton = TSButton(self.buttonSurface, 0,0,0,0, self.getLanguageString('#SPF_Support_Button_Title'))

        self.buttons = [self.quitButton, self.playButton, self.htpButton, self.settingsButton, self.loadoutButton,
                        self.codeButton, self.supportButton]
        self.containButtons = [self.loadoutButton, self.codeButton]
        padding = (ScaleUtility.scaleValue(8), ScaleUtility.scaleValue(10))
        self.playContainer = TSButtonContainer(self.screen, "", self.playButton,  padding, 0, playContainerRes[0], playContainerRes[1], playContainerRes[2], playContainerRes[3])
        self.customizeContainer = TSButtonContainer(self.screen, "Customize", self.containButtons, (ScaleUtility.scaleValue(5), ScaleUtility.scaleValue(10)), ScaleUtility.scaleValue(10), customizeContainerRes[0], customizeContainerRes[1], customizeContainerRes[2], customizeContainerRes[3])
        self.supportContainer = TSButtonContainer(self.screen, "", self.supportButton, padding, 0, supportContainerRes[0], supportContainerRes[1], supportContainerRes[2], supportContainerRes[3])
        self.buttonContainer = TSButtonContainer(self.screen, "", self.htpButton, padding, 0, htpContainerRes[0], htpContainerRes[1], htpContainerRes[2], htpContainerRes[3])
                                                 
        self.containers = [self.playContainer, self.customizeContainer, self.supportContainer, self.buttonContainer]

        self.startGame = False
        self.joystickConnected = False

        self.buttonClick = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/menu/buttonclick.wav'))
        self.buttonRelease = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/menu/buttonclickrelease.wav'))
        self.buttonNotSupportedSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/menu/button_fail.wav'))
        self.notificationSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/menu/notification_alert.wav'))

        self.notificationImage = pygame.image.load(os.path.join(os.path.dirname(__file__), '../../resource/images/menu/button_alert.png')).convert()
        self.notificationImage.set_colorkey((255,255,255))
        self.blitNotificationImage = False

        self.testSurface = pygame.Surface(ScaleUtility.scalePos(800, 600))
        self.testWindow = TSWindow(self.testSurface)
        self.testWindow.setTitle("Options")
        logoRes = ScaleUtility.scaleResSurface(50, 25, 520, 300)
        self.logoFile = pygame.transform.smoothscale(pygame.image.load(os.path.join(os.path.dirname(__file__), '../../resource/images/menu/spf_title.png')).convert(), (logoRes[2] - ScaleUtility.scaleValue(10) * 2, logoRes[3] - ScaleUtility.scaleValue(10) * 2))

    def getLocalFile(self, file):
        self.logger.info("Grabbing language file from: " + os.path.join(os.path.dirname(__file__), file))
        return os.path.join(os.path.dirname(__file__), file)

    def getLanguageString(self, string):
        returnS = ""
        try:
            returnS = self.languageFile['strings'][string]
        except KeyError:
            returnS = string
        return returnS


    def blit(self):
        self.screen.fill((0,0,0))
        self.blitBackground(self.randomBackground)
        self.addFooter()
        self.blitLogo()
        for container in self.containers:
            container.drawBackground()

    def quit(self):
        if not self.didQuit:
            pygame.mixer.music.stop()

            self.didQuit = True

    def blitFPS(self, Clock):
        pygame.draw.rect(self.FPS_SURFACE, (0,0,0), ScaleUtility.scaleResSurface(0, 0, 100, 50))

        font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../resource/fonts/tf2secondary.ttf'), ScaleUtility.scaleValue(36))
        text = font.render(str(round(Clock.get_fps(), 2)), True, (255, 255, 0))

        text_w = text.get_rect().width
        text_h = text.get_rect().height

        self.FPS_SURFACE.blit(text, ((0 + ScaleUtility.scaleValue(100) / 2) - text_w / 2, (0 + ScaleUtility.scaleValue(50) / 2) - text_h / 2))
        self.screen.blit(self.FPS_SURFACE, ScaleUtility.scalePos(1750,25))

    def eventLoop(self, Clock):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit() # Exit
                if event.key == pygame.K_F12:
                    self.showFPS = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F12:
                    self.showFPS = False
                if event.key == pygame.K_F11:
                    t = time.localtime()
                    time_string = str(t.tm_year) + "-" + str(t.tm_mon) + "-" + str(t.tm_mday) + "_" + str(t.tm_hour) + "." + str(t.tm_min) + "." + str(t.tm_sec)
                    pygame.image.save(self.screen, os.path.join(os.path.expanduser("~"), "Pictures/SPF/" + time_string + ".jpg"))
                    self.FloatText.addText("Screenshot saved as " + time_string, 5)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseAction(True)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseAction(False)

            elif event.type == pygame.QUIT:
                pygame.quit()

        self.blit()

        for button in self.buttons:
            button.updateButton()

        if self.showFPS:
            self.blitFPS(Clock)

        if (self.blitNotificationImage):
            self.screen.blit(self.notificationImage, (1700, 0))

        if (self.testWindow.isOpen):
            self.testWindow.update((self.SCREEN_W / 2 - self.testSurface.get_width() / 2 + 100, self.SCREEN_H / 2 - self.testSurface.get_height() / 2), self)
            self.screen.blit(self.testSurface, (self.SCREEN_W / 2 - self.testSurface.get_width() / 2 + 100, self.SCREEN_H / 2 - self.testSurface.get_height() / 2))

        if (pygame.joystick.get_count() > 0 and not self.joystickConnected):
            self.logger.info("Found joystick")
            self.notificationSound.play()
            self.joystickConnected = True
            self.blitNotificationImage = True
        self.FloatText.update()

        pygame.display.update()

    def blitLogo(self):
        BAR_COLOR = (53, 50, 45)
        PADDING = ScaleUtility.scalePos(10,10)
        AREA = ScaleUtility.scaleResSurface(50, 25, 520, 300)

        pygame.draw.rect(self.screen, BAR_COLOR, AREA)
        self.screen.blit(self.logoFile, (AREA[0] + PADDING[0], AREA[1] + PADDING[1]))

    def blitBackground(self, background):
        if not background == None:
            self.screen.blit(background, (0,0))


    def returnRandomBackground(self):
        BACKGROUND_DIRECTORY = os.path.join(os.path.dirname(__file__), '../../resource/images/menu/background/')
        try:
            randomPick = (os.path.join(os.path.dirname(__file__), BACKGROUND_DIRECTORY + random.choice(os.listdir(BACKGROUND_DIRECTORY))))
        except IndexError:
            # No backgrounds were found (for some reason)
            self.logger.error("No background images found")
            randomPick = None

        scaledImage = None
        if not randomPick == None:
            backgroundImage = pygame.image.load(randomPick).convert()
            scaledImage = pygame.transform.smoothscale(backgroundImage, (self.SCREEN_W, self.SCREEN_H))

        return scaledImage

    def playRandomMusic(self):
        # Pick a random song
        MUSIC_DIRECTORY = os.path.join(os.path.dirname(__file__), '../../resource/sound/menu/music/')
        try:
            randomPick = (os.path.join(os.path.dirname(__file__), MUSIC_DIRECTORY + random.choice(os.listdir(MUSIC_DIRECTORY))))
        except IndexError:
            # No music was found (for some reason)
            randomPick = None

        # Load the random song that was picked
        if not randomPick == None:
            self.logger.info("Playing track from file: " + randomPick)
            pygame.mixer.music.load(randomPick)
            pygame.mixer.music.play(-1) # Loop forever

    def addFooter(self):
        COVERAGE = 8
        BAR_COLOR = (53, 50, 45)

        pygame.draw.rect(self.screen, BAR_COLOR, (0, int(self.SCREEN_H - (self.SCREEN_H / COVERAGE)), self.SCREEN_W, int(self.SCREEN_H / COVERAGE)))

        font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../resource/fonts/tf2secondary.ttf'), ScaleUtility.scaleValue(36))
        text = font.render("Version " + self.version + " - made by /u/djfigs1", True, (119,107,95))

        self.screen.blit(text, ScaleUtility.scalePos(1375, 995))

    def mouseAction(self, state):
        touched = False
        for button in self.buttons:
            if button.isMouseTouching():
                if not state:
                    touched = True
                    self.logger.debug(button.text + " clicked")
                    self.buttonRelease.play()
                else:
                    self.buttonClick.play()
        if touched:
            if self.quitButton.isMouseTouching():
                pygame.quit()
            elif self.playButton.isMouseTouching():
                self.startGame = True
                self.logger.debug("TitleScreen start game enabled")
            elif self.supportButton.isMouseTouching():
                webbrowser.open("https://steamcommunity.com/tradeoffer/new/?partner=178459664&token=cQDpNvAs")
            elif self.settingsButton.isMouseTouching():
                self.testWindow.toggleOpen()
            else:
                self.FloatText.addText("That feature hasn't been implemented yet", 5, color=(255,85,85))
                self.buttonNotSupportedSound.play()


    def scaleResSurface(self, x, y, width, height):
        # 1920:1080  500, 250, 100, 50
        # 960:540 250, 125, 50, 25
        SCALE_BASE = (1920,1080)

        WIDTH_SCALE = float(SCALE_BASE[0]) / float(self.SCREEN_W)
        HEIGHT_SCALE = float(SCALE_BASE[1]) / float(self.SCREEN_H)

        scaled_X = int(float(x) / WIDTH_SCALE)
        scaled_Y = int(float(y) / HEIGHT_SCALE)
        scaled_width = int(float(width) / WIDTH_SCALE)
        scaled_height = int(float(height) / HEIGHT_SCALE)

        return (scaled_X, scaled_Y, scaled_width, scaled_height)
        

