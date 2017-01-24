import pygame, time, os

class FloatText:
    def __init__(self, surface, y):
        self.texts = []
        self.surface = surface
        self.y = y
        self.FONT_SIZE = 24

        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../resource/fonts/tf2build.ttf'),
                                    self.FONT_SIZE)

    def addText(self, text, display_time, color=(255,255,255)):
        textDict = {}
        textDict['text'] = text
        textDict['time'] = time.time() + display_time
        textDict['color'] = color
        self.texts.append(textDict)

    def blit(self):
        y = self.y
        for text in self.texts:
            text = self.font.render(text['text'], True, text['color'])
            self.surface.blit(text, (self.surface.get_rect().width - text.get_rect().width - 10, y))
            y += 30


    def update(self):
        current_time = time.time()
        for text in self.texts:
            if (current_time >= text['time']):
                self.texts.remove(text)
        self.blit()