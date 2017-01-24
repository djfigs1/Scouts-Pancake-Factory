import pygame, TSButton, elements, elements.TitleScreenElements.TitleScreen, os

class TSWindow:
    def __init__(self, surface):
        self.surface = surface
        self.menuColor = (53, 50, 45)
        self.menuBackgroundColor = (119,107,95)
        self.borderThickness = 5
        self.textColor = (255,255,255)
        self.surface_w = surface.get_width()
        self.surface_h = surface.get_height()
        self.isOpen = False
        self.buttons = []
        if (elements.ConfigUtility.getConfigSetting("ts_music_enable")):
            self.button = TSButton.TSButton(surface, self.surface_w / 2 - 500 / 2, 100, 500, 50, "Music Enabled")
        else:
            self.button = TSButton.TSButton(surface, self.surface_w / 2 - 500 / 2, 100, 500, 50, "Music Disabled")
        self.buttons.append(self.button)

        self.fps_button = TSButton.TSButton(surface, self.surface_w / 2 - 500 / 2, 160, 500, 50, "FPS Counter")
        self.test_button = TSButton.TSButton(surface, self.surface_w / 2 - 500 / 2, 220, 500, 50, "Float Test")
        self.buttons.append(self.fps_button)
        self.buttons.append(self.test_button)

        self.title = ""
        self.mouseClick = False
        self.FONT_SIZE = 60

    def setTitle(self, title):
        self.title = title

    def blit(self):
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        self.surface.fill(self.menuBackgroundColor)
        pygame.draw.rect(self.surface, self.menuColor, (self.borderThickness, self.borderThickness, self.surface_w - self.borderThickness * 2, self.surface_h - self.borderThickness * 2))

        font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../resource/fonts/tf2build.ttf'), self.FONT_SIZE)
        text = font.render(self.title, True, self.textColor)
        text_w = text.get_rect().width

        self.surface.blit(text, ((self.surface_w / 2) - text_w / 2, self.surface_h / 32))

    def update(self, xy, instance):
        if self.isOpen:
            self.blit()

        for button in self.buttons:
            if (button.isMouseTouching(xOffset=-xy[0], yOffset=-xy[1])) and not pygame.mouse.get_pressed()[0] and self.mouseClick and self.isOpen:
                if (button == self.fps_button):
                    instance.showFPS = not instance.showFPS
                    elements.ConfigUtility.writeConfigSetting("fps_counter", instance.showFPS)
                elif (button == self.button):
                    if (self.button.isMouseTouching(xOffset=-xy[0], yOffset=-xy[1])) and not pygame.mouse.get_pressed()[
                        0] and self.mouseClick:
                        enabled = elements.ConfigUtility.getConfigSetting("ts_music_enable")
                        if (enabled):
                            self.button.text = "Music Disabled"
                            pygame.mixer.music.stop()
                        else:
                            self.button.text = "Music Enabled"
                            instance.playRandomMusic()
                        elements.ConfigUtility.writeConfigSetting("ts_music_enable", not enabled)
                elif (button == self.test_button):
                    instance.FloatText.addText("--- TESTING ---", 5)

            button.setVisible(self.isOpen)
            button.updateButton(xOffset=-xy[0], yOffset=-xy[1])
        self.mouseClick = pygame.mouse.get_pressed()[0]

    def open(self):
        self.isOpen = True

    def close(self):
        self.isOpen = False

    def toggleOpen(self):
        self.isOpen = not self.isOpen