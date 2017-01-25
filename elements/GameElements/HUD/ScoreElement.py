import pygame, os

class Score:
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../../resource/fonts/tf2build.ttf'), 128)
        self.secondaryFont = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../../resource/fonts/tf2build.ttf'), 80)

        self.x, self.y = 50, 25

    def blit(self, score, miss):
        scoreText = self.font.render(str(score), True, (255,255,255))
        # missText = self.secondaryFont.render(str(miss), True, (255,0,0))
        self.surface.blit(scoreText, (self.x, self.y))
        # self.surface.blit(missText, (self.x + 150, self.y + 50))

    def update(self, gameState):
        score = gameState['score']
        miss = gameState['miss']
        self.blit (score, miss)
        pass