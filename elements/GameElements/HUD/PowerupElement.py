import pygame, os
import elements.HUDElements.ScaleUtility as SU

class Powerup:
    def __init__(self, surface):
        self.surface = surface
        self.x, self.y = SU.scalePos(1000, 25)
        self.aTime = 0
        self.color = 200
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '../../../resource/fonts/tf2build.ttf'), SU.scaleValue(40))

    def blit(self):
        pass

    def update(self, gamestate):
        try:
            powerups = gamestate['powerups']
            valid = True
        except KeyError:
            valid = False

        self.blit()

        if valid:
            if len(powerups) > 0:
                for powerup in powerups:
                    if not powerup.visible:
                        time = powerup.powerTime
                        text = self.font.render("POWERUP", True, (255,255,255))
                        percentTime = float(time) / 10000.0
                        pygame.draw.rect(self.surface, (100,100,100), (self.x, self.surface.get_rect()[3] / 2 - 25, 800, 50))
                        pygame.draw.rect(self.surface, (255,255,255), (self.x, self.surface.get_rect()[3] / 2 - 25, 800 - int(800.0 * percentTime), 50))
                        self.surface.blit(text, (self.x + 800 / 2 - text.get_width() / 2, self.surface.get_rect()[3] / 2 - text.get_height() / 2 - 45))