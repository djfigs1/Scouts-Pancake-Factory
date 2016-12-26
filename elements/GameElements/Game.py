from elements.GameElements import SPFScout
from elements.GameElements import SPFPancake
from elements.GameElements.SpeedPowerup import SpeedPowerup
from elements.GameElements.HUD.GameHUD import GameHUD
import pygame, os, random

class Game:
    def __init__(self, screen):
        # INIT Variables.
        self.screen = screen
        self.scout = SPFScout(screen)
        self.speed = 10
        self.score = 0
        self.miss = 0
        self.gameOver = False
        pygame.key.set_repeat(1,1)
        self.pancakes = [SPFPancake(self.screen, x=500, y=300)]
        self.powerups = [SpeedPowerup(self.screen, self.scout)]
        self.pointSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/game/hitsound.wav'))
        self.winSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/game/win_music.wav'))
        self.loseSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/game/lose_music.wav'))
        self.missSound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '../../resource/sound/game/miss.wav'))
        self.levelBackground = pygame.image.load(os.path.join(os.path.dirname(__file__), '../../resource/images/game/levels/background.png')).convert()
        self.gameState = {}
        self.pause = False

        # Check if there's a connected joystick.
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except pygame.error:
            self.joystick = None

        self.testPowerup = SpeedPowerup(self.screen, self.scout)
        self.HUD = GameHUD(self.screen)

    def eventLoop(self, Clock):
        pygame.mouse.set_visible(False)
        # Reset the Screen
        self.screen.fill((0,0,0))

        # Blit the Level Background
        self.screen.blit(self.levelBackground, (0,0))

        # Keep playing until the Player has reached a score of 20, or they've missed three pancakes.
        if (not self.score >= 20 and not self.miss >= 3):
            for powerup in self.powerups:
                powerup.update(Clock)

                if powerup.finished:
                    self.powerups.remove(powerup)

            for pancake in self.pancakes:
                pancake.blit(pancake.x, pancake.y + 5)
                pancakeRect = pancake.getRect()

                if (self.scout.testObjectColosion(pancakeRect)):
                    self.pointSound.play()
                    self.pancakes.remove(pancake)
                    self.pancakes.append(SPFPancake(self.screen, x=random.randint(0, 1920 - pancake.getRect()[2])))
                    self.score += 1
                elif (pancakeRect[1] + pancakeRect[3] >= 1080):
                    self.pancakes.remove(pancake)
                    self.pancakes.append(SPFPancake(self.screen, x=random.randint(0, 1920 - pancake.getRect()[2])))
                    self.missSound.play()
                    self.miss += 1
        elif (not self.gameOver and self.score >= 20 and self.miss < 3):
            # If they won, meaning they got 20 pancakes, with no more than two misses.
            self.winSound.play()
            self.gameOver = True
        elif (not self.gameOver and self.miss >= 3):
            # If they didn't fill the above requirement, they've lost the game.
            self.loseSound.play()
            self.gameOver = True
        elif (self.gameOver):
            # Draw the appropriate text.
            if (self.miss >= 3):
                font = pygame.font.SysFont("TF2", 256)
                text = font.render("YOU FAILED", True, (255, 0, 0))
                text_w = text.get_rect().width
                text_h = text.get_rect().height

                self.screen.blit(text, ((1920 / 2) - text_w / 2, 400 - text_h / 2))
            else:
                font = pygame.font.SysFont("TF2", 256)
                text = font.render("VICTORY", True, (0, 255, 0))
                text_w = text.get_rect().width
                text_h = text.get_rect().height

                self.screen.blit(text, ((1920 / 2) - text_w / 2, 400 - text_h / 2))


        self.scout.blit(Clock)
        self.scout.setSpeed(0)

        # Update the Game State dictionary.
        self.gameState['score'] = self.score
        self.gameState['miss'] = self.miss
        self.gameState['FPS'] = Clock.get_fps()
        self.gameState['powerups'] = self.powerups
        self.gameState['time'] = Clock.get_time()

        # Update the HUD.
        self.HUD.update(self.gameState)

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.scout.setSpeed(-self.speed)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.scout.setSpeed(self.speed)

        # Handle joystick events ONLY IF there's a joystick initialized.
        if (self.joystick != None):
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

            if self.joystick.get_hat(0)[0] > 0:
                self.scout.setSpeed(self.speed)
            elif self.joystick.get_hat(0)[0] < 0:
                self.scout.setSpeed(-self.speed)



        pygame.display.update()