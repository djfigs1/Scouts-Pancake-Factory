import pygame, os
from elements.TitleScreenElements.TSButton import TSButton

class TSButtonContainer:

    def __init__(self, screen, text, buttons, padding, button_padding, x, y, width, height):
        self.screen = screen
        self.text = text
        self.buttons = buttons
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.padding = padding
        self.button_padding = button_padding
        self.TITLE_TEXT_OFFSET = 50

        self.y_offset = self.y + self.TITLE_TEXT_OFFSET

        self.BACKGROUND_COLOR = (53, 50, 45)
        self.TEXT_COLOR = (245,234,212)

        self.drawBackground()
        self.fitButtons()

    def drawBackground(self):
        if not self.text == "":
            font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../resource/fonts/tf2build.ttf'), 36)
            text = font.render(self.text, True, (self.TEXT_COLOR))
            text_h = text.get_rect().height

            pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (self.x, self.y, self.width, self.TITLE_TEXT_OFFSET))
            self.screen.blit(text, (self.x + self.padding[0] + self.button_padding / 2, (self.y + (self.TITLE_TEXT_OFFSET + self.padding[1]) / 2) - text_h / 2))

        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (self.x, self.y_offset, self.width, self.height))

    def fitButtons(self):
        if isinstance(self.buttons, TSButton):
            num_of_buttons = 1
            self.buttons = [self.buttons]
        else:
            num_of_buttons = len(self.buttons)

        box_x = self.x + self.padding[0]
        box_width = self.width - (self.padding[0] * 2)
        box_y = self.y_offset + self.padding[1]
        box_height = self.height - (self.padding[1] * 2)
        button_width = (box_width - num_of_buttons * self.button_padding) / num_of_buttons

        x = 0
        for button in self.buttons:
            button.height = box_height
            button.width = button_width
            button.x = (box_x + self.button_padding / 2) + button_width * x + self.button_padding * x
            button.y = box_y
            x += 1

