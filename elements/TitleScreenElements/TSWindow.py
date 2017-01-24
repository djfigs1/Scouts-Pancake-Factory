import pygame, TSButton, elements

class TSWindow:
    def __init__(self, surface):
        self.surface = surface
        self.menuColor = (0,0,0)
        self.surface_w = surface.get_width()
        self.surface_h = surface.get_height()
        self.isOpen = False
        self.button = TSButton.TSButton(surface, 100, 100, 500, 50, "Music")
        self.title = ""
        self.mouseClick = False

    def setTitle(self, title):
        self.title = title

    def blit(self):
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        self.surface.fill((53, 50, 45))

    def update(self, xy):
        self.button.setVisible(self.isOpen)
        if self.isOpen:
            self.blit()
            if (self.button.isMouseTouching(xOffset=-xy[0], yOffset=-xy[1])) and not pygame.mouse.get_pressed()[0] and self.mouseClick:
                enabled = elements.ConfigUtility.getConfigSetting("ts_music_enable")
                if (enabled):
                    self.button.text = "Music Disabled"
                else:
                    self.button.text = "Music Enabled"
                elements.ConfigUtility.writeConfigSetting("ts_music_enable", not enabled)

            self.mouseClick = pygame.mouse.get_pressed()[0]

        self.button.updateButton(xOffset=-xy[0], yOffset=-xy[1])

    def open(self):
        self.isOpen = True

    def close(self):
        self.isOpen = False

    def toggleOpen(self):
        self.isOpen = not self.isOpen