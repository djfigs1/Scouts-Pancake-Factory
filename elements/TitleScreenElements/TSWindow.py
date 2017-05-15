import pygame

class TSWindow(object):
    def __init__(self, surface):
        self.surfacce = surface
        self.isHidden = True
        self.x = 0
        self.y = 0

    def show(self):
        self.isHidden = False

    def hide(self):
        self.isHidden = True

    def blit(self):
        pass

    def update(self):
        pass