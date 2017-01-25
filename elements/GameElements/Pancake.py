import pygame, os, random

class SPFPancake:
    def __init__(self, surface, y=-random.randint(100, 300)):
        self.surface = surface
        self.pancake = pygame.image.load(os.path.join(os.path.dirname(__file__), '../../resource/images/game/pancake.png')).convert()
        self.pancake = pygame.transform.scale(self.pancake, (int(float(self.pancake.get_rect()[2]) / 2.5), int(float(self.pancake.get_rect()[3]) / 2.5)))
        self.pancake.set_colorkey((0,0,0))

        self.x = random.randint(0, 1920 - self.pancake.get_rect().width)
        self.y = y

        #Gravity in Feet/Second
        self.gravityAccel = -4
        self.prevVol = 0
        self.prevPos = 0

    def blit(self):
        self.surface.blit(self.pancake, (self.x,self.y))

    def gravityBlit(self, time):
        vel = -self.gravityAccel * float(time) / 1000.0 + self.prevVol
        pos = 0.5 * -self.gravityAccel * time**2 + vel*time + self.prevPos
        self.y += vel
        self.blit()
        self.prevPos = pos
        self.prevVol = vel

    def update(self, clock):
        self.gravityBlit(clock.get_time())

    def getRect(self):
        return (self.x, self.y, self.pancake.get_rect().width, self.pancake.get_rect().height)