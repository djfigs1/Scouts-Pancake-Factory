import pygame, os
import elements.HUDElements.ScaleUtility as SU
import Physics

class SPFScout:
    def __init__(self, surface):
        self.runPoses = []
        self.surface = surface
        self.speed = 0
        self.frame = 0
        self.frameTime = 0
        self.right = True
        self.jumps = 0

        self.x = 0
        self.y = SU.scaleValue(750)
        self.vel = 0
        self.pos = 0

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

    def jump(self):
        if not self.jumps >= 2:
            self.vel = -300
            self.jumps += 1

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

    def update(self, clock, pause):
        if not pause:
            if not self.pos == 0 or not self.vel == 0:
                vel, pos = Physics.Gravity(256, self.pos, self.vel, float(clock.get_time()) / 1000.0)
                if (pos > 0):
                    pos = 0
                    vel = 0
                self.vel = vel
                self.y, self.pos = pos + SU.scaleValue(750), pos
            else:
                self.jumps = 0
                self.y = SU.scaleValue(750)
        self.blit(clock)
        self.setSpeed(0)

    def testObjectColosion(self, rect):
        scoutRect = self.getRect()
        if (scoutRect[0] >= rect[0] and scoutRect[0] <= rect[0] + rect[2] and rect[1] >= scoutRect[1] - rect[3] and scoutRect[1] + scoutRect[3] >= rect[1]):
            return True
        else:
            return False
