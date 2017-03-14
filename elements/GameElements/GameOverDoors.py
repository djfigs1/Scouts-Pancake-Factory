import pygame, os
import elements.HUDElements.ScaleUtility as SU

class GameOverDoors:

    def __init__(self, surface):
        self.surface = surface
        self.timeTilDeploy = 5000
        self.isDeployed = False
        self.width = 0
        self.height = pygame.display.Info().current_h
        self.speed = 15
        self.increment = 20
        self.deployTime = 0
        self.accumTime = 0
        self.color = (255,0,0)

        self.imageDoor = pygame.image.load(os.path.join(os.path.dirname(__file__), '../../resource/images/game/spf_gameover_door.png')).convert()
        self.imageDoor = pygame.transform.smoothscale(self.imageDoor, SU.scalePos(self.imageDoor.get_rect().width, self.imageDoor.get_rect().height))
        
        self.imageLogo = pygame.image.load(os.path.join(os.path.dirname(__file__), '../../resource/images/game/spf_gameover_logo.png'))
        self.imageLogo = pygame.transform.smoothscale(self.imageLogo, SU.scalePos(self.imageLogo.get_rect().width, self.imageLogo.get_rect().height))

        self.flippedDoor = pygame.transform.flip(self.imageDoor, True, False)

    def deploy(self):
        self.isDeployed = True

    def blit(self):
        if (not self.width >= SU.scaleValue(1920) / 2):
            if (self.accumTime >= self.speed):
                self.accumTime = 0
                self.width += SU.scaleValue(self.increment)
            if (self.width >= SU.scaleValue(1920) / 2):
                slam = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/game/mm_door_close.wav'))
                slam.play()


        #pygame.draw.rect(self.surface, self.color, (0, 0, self.width, self.height))
        #.draw.rect(self.surface, self.color, (SU.scaleValue(1920) - self.width, 0, self.width, self.height))
        self.surface.blit(self.imageDoor, (self.width-self.imageDoor.get_rect().width,0))
        self.surface.blit(self.flippedDoor, (SU.scaleValue(1920) - self.width, 0))
        #self.surface.blit(self.imageLogo, (self.width-self.imageDoor.get_rect().width,SU.scaleValue(1080) / 2 - self.imageLogo.get_rect().height / 2))

    def update(self, clock):
        if (self.isDeployed):
            self.accumTime += clock.get_time()
            if (self.deployTime >= self.timeTilDeploy):
                self.blit()
            else:
                self.deployTime += clock.get_time()
