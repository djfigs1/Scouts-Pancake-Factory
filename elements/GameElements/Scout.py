import pygame, os
import elements.HUDElements.ScaleUtility as SU

class SPFScout:
    def __init__(self, surface):
        self.runPoses = []
        self.surface = surface
        self.speed = 0
        self.frame = 0
        self.frameTime = 0
        self.right = True

        self.x = 0
        self.y = SU.scaleValue(750)

        self.loadTextures()

    def loadTextures(self):
        RUN_DIRECTORY = os.path.join(os.path.dirname(__file__), '../../resource/images/run/')
        items = len(os.listdir(RUN_DIRECTORY))

        for x in range(0, items):
            self.runPoses.append(pygame.image.load(os.path.join(os.path.dirname(__file__), RUN_DIRECTORY + "run" + str(x) + ".png")).convert())
            rect = self.runPoses[x].get_rect()
            self.runPoses[x] = pygame.transform.scale(self.runPoses[x], (int(float(rect[2]) / 4.0), int(float(rect[3]) / 4.0)))
            self.runPoses[x] = pygame.transform.scale(self.runPoses[x], SU.scalePos(self.runPoses[x].get_rect().width, self.runPoses[x].get_rect().height))
            self.runPoses[x].set_colorkey((0,255,0))

    def getRect(self):
        return (self.x, self.y, self.runPoses[self.frame].get_rect()[2], self.runPoses[self.frame].get_rect()[3])

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

        if speed > 0:
            self.right = True
        elif speed < 0:
            self.right = False

    def blit(self, clock):
        self.frameTime += clock.get_time()
        rect = self.runPoses[self.frame].get_rect()

        if (self.right):
            self.surface.blit(self.runPoses[self.frame], (self.x - int(float(rect[2]) / 2.0), self.y))
        else:
            self.surface.blit(pygame.transform.flip(self.runPoses[self.frame], True, False), (self.x - int(float(rect[2]) / 2.0), self.y))
        if (self.speed != 0):
            self.x += self.speed
            if self.frameTime >= (1000 / 24):
                self.frameTime = 0
                self.frame += 1
                if self.frame >= 10:
                    self.frame = 0
        else:
            self.frame = 10

    def testObjectColosion(self, rect):
        scoutRect = self.getRect()
        if (scoutRect[0] >= rect[0] and scoutRect[0] <= rect[0] + rect[2] and rect[1] >= scoutRect[1] - rect[3] and scoutRect[1] + scoutRect[3] >= rect[1]):
            return True
        else:
            return False
