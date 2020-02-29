import pygame
from side_scroller.score import Score
from side_scroller.constants import IMAGE_PATH

class Background(pygame.sprite.Sprite):
    """ The game's background image information. """
    def __init__(self, imageFile: str):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"{IMAGE_PATH}{imageFile}")
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0

class GameSettings:
    """
    Game settings to simplify game adjustments. Most values are global, but
    instances allow maintaining values that could update throught game.
    """
    height = 600
    width = 800
    background = Background("background.jpg")
    lossScreen = Background("loss_screen.png")
    allTimeScore = Score()
    allTimeScore.load_high_score()

    hoverLimit = 20
    maxSpeed = 3
    minSpeed = 2
    speedIncrementCount = 10
    minFps = 60
    maxFps = 150

    obstacleFrequency = 40 #Increase for fewer obstacles from beginning
    obstacleTickAdjust = 40 #Amount obstacle frequency adjusts per level
    obstacleTickSpeedAdjust = 0.5 #Amount speed increases per level after hitting maxFps

    fpsTick = 2
    levelTick = 100
    frequencyTick = 800 #Increase for lower obstacle increase per level

    def __init__(self):
        self.reset()

    def reset(self):
        """ Sets gamesetting defaults. """
        self.obstacleFrequency = GameSettings.obstacleFrequency
        self.obstacleSpeed = 0
