import pygame, os

class SPFPancake:
    def __init__(self, surface, x=0, y=150):
        self.surface = surface
        self.x = x
        self.y = y
        self.pancake = pygame.image.load(os.path.join(os.path.dirname(__file__), '../../resource/images/game/pancake.png')).convert()
        self.pancake = pygame.transform.scale(self.pancake, (int(float(self.pancake.get_rect()[2]) / 2.5), int(float(self.pancake.get_rect()[3]) / 2.5)))
        self.pancake.set_colorkey((0,0,0))

    def blit(self, x, y):
        self.x = x
        self.y = y

        self.surface.blit(self.pancake, (self.x,self.y))

    def getRect(self):
        return (self.x, self.y, self.pancake.get_rect()[2], self.pancake.get_rect()[3])