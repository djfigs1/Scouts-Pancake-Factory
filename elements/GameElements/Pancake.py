import pygame, os, random
import elements.HUDElements.ScaleUtility as SU
import ResourceManager
import Physics
from elements.SPFScreenObject import SPFScreenObject


class SPFPancake(SPFScreenObject):
    def __init__(self, surface):
        SPFScreenObject.__init__(self, surface)
        self.surface = surface
        self.pancake = ResourceManager.textureDictionary['pancake']
        self.x = random.randint(0, SU.scaleValue(1920) - self.pancake.get_rect().width)
        self.y = -random.randint(self.pancake.get_rect().height, SU.scaleValue(300))

        #Gravity in Feet/Second
        self.gravityAccel = SU.scaleFloatValue(128)
        self.prevVol = 0
        self.prevPos = self.y

    def blit(self):
        self.surface.blit(self.pancake, (self.x,self.y))

    def gravityBlit(self, time):
        mTime = float(time) / 1000.0
        vel = self.gravityAccel * mTime + self.prevVol
        pos = 0.5 * self.gravityAccel * (mTime**2) + vel*mTime+ self.prevPos
        self.y = pos
        self.blit()
        self.prevPos = pos
        self.prevVol = vel

    def update(self, clock):
        vel, pos = Physics.Gravity(self.gravityAccel, self.prevPos, self.prevVol, float(clock.get_time()) / 1000.0)
        self.prevVol, self.prevPos = vel, pos
        self.y = self.prevPos
        self.blit()

    def getRect(self):
        return (self.x, self.y, self.pancake.get_rect().width, self.pancake.get_rect().height)