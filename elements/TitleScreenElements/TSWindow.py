import pygame

class TSWindow:
    def __init__(self, surface):
        self.surface = surface
        self.menuColor = (0,0,0)
        self.surface_w = surface.get_width()
        self.surface_h = surface.get_height()
        self.isOpen = False
        self.title = ""

    def setTitle(self, title):
        self.title = title

    def blit(self):
        self.surface.fill((53, 50, 45))

    def update(self):
        if self.isOpen:
            self.blit()

    def open(self):
        self.isOpen = True

    def close(self):
        self.isOpen = False

    def toggleOpen(self):
        self.isOpen = not self.isOpen