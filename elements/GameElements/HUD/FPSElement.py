import pygame, os

class FPS:
    def __init__(self,surface):
        self.surface = surface
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../../resource/fonts/tf2secondary.ttf'), 80)

    def update(self, gamestate):
        fps = gamestate['FPS']
        text = self.font.render(str(int(fps)), True, (255,255,255))

        self.surface.blit(text, (500, self.surface.get_height() / 2 - text.get_height() / 2))