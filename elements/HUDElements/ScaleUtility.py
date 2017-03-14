import pygame

def scaleResSurface(x, y, width, height):
    SCALE_BASE = (1920, 1080)
    SCREEN_W = pygame.display.Info().current_w
    SCREEN_H = pygame.display.Info().current_h

    scaled_X = int(float(x) / float(SCALE_BASE[0]) * float(SCREEN_W))
    scaled_Y = int(float(y) / float(SCALE_BASE[1]) * float(SCREEN_H))
    scaled_width = int(float(width) / float(SCALE_BASE[0]) * float(SCREEN_W))
    scaled_height = int(float(height) / float(SCALE_BASE[1]) * float(SCREEN_H))

    return (scaled_X, scaled_Y, scaled_width, scaled_height)

def scaleValue(value):
    SCALE_BASE = (1920, 1080)
    SCREEN_W = pygame.display.Info().current_w
    SCREEN_H = pygame.display.Info().current_h

    scaled_Value = int(float(value) / float(SCALE_BASE[0]) * float(SCREEN_W))

    return scaled_Value

def scaleFloatValue(value):
    SCALE_BASE = (1920, 1080)
    SCREEN_W = pygame.display.Info().current_w
    SCREEN_H = pygame.display.Info().current_h

    scaled_Value = float(value) / float(SCALE_BASE[0]) * float(SCREEN_W)

    return scaled_Value

def scalePos(x,y):
    SCALE_BASE = (1920, 1080)
    SCREEN_W = pygame.display.Info().current_w
    SCREEN_H = pygame.display.Info().current_h

    scaled_X = int(float(x) / float(SCALE_BASE[0]) * float(SCREEN_W))
    scaled_Y = int(float(y) / float(SCALE_BASE[1]) * float(SCREEN_H))

    return (scaled_X, scaled_Y)

def scaleMouse():
    SCALE_BASE = (1920, 1080)
    SCREEN_W = pygame.display.Info().current_w
    SCREEN_H = pygame.display.Info().current_h

    mouse_X = pygame.mouse.get_pos()[0]
    mouse_Y = pygame.mosue.get_pos()[1]

    scaled_X = int(float(mouse_X) / float(SCREEN_W) * float(SCALE_BASE[0]))
    scaled_Y = int(float(mouse_Y) / float(SCREEN_H) * float(SCALE_BASE[1]))

    return (scaled_X, scaled_Y)

def centerHorizontally(width):
    return scaleValue(1920) / 2 - width / 2

def centerVertically(height):
    return scaleValue(1080) / 2 - height / 2