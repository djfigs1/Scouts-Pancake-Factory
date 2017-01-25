import pygame, os, random

class SpeedPowerup:

    def __init__(self, surface, scout):
        self.surface = surface
        self.scout = scout
        self.powerTime = 0
        self.visible = True
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '../../resource/images/game/powerup/speed.png')).convert()
        self.startSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/game/powerupStart.wav'))
        self.endSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/game/powerupEnd.wav'))
        self.finished = False

        self.x, self.y = 0, 0
        self.x, self.y = random.randint(0, 1920 - self.getRect()[2]), 800

    def applyPowerup(self):
        speedMultiplier = 0
        if self.scout.getSpeed() > 0:
            speedMultiplier = 4
        elif self.scout.getSpeed() < 0:
            speedMultiplier = -4
        self.scout.setSpeed(self.scout.getSpeed() + speedMultiplier)

    def blit(self, x, y):
        self.x = x
        self.y = y
        self.surface.blit(self.image, (x,y))

    def getRect(self):
        return (self.x, self.y, self.image.get_rect()[2], self.image.get_rect()[3])


    def update(self, clock):
        if (self.visible):
            self.blit(self.x, self.y)
            if (self.scout.testObjectColosion(self.getRect())):
                # The scout has picked up the powerup.
                self.visible = False
                self.startSound.play()
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

