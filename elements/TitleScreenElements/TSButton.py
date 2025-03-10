import os, pygame
import elements.HUDElements.ScaleUtility as SU

class TSButton:
    def __init__(self, surface, x, y, width, height, text, footerButton=False, soundEffects=True):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.visible = True
        self.footerButton = footerButton
        self.soundEffects = soundEffects

        self.TEXT_COLOR = (74, 69, 60)
        self.BUTTON_COLOR = (245,234,212)
        self.HIGHLIGHT_COLOR = (127,63,51)
        self.F_BUTTON_COLOR = (119,107,95)
        self.F_HIGHLIGHT_COLOR = (74,69,60)
        self.F_TEXT_COLOR = (119,107,95)
        self.touched = False

        self.FONT_SIZE = SU.scaleValue(36)

        self.color = self.BUTTON_COLOR
        self.textColor = self.TEXT_COLOR

        self.ROLLOVER = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/menu/buttonrollover.wav'))
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../resource/fonts/tf2build.ttf'),
                                        self.FONT_SIZE)

    def updateButton(self, xOffset=0, yOffset=0):
        if (self.visible):
            if self.isMouseTouching(xOffset=xOffset, yOffset=yOffset):
                if (self.footerButton):
                    self.color = self.BUTTON_COLOR
                    self.textColor = self.F_BUTTON_COLOR
                else:
                    self.color = self.HIGHLIGHT_COLOR
                    self.textColor = self.BUTTON_COLOR

                if not self.touched and self.soundEffects:
                    self.ROLLOVER.play()
                    self.touched = True
            else:
                if (self.footerButton):
                    self.color = self.F_BUTTON_COLOR
                    self.textColor = self.BUTTON_COLOR
                else:
                    self.color = self.BUTTON_COLOR
                    self.textColor = self.TEXT_COLOR

                if self.touched and self.soundEffects:
                    self.touched = False
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))

            if not self.text == "":
                
                text = self.font.render(self.text, True, self.textColor)
                text_w = text.get_rect().width
                text_h = text.get_rect().height

                self.surface.blit(text,
                                  ((self.x + self.width / 2) - text_w / 2, (self.y + self.height / 2) - text_h / 2 + 2))




    def isMouseTouching(self, xOffset=0, yOffset=0):
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        # if mouseX >= self.x and mouseX <= self.x + self.width:
        #     if mouseY >= self.y and mouseY <= self.y + self.height:
        #         return True

        if (self.rect.collidepoint(mouseX + xOffset, mouseY + yOffset)):
            return True

        return False

    def setVisible(self, vis):
        self.visible = vis
