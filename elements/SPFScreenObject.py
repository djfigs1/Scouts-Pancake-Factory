class SPFScreenObject(object):
    def __init__(self, surface):
        self.surface = surface
        self.x = 0
        self.y = 0
        self.testVariable = 0

    def blit(self):
        # Should be usedg only, should NOT update any values within the class.
        pass

    def update(self):
        # Should be used to update information within the object.
        pass