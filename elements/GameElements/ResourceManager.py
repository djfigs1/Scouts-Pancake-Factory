import pygame, os
import elements.HUDElements.ScaleUtility as SU

textureDictionary = {}

def __init__():
    #region Pancake
    textureDictionary['pancake'] = pygame.image.load(os.path.join(os.path.dirname(__file__), '../../resource/images/game/pancake.png')).convert()
    textureDictionary['pancake'] = pygame.transform.scale(textureDictionary['pancake'], (int(float(textureDictionary['pancake'].get_rect()[2]) / 2.5), int(float(textureDictionary['pancake'].get_rect()[3]) / 2.5)))
    textureDictionary['pancake'] = pygame.transform.scale(textureDictionary['pancake'], SU.scalePos(246, 146))
    textureDictionary['pancake'].set_colorkey((0,0,0))
    #endregion