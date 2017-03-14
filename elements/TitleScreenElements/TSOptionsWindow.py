import pygame, TSButton, elements, elements.TitleScreenElements.TitleScreen, os
import elements.HUDElements.ScaleUtility as SU

class TSWindow:
    def __init__(self, surface):
        self.surface = surface
        self.menuColor = (53, 50, 45)
        self.menuBackgroundColor = (119,107,95)
        self.borderThickness = SU.scaleValue(5)
        self.textColor = (255,255,255)
        self.surface_w = surface.get_width()
        self.surface_h = surface.get_height()
        self.isOpen = False
        self.buttons = []
        if (elements.ConfigUtility.getConfigSetting("ts_music_enable")):
            self.button = TSButton.TSButton(surface, self.surface_w / 2 - SU.scaleValue(500) / 2, SU.scaleValue(100), SU.scaleValue(500), SU.scaleValue(50), "Music Enabled")
        else:
            self.button = TSButton.TSButton(surface, self.surface_w / 2 - SU.scaleValue(500) / 2, SU.scaleValue(100), SU.scaleValue(500), SU.scaleValue(50), "Music Disabled")
        self.buttons.append(self.button)

        self.fps_button = TSButton.TSButton(surface, self.surface_w / 2 - SU.scaleValue(500) / 2, SU.scaleValue(160), SU.scaleValue(500), SU.scaleValue(50), "FPS Counter")
        self.test_button = TSButton.TSButton(surface, self.surface_w / 2 - SU.scaleValue(500) / 2, SU.scaleValue(220), SU.scaleValue(500), SU.scaleValue(50), "Float Test")
        self.volume_down = TSButton.TSButton(surface, self.surface_w / 2 - SU.scaleValue(500) / 2, SU.scaleValue(280), SU.scaleValue(100), SU.scaleValue(50), "-")
        self.volume_up = TSButton.TSButton(surface, self.surface_w / 2 + SU.scaleValue(150), SU.scaleValue(280), SU.scaleValue(100), SU.scaleValue(50), "+")
        self.close_button = TSButton.TSButton(surface, self.surface_w / 2 - SU.scaleValue(250) / 2, self.surface_h - self.surface_h / 10, SU.scaleValue(250), SU.scaleValue(50), "Exit", footerButton=True)
        self.buttons.append(self.fps_button)
        self.buttons.append(self.test_button)
        self.buttons.append(self.close_button)
        self.buttons.append(self.volume_down)
        self.buttons.append(self.volume_up)
        self.vol = elements.ConfigUtility.getConfigSetting("volume")

        self.title = ""
        self.mouseClick = False
        self.FONT_SIZE = SU.scaleValue(60)
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../resource/fonts/tf2build.ttf'), self.FONT_SIZE)

    def setTitle(self, title):
        self.title = title

    def blit(self):
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        self.surface.fill(self.menuBackgroundColor)
        pygame.draw.rect(self.surface, self.menuColor, (self.borderThickness, self.borderThickness, self.surface_w - self.borderThickness * 2, self.surface_h - self.borderThickness * 2))
        text = self.font.render(self.title, True, self.textColor)
        text_w = text.get_rect().width
        self.surface.blit(text, ((self.surface_w / 2) - text_w / 2, self.surface_h / 32))

    def update(self, xy, instance):
        if self.isOpen:
            self.blit()
            self.blitVolumeSlider(SU.scaleValue(280))

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
                elif (button == self.close_button):
                    self.isOpen = False
                elif (button == self.volume_down):
                    vol = pygame.mixer.music.get_volume()
                    vol -= 0.1
                    if vol < 0:
                        vol = 0
                    pygame.mixer.music.set_volume(vol)
                    self.vol = vol
                    elements.ConfigUtility.writeConfigSetting("volume", vol)
                elif (button == self.volume_up):
                    vol = pygame.mixer.music.get_volume()
                    vol += 0.1
                    if vol > 1:
                        vol = 1
                    else:
                        vol = round(vol, 2)
                    pygame.mixer.music.set_volume(vol)
                    self.vol = vol
                    elements.ConfigUtility.writeConfigSetting("volume", vol)


            button.setVisible(self.isOpen)
            button.updateButton(xOffset=-xy[0], yOffset=-xy[1])
        self.mouseClick = pygame.mouse.get_pressed()[0]

    def open(self):
        self.isOpen = True

    def close(self):
        self.isOpen = False

    def toggleOpen(self):
        self.isOpen = not self.isOpen

    def blitVolumeSlider(self, y):
        pygame.draw.rect(self.surface, (100, 100, 100), (self.surface_w / 2 - SU.scaleValue(500) / 2 + SU.scaleValue(107), y, SU.scaleValue(285), SU.scaleValue(50)))
        pygame.draw.rect(self.surface, (255, 255, 255), (self.surface_w / 2 - SU.scaleValue(500) / 2 + SU.scaleValue(107), y, SU.scaleValue(285) * self.vol, SU.scaleValue(50)))
