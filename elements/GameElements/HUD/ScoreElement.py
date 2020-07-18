import pygame, os
import elements.HUDElements.ScaleUtility as SU

class Score:
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../../resource/fonts/tf2build.ttf'), SU.scaleValue(128))
        self.secondaryFont = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../../resource/fonts/tf2build.ttf'), SU.scaleValue(80))

        self.x, self.y = SU.scalePos(50, 25)

    def blit(self, score, miss):
        pygame.draw.circle(self.surface, (244, 161, 66), (0,int(self.surface.get_rect().height / 2)), int(SU.scaleValue(200)))
        scoreText = self.font.render(str(score), True, (255,255,255))
        # missText = self.secondaryFont.render(str(miss), True, (255,0,0)
        self.surface.blit(scoreText, (self.x, self.y))
        # self.surface.blit(missText, (self.x + 150, self.y + 50))

    def update(self, gameState):
        score = gameState['score']
        miss = gameState['miss']
        self.blit (score, miss)
        pass
