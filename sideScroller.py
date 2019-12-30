import pygame
import sys
import os
import random
import json

#DEBUG for running in IDE terminal
os.chdir("C:/Users/pecja/Development/Python/PyGame/SideScroller")
#END

#region Initializing Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
#endregion

directions = {
    1: 'Up',
    2: 'Down' }

highscore = {}

def load_highscore():
    """ Returns highscore info as dictionary. If it's not already within game, retrieves from file in same directory. """
    if len(highscore) > 0:
        return highscore
    try:
        return json.load(open('highscore.txt'))
    except:
        return {}


class Score:
    highScore = 0
    highLevel = 0

    def __init__(self):
        self.score = 0
        self.level = 1
    
    def reset_score(self):
        """ Reset score and update high score/level if needed. """
        if self.score > Score.highScore:
            Score.highScore = self.score
        if self.level > Score.highLevel:
            Score.highLevel = self.level
        self.score = 0
        self.level = 1
    def set_highscore(self, score:dict, save:bool=False):
        """ Adjusts highscores. returns True if score is higher than previous high score. Otherwise, False. """
        if len(score) == 0:
            return False
        updated = False
        if score.get('score') > self.highScore:
            self.highScore = score.get('score')
            updated = True
        if score.get('level') > self.highLevel:
            self.highLevel = score.get('level')
            updated = True
        if updated is True and save is True:
            try:
                json.dump(score, open('highscore.txt', 'w'))
            except:
                raise Exception("Failed to save highscore to file.")
        return updated

class Background(pygame.sprite.Sprite):
    def __init__(self, imageFile):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imageFile)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0

class GameSettings:
    height = 300
    width = 400
    background = Background("img/background.png")
    allTimeScore = Score()
    allTimeScore.set_highscore(load_highscore())

    hoverLimit = 5
    maxSpeed = 6
    minSpeed = 1
    speedIncrementCount = 10

    obstacleFrequency = 50
    obstacleSpeed = 3

    levelTick = 200
    frequencyTick = 1000

    def __init__(self):
        self.obstacleFrequency = GameSettings.obstacleFrequency
        self.obstacleSpeed = GameSettings.obstacleSpeed

class Obstacle(pygame.sprite.Sprite):
    images = [pygame.image.load("img/obstacles/obstacle.png"),
    pygame.image.load("img/obstacles/obstacle2.png"),
    pygame.image.load("img/obstacles/obstacle3.png")]
    image = pygame.image.load("img/obstacles/obstacle.png")

    width = image.get_width()
    height = image.get_height()

    def __init__(self, x, y):
        self.image = Obstacle.images[random.randrange(0, len(Obstacle.images))]
        width = self.image.get_width()
        height = self.image.get_height()

        self.yBottomBarrier = GameSettings.height - height
        self.x = x + width
        if y > self.yBottomBarrier:
            self.y = self.yBottomBarrier
        else:
            self.y = y
        self.rect = pygame.Rect(x + width, y, width, height)

class SpeedCounter:
    def __init__(self, direction):
        self.count = 0
        self.direction = directions.get(direction)

class Player(pygame.sprite.Sprite):
    up = pygame.image.load("img/player/up_state.png")
    neutral = pygame.image.load("img/player/neutral_state.png")
    down = pygame.image.load("img/player/down_state.png")
    width = max(up.get_width(), neutral.get_width(), down.get_width())
    height = max(up.get_height(), neutral.get_height(), down.get_height())
    yBottomBarrier = GameSettings.height - height

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, Player.width, Player.height)

        self.currentSpeed = 1
        self.speedCounter = SpeedCounter(1)

        self.score = Score()
        self.game = GameSettings()

    def reset_speed(self):
        self.speedCounter.count = 0
        self.currentSpeed = GameSettings.minSpeed

    def increase_speed_counter(self, direction:int):
        """ Wrapper for increasing speed counter. If the direction has changed, we'll create a new counter
            and start the count over.
        """
        if self.speedCounter.direction != directions.get(direction):
            self.reset_speed()
            self.speedCounter = SpeedCounter(direction)
        if self.currentSpeed == GameSettings.maxSpeed:
            return
        self.speedCounter.count += 1
        if self.speedCounter.count % GameSettings.speedIncrementCount == 0:
            self.currentSpeed += 1

    def increase_y_axis(self, val):
        if self.y + val > self.yBottomBarrier:
            yAdjust = self.yBottomBarrier - self.y
            self.y = self.yBottomBarrier
        else:
            yAdjust = val
            self.y += val
        self.rect.move_ip(0, yAdjust)
    
    def decrease_y_axis(self, val):
        if self.y - val < 0:
            yAdjust = self.y
            self.y = 0
        else:
            yAdjust = val
            self.y -= val
        self.rect.move_ip(0, -yAdjust)
    
    def adjust_highscores(self):
        score = {'score':self.score.score,
                'level':self.score.level}
        self.score.set_highscore(score)
        self.game.allTimeScore.set_highscore(score, True)

def up_key_state(screen, player:Player):
    """ Logic to execute when the up arrow is pressed. Returns updated neutralCount """
    screen.blit(player.up, (player.x, player.y))
    if player.y != 0:
        player.decrease_y_axis(1 * player.currentSpeed)
        player.increase_speed_counter(1)
    return 0

def down_key_state(screen, player:Player, neutralCount:int):
    """ Logic to execute when the down arrow is pressed. Returns updated neutralCount """
    if player.y < Player.yBottomBarrier:
        screen.blit(player.down, (player.x, player.y))
        player.increase_y_axis(1 * player.currentSpeed)
    else:
        screen.blit(player.neutral, (player.x, player.y))
    if neutralCount <= GameSettings.hoverLimit:
        neutralCount = 0
    player.increase_speed_counter(2)
    return neutralCount

def neutral_key_state(screen, player:Player, neutralCount:int):
    """ Logic to execute when no relevant key is pressed. Returns updated neutralCount """
    if player.speedCounter.direction == directions.get(1):
        screen.blit(player.neutral, (player.x, player.y))
        player.reset_speed()
    else:
        screen.blit(player.down, (player.x, player.y))
        player.increase_y_axis(1 * player.currentSpeed)
    return neutralCount + 1

def move_obstacles(screen, obstacles:list, player:Player):
    removedObstacles = []
    for obstacle in obstacles:
        screen.blit(obstacle.image, (obstacle.x, obstacle.y))
        xShift = player.game.obstacleSpeed + (1 * player.score.level)
        obstacle.x -= xShift
        obstacle.rect.move_ip(-(xShift), 0)
        if obstacle.x < -obstacle.width:
            removedObstacles.append(obstacle)
    for obstacle in removedObstacles:
        obstacles.remove(obstacle)

def quit_game():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def wait_for_return():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True

def loss_screen(player:Player, screen:pygame.display):
    screen.fill(white)
    highScoreFont = pygame.font.SysFont("Ariel", 20)
    highScoreText = highScoreFont.render(f"Level: {player.score.level}    Score: {player.score.score}", True, black)
    screen.blit(highScoreText, highScoreText.get_rect(center=(int(GameSettings.width/2), int(GameSettings.height/2))))

    lossFont = pygame.font.SysFont("Ariel", 40)
    lossText = lossFont.render("Game Over", True, black)
    screen.blit(lossText, lossText.get_rect(center=(int(GameSettings.width/2), int(GameSettings.height/2 - highScoreText.get_height()))))
    
    retryFont = pygame.font.SysFont("Ariel", 30)
    retryText = retryFont.render("Press Enter to try again.", True, black)
    screen.blit(retryText, retryText.get_rect(center=(int(GameSettings.width/2), int(GameSettings.height/2 + highScoreText.get_height()))))
    pygame.display.update()
    return wait_for_return()

def score_HUD(screen, player:Player):
    font = pygame.font.SysFont("Ariel", 20)
    text = font.render(f"Level: {player.score.level}    Score: {player.score.score}", True, black)
    screen.blit(text, text.get_rect())

def tick_adjustments(player:Player, obstacles:list):
    """ Updates to score and game based on current tick. """
    if player.score.score % player.game.obstacleFrequency == 0:
        obstacles.append(Obstacle(random.randrange(GameSettings.width, GameSettings.width + 50), 
                        random.randrange(0, GameSettings.height)))
    if player.score.score % GameSettings.levelTick == 0:
        player.score.level += 1
    if player.score.score % GameSettings.frequencyTick == 0:
        newFrequency = int(player.game.obstacleFrequency/2)
        player.game.obstacleFrequency = newFrequency

def main(player:Player, screen:pygame.display):
    fps = 30
    fpsClock = pygame.time.Clock()

    endState = False

    neutralCount = 0
    obstacles = []

    while not endState:
        player.score.score += 1
        screen.blit(GameSettings.background.image, GameSettings.background.rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            neutralCount = up_key_state(screen, player)
        elif keys[pygame.K_DOWN] or (neutralCount > GameSettings.hoverLimit):
            neutralCount = down_key_state(screen, player, neutralCount)
        else:
            neutralCount = neutral_key_state(screen, player, neutralCount)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        
        tick_adjustments(player, obstacles)

        move_obstacles(screen, obstacles, player)
        score_HUD(screen, player)
        pygame.display.update()
        if len(pygame.sprite.spritecollide(player, obstacles, False)) > 0:
            endState = True
        fpsClock.tick(fps)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Jason's Game")
    player = Player(0, Player.yBottomBarrier)
    screen = pygame.display.set_mode((GameSettings.width, GameSettings.height))

    play = True
    while play is True:
        main(player, screen)
        player.adjust_highscores()
        play = loss_screen(player, screen)
        player.score.reset_score()