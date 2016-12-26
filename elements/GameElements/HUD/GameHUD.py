import pygame, os
from elements.GameElements.HUD import *

class GameHUD:
    def __init__(self, surface):
        self.surface = surface
        self.SCREEN_W = pygame.display.Info().current_w
        self.SCREEN_H = pygame.display.Info().current_h

        self.footerSurface = pygame.Surface((self.SCREEN_W, int(self.SCREEN_H / 7)))
        self.hudElements = []

        self.addHUDElement(Score(self.footerSurface))
        self.addHUDElement(Powerup(self.footerSurface))
        self.addHUDElement(FPS(self.footerSurface))

    def drawBase(self):
        self.footerSurface.fill((0, 0, 0))
        COVERAGE = 7
        BAR_COLOR = (53, 50, 45)
        pygame.draw.rect(self.footerSurface, BAR_COLOR, (0, 0, self.footerSurface.get_width(), self.footerSurface.get_height()))

    def addHUDElement(self, element):
        self.hudElements.append(element)

    def update(self, gameState):
        self.drawBase()
        for element in self.hudElements:
            element.update(gameState)
        self.surface.blit(self.footerSurface, (0, int(self.SCREEN_H - (self.SCREEN_H / 7))))