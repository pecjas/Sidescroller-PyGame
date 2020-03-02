import pygame
from side_scroller.score import Score
from side_scroller.constants import IMAGE_PATH, SCORE_PATH

class Background(pygame.sprite.Sprite):
    """ The game's background image information. """
    def __init__(self, image_file: str):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"{IMAGE_PATH}{image_file}")
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0

class Fonts():

    pygame.font.init()
    hud_font = pygame.font.SysFont("Ariel", 20)

    loss_font = pygame.font.SysFont("Ariel", 100)
    retry_font = pygame.font.SysFont("Ariel", 30)
    high_score_font = pygame.font.SysFont("Ariel", 50)
    score_font = pygame.font.SysFont("Ariel", 50)

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
    allTimeScore.load_high_score("test/score/")

    hoverLimit = 20
    maxSpeed = 3
    minSpeed = 2
    speed_increment_count = 10
    minFps = 60
    maxFps = 150

    obstacle_frequency = 40 #Increase for fewer obstacles from beginning
    obstacle_tick_adjustment = 40 #Amount obstacle frequency adjusts per level
    obstacle_tick_speed_adjustments = 0.5 #Amount speed increases per level after hitting maxFps

    fpsTick = 2
    levelTick = 100
    frequencyTick = 800 #Increase for lower obstacle increase per level

    def __init__(self):
        self.set_defaults()

    def set_defaults(self):
        """ Sets gamesetting defaults. """
        self.obstacle_frequency = GameSettings.obstacle_frequency
        self.obstacle_speed = 0
        self.game_fps = self.minFps
        self.fps_over_min = 1
