import pygame, elements, elements.TitleScreenElements.TitleScreen, os
from elements.TitleScreenElements.TSButton import TSButton
import elements.HUDElements.ScaleUtility as SU

class PauseWindow:
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

        self.menuexit_button = TSButton(surface, self.surface_w / 2 - SU.scaleValue(500) / 2, SU.scaleValue(75), SU.scaleValue(500), SU.scaleValue(50), "Exit to Menu")
        self.exit_button = TSButton(surface, self.surface_w / 2 - SU.scaleValue(250) / 2, self.surface_h - SU.scaleValue(50), SU.scaleValue(250), SU.scaleValue(50), "Resume", footerButton=True)
        self.buttons.append(self.exit_button)
        self.buttons.append(self.menuexit_button)



        self.title = ""
        self.mouseClick = False
        self.FONT_SIZE = SU.scaleValue(60)
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../../resource/fonts/tf2build.ttf'),
                                     self.FONT_SIZE)

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
        for button in self.buttons:
            if (button.isMouseTouching(xOffset=-xy[0], yOffset=-xy[1])) and not pygame.mouse.get_pressed()[0] and self.mouseClick and self.isOpen:
                if (button == self.exit_button):
                    self.close()
                    instance.pause = False
                elif (button == self.menuexit_button):
                    instance.endGame = True
                    self.close()


            button.setVisible(self.isOpen)
            button.updateButton(xOffset=-xy[0], yOffset=-xy[1])
        self.mouseClick = pygame.mouse.get_pressed()[0]

    def open(self):
        self.isOpen = True

    def close(self):
        self.isOpen = False

    def toggleOpen(self):
        self.isOpen = not self.isOpen
        if (self.isOpen):
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)