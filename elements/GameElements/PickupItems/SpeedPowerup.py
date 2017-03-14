import pygame, os, random
import elements.HUDElements.ScaleUtility as SU
import elements.ConfigUtility

class SpeedPowerup:

    def __init__(self, surface, scout):
        self.surface = surface
        self.scout = scout
        self.powerTime = 0
        self.visible = True
        self.vol = elements.ConfigUtility.getConfigSetting("volume")
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '../../../resource/images/game/powerup/speed.png')).convert()
        self.image = pygame.transform.smoothscale(self.image, SU.scalePos(self.image.get_rect().width, self.image.get_rect().height))
        self.startSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../../resource/sound/game/powerupStart.wav'))
        self.endSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../../resource/sound/game/powerupEnd.wav'))
        self.startSound.set_volume(self.vol)
        self.endSound.set_volume(self.vol)
        self.finished = False

        self.x, self.y = 0, 0
        self.x, self.y = random.randint(0, SU.scaleValue(1920) - self.getRect()[2]), -random.randint(SU.scaleValue(100), SU.scaleValue(300))

        #Gravity in Feet/Second
        self.gravityAccel = SU.scaleFloatValue(-4)
        self.prevVol = 0
        self.prevPos = 0

    def applyPowerup(self):
        speedMultiplier = 0
        if self.scout.getSpeed() > 0:
            speedMultiplier = 4
        elif self.scout.getSpeed() < 0:
            speedMultiplier = -4
        self.scout.setSpeed(self.scout.getSpeed() + SU.scaleValue(speedMultiplier))

    def gravityBlit(self, time):
        vel = -self.gravityAccel * float(time) / 1000.0 + self.prevVol
        pos = 0.5 * -self.gravityAccel * time**2 + vel*time + self.prevPos
        self.y += vel
        self.blit()
        self.prevPos = pos
        self.prevVol = vel

    def blit(self):
        self.surface.blit(self.image, (self.x,self.y))

    def getRect(self):
        return (self.x, self.y, self.image.get_rect()[2], self.image.get_rect()[3])


    def update(self, clock):
        if (self.visible):
            self.gravityBlit(clock.get_time())
            if (self.scout.testObjectColosion(self.getRect())):
                # The scout has picked up the powerup.
                self.visible = False
                self.startSound.play()
            if (self.y >= SU.scaleValue(1080)):
                self.finished = True
        else:
            self.powerTime += clock.get_time()
            if self.powerTime > 10000:
                # If the powerup buff has lasted for more than 10 seconds, remove it.
                self.endSound.play()
                self.finished = True
            else:
                self.applyPowerup()

    def finished(self):
        return self.finished