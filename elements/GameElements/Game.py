import logging
import os
import pygame
import random

import elements.ConfigUtility
import elements.HUDElements.ScaleUtility as SU
import ResourceManager
from elements.GameElements import SPFPancake
from elements.GameElements import SPFScout
from elements.GameElements.GameOverDoors import GameOverDoors
from elements.GameElements.GameStatsWindow import GameStatsWindow
from elements.GameElements.HUD.GameHUD import GameHUD
from elements.GameElements.HUD.PauseWindow import PauseWindow
from elements.GameElements.PickupItems.SpeedPowerup import SpeedPowerup
from elements.HUDElements.FloatText import FloatText


class Game:
    def __init__(self, screen):
        # INIT Variables.
        ResourceManager.__init__()
        self.screen = screen
        self.vol = elements.ConfigUtility.getConfigSetting("volume")
        self.scout = SPFScout(screen)
        self.speed = SU.scaleFloatValue(10)
        self.score = 0
        self.miss = 0
        self.gameOver = False
        self.endGame = False
        self.FloatText = FloatText(self.screen, 10)
        pygame.key.set_repeat(1,1)
        self.pancakes = [SPFPancake(self.screen), SPFPancake(self.screen), SPFPancake(self.screen)]
        self.powerups = []
        self.pointSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/game/hitsound.wav'))
        self.winSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/game/win_music.wav'))
        self.loseSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/game/lose_music.wav'))
        self.missSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/game/miss.wav'))
        self.pointSound.set_volume(self.vol)
        self.winSound.set_volume(self.vol)
        self.loseSound.set_volume(self.vol)
        self.missSound.set_volume(self.vol)
        self.levelBackground = pygame.transform.smoothscale(pygame.image.load(os.path.join(os.path.dirname(__file__), '../../resource/images/game/levels/background.png')).convert(), (pygame.display.Info().current_w, pygame.display.Info().current_h))
        self.windowSurf = pygame.Surface(SU.scalePos(650, 200))
        self.window = PauseWindow(self.windowSurf)
        self.window.setTitle("Paused")
        self.gameOverWindow = GameOverDoors(self.screen)
        self.gameOverStats = GameStatsWindow(self.screen)
        self.gameState = {}
        self.pause = False
        self.logger = logging.getLogger("spf")
        self.logger.info("Initializing Game")
        self.winScore = 100

        #region Joystick
        # Check if there's a connected joystick.
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except pygame.error:
            self.joystick = None

        if self.joystick != None:
            self.logger.info("Enabiling joystick in-game")
        #endregion

        self.testPowerup = SpeedPowerup(self.screen, self.scout)
        self.HUD = GameHUD(self.screen)

    def quit(self):
        pygame.mixer.stop()
        self.endGame = False
        pass

    def eventLoop(self, Clock):
        # Reset the Screen
        self.screen.fill((0,0,0))

        # Blit the Level Background
        self.screen.blit(self.levelBackground, (0,0))

        # Keep playing until the Player has reached a score of 20, or they've missed three pancakes.
        if (not self.pause):
            if (not self.score >= self.winScore and not self.miss >= 3):
                for powerup in self.powerups:
                    powerup.update(Clock)

                    if powerup.finished:
                        self.powerups.remove(powerup)

                for pancake in self.pancakes:
                    pancake.update(Clock)
                    pancakeRect = pancake.getRect()

                    if (self.scout.testObjectColosion(pancakeRect)):
                        self.pointSound.play()
                        self.pancakes.remove(pancake)
                        self.pancakes.append(SPFPancake(self.screen))
                        self.score += 1
                        if (random.randint(1, 20) == 20):
                            self.powerups.append(SpeedPowerup(self.screen, self.scout))
                    elif (pancakeRect[1] + pancakeRect[3] >= SU.scaleValue(1080)):
                        self.pancakes.remove(pancake)
                        self.pancakes.append(SPFPancake(self.screen))
                        # self.missSound.play()
            elif (not self.gameOver and self.score >= self.winScore and self.miss < 3):
                # If they won, meaning they got 20 pancakes, with no more than two misses.
                self.logger.info("Game victory")
                self.winSound.play()
                self.gameOverWindow.deploy()
                self.gameOverStats.deploy()
                self.gameOver = True
            elif (not self.gameOver and self.miss >= 3):
                # If they didn't fill the above requirement, they've lost the game.
                self.logger.info("Game defeat")
                self.loseSound.play()
                self.gameOver = True
                self.gameOverWindow.deploy()
                self.gameOverStats.deploy()
            elif (self.gameOver):
                # Draw the appropriate text.
                if (self.miss >= 3):
                    font = pygame.font.SysFont("TF2", SU.scaleValue(256))
                    text = font.render("YOU FAILED", True, (255, 0, 0))
                    text_w = text.get_rect().width
                    text_h = text.get_rect().height

                    self.screen.blit(text, ((SU.scaleValue(1920) / 2) - text_w / 2, SU.scaleValue(400) - text_h / 2))
                else:
                    font = pygame.font.SysFont("TF2", SU.scaleValue(256))
                    text = font.render("VICTORY", True, (0, 255, 0))
                    text_w = text.get_rect().width
                    text_h = text.get_rect().height

                    self.screen.blit(text, ((SU.scaleValue(1920) / 2) - text_w / 2, SU.scaleValue(400) - text_h / 2))
        else:
            if (not self.gameOver):
                for pancake in self.pancakes:
                    pancake.blit()

        # Update the Game State dictionary.
        self.gameState['score'] = self.score
        self.gameState['miss'] = self.miss
        self.gameState['FPS'] = Clock.get_fps()
        self.gameState['powerups'] = self.powerups
        self.gameState['time'] = Clock.get_time()

        # Update Classes
        self.scout.update(Clock, self.pause)
        self.gameOverWindow.update(Clock)
        self.gameOverStats.update(Clock)
        self.HUD.update(self.gameState)
        self.window.update((self.screen.get_rect().width / 2 - self.windowSurf.get_rect().width / 2,
                            self.screen.get_rect().height / 2 - self.windowSurf.get_rect().height / 2), self)
        self.FloatText.update()

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if not (self.pause):
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.scout.setSpeed(-self.speed)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.scout.setSpeed(self.speed)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.window.toggleOpen()
                    self.pause = not self.pause
                if event.key == pygame.K_SPACE:
                    self.scout.jump()


        # Handle joystick events ONLY IF there's a joystick initialized.
        if (self.joystick != None):
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            if self.joystick.get_hat(0)[0] > 0:
                self.scout.setSpeed(self.speed)
            elif self.joystick.get_hat(0)[0] < 0:
                self.scout.setSpeed(-self.speed)

        if (self.window.isOpen):
            self.screen.blit(self.windowSurf, (self.screen.get_rect().width / 2 - self.windowSurf.get_rect().width / 2, self.screen.get_rect().height / 2 - self.windowSurf.get_rect().height / 2))
        else:
            pygame.mouse.set_visible(False)

        pygame.display.update()