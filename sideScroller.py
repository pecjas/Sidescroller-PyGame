import sys
import os
import random
import json
import pygame

ABSPATH = os.path.abspath(__file__)
DNAME = os.path.dirname(ABSPATH)
os.chdir(DNAME)

#region Initializing Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#endregion

DIRECTIONS = {
    0: 'Neutral',
    1: 'Up',
    2: 'Down' }

highscore = {}

def load_highscore():
    """
    Attempts to load highscore from file.

    RETURNS: highscore info as dictionary. If it's not already within game, retrieves
    from file in same directory.
    """
    if len(highscore) > 0:
        return highscore
    try:
        return json.load(open('highscore.txt'))
    except:
        return {}


class Score:
    """ Tracks score. Intance tracks a given play's score/level. """
    highScore = 0

    def __init__(self):
        self.score = 0
        self.level = 1

    def reset_score(self):
        """ Reset score and update highscore if needed. """
        if self.score > Score.highScore:
            Score.highScore = self.score
        self.score = 0
        self.level = 1
    def set_highscore(self, score: dict, save: bool=False):
        """
        Updates highscore if passed in score is higher.

        RETURNS: True if score is higher than previous highscore. Otherwise, False.
        """
        if len(score) == 0:
            return False
        updated = False
        if score.get('score') > Score.highScore:
            Score.highScore = score.get('score')
            updated = True
        if updated is True and save is True:
            try:
                json.dump(score, open('highscore.txt', 'w'))
            except:
                raise Exception("Failed to save highscore to file.")
        return updated

class Background(pygame.sprite.Sprite):
    """ The game's background image information. """
    def __init__(self, imageFile: str):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imageFile)
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
    background = Background("img/background.jpg")
    lossScreen = Background("img/loss_screen.png")
    allTimeScore = Score()
    allTimeScore.set_highscore(load_highscore())

    hoverLimit = 20
    maxSpeed = 3
    minSpeed = 2
    speedIncrementCount = 10
    minFps = 30
    maxFps = 150

    obstacleFrequency = 60 #Increase for fewer obstacles from beginning
    obstacleTickAdjust = 10 #Amount obstacle frequency adjusts per level
    obstacleTickSpeedAdjust = 1 #Amount speed increases per level after hitting maxFps

    fpsTick = 30
    levelTick = 100
    frequencyTick = 1000 #Increase for lower obstacle increase per level

    def __init__(self):
        self.reset()

    def reset(self):
        """ Sets gamesetting defaults. """
        self.obstacleFrequency = GameSettings.obstacleFrequency
        self.obstacleSpeed = 0

class Obstacle(pygame.sprite.Sprite):
    """ Obstacles the player must avoid. """
    images = [pygame.image.load("img/obstacles/obstacle.png"),
    pygame.image.load("img/obstacles/obstacle2.png"),
    pygame.image.load("img/obstacles/obstacle3.png")]

    def __init__(self, x, y):
        self.image = Obstacle.images[random.randrange(0, len(Obstacle.images))]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = random.randint(1, 2)

        self.yBottomBarrier = GameSettings.height - self.height
        self.x = x + self.width
        if y > self.yBottomBarrier:
            self.y = self.yBottomBarrier
        else:
            self.y = y
        self.rect = pygame.Rect(x + self.width, self.y, self.width, self.height)

class SpeedCounter:
    """ Tracks direction and distance traveled. Used to determine object speed. """
    def __init__(self, direction):
        self.count = 0
        self.direction = DIRECTIONS.get(direction)

class Hitbox(pygame.sprite.Sprite):
    """ Hitboxes to facilitate collision detection. """
    def __init__(self, rect: pygame.Rect, orientation):
        self.rect = rect
        self.orientation = orientation

class Player(pygame.sprite.Sprite):
    """ The player sprite controlled by the user. """
    up = pygame.image.load("img/player/up_state.png")
    neutral = pygame.image.load("img/player/neutral_state.png")
    down = pygame.image.load("img/player/down_state.png")
    width = max(up.get_width(), neutral.get_width(), down.get_width())
    height = max(up.get_height(), neutral.get_height(), down.get_height())
    yBottomBarrier = GameSettings.height - height

    def __init__(self, x: int=0, y: int=0):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, Player.width, Player.height)

        self.hitboxes = [Hitbox(pygame.Rect(x, y, Player.width, Player.height), DIRECTIONS.get(0))]
        #Upstate hitboxes
        self.hitboxes.append(
            Hitbox(pygame.Rect(x, y, Player.width, round(Player.height/2)),
            DIRECTIONS.get(1)))
        self.hitboxes.append(
            Hitbox(pygame.Rect(x, y, round(Player.width/2), Player.height),
            DIRECTIONS.get(1)))
        #Downstate hitboxes
        self.hitboxes.append(
            Hitbox(pygame.Rect(x, y + round(Player.height/2), Player.width, round(Player.height/2)),
            DIRECTIONS.get(2)))
        self.hitboxes.append(
            Hitbox(pygame.Rect(x, y, round(Player.width/2), Player.height),
            DIRECTIONS.get(2)))

        self.orientation = DIRECTIONS.get(0)
        self.currentSpeed = 1
        self.levelSpeedBoost = 0
        self.speedCounter = SpeedCounter(1)
        self.progressToMove = 0

        self.score = Score()
        self.game = GameSettings()

    def reset_speed(self):
        """ Reset SpeedCounter to defaults. Should be called whenever a new round starts. """
        self.speedCounter.count = 0
        self.currentSpeed = GameSettings.minSpeed
        self.levelSpeedBoost = 0
        self.progressToMove = 0

    def increase_speed_counter(self, direction: int, fpsOverMin: float):
        """
            Wrapper for increasing speed counter. If the direction has changed, we'll create a new
            counter and start the count over.
        """
        if self.speedCounter.direction != DIRECTIONS.get(direction):
            self.reset_speed()
            self.speedCounter = SpeedCounter(direction)
        if self.currentSpeed == GameSettings.maxSpeed:
            return
        self.speedCounter.count += 1
        if (self.speedCounter.count / int(fpsOverMin)) % GameSettings.speedIncrementCount == 0:
            self.currentSpeed += 1

    def increase_y_axis(self, val: int):
        """ Move player down. Includes handling to avoid leaving screen. """
        if self.y + val > self.yBottomBarrier:
            yAdjust = self.yBottomBarrier - self.y
            self.y = self.yBottomBarrier
        else:
            yAdjust = val
            self.y += val
        self.rect.move_ip(0, yAdjust)
        for hitbox in self.hitboxes:
            hitbox.rect.move_ip(0, yAdjust)
    
    def decrease_y_axis(self, val: int):
        """ Move player up. Includes handling to avoid leaving screen. """
        if self.y - val < 0:
            yAdjust = self.y
            self.y = 0
        else:
            yAdjust = val
            self.y -= val
        self.rect.move_ip(0, -yAdjust)
        for hitbox in self.hitboxes:
            hitbox.rect.move_ip(0, -yAdjust)

    def adjust_highscores(self):
        """ Wrapper tag to update highscore after the completion of a game. """
        score = {'score':int(self.score.score)}
        self.score.set_highscore(score, True)

    def can_move(self, movement: int, direction: str):
        """
        Checks if player has made enough progress to move a pixel
        and updates progressToMove accordingly
        RETURNS: True if player can move
        """
        if direction != self.orientation:
            self.progressToMove = movement
            return False
        self.progressToMove += movement
        if self.progressToMove < 1:
            return False
        self.progressToMove -= 1
        return True

    def prepare_new_game(self):
        self.reset_speed()
        self.score.reset_score()
        self.game.reset()

def up_key_state(screen, player: Player, fpsOverMin: int):
    """ Logic to execute when the up arrow is pressed. Returns updated neutralCount """
    previousOrientation = player.orientation
    player.orientation = DIRECTIONS.get(1)
    if player.y != 0:
        if player.can_move(player.currentSpeed / fpsOverMin, previousOrientation):
            player.decrease_y_axis(player.currentSpeed + int(player.levelSpeedBoost))
        player.increase_speed_counter(1, fpsOverMin)
    screen.blit(player.up, (player.x, player.y))
    return 0

def down_key_state(screen: pygame.display, player: Player, neutralCount: int, fpsOverMin: int):
    """ Logic to execute when the down arrow is pressed. Returns updated neutralCount """
    previousOrientation = player.orientation
    player.orientation = DIRECTIONS.get(2)
    if player.y < Player.yBottomBarrier:
        if player.can_move(player.currentSpeed / fpsOverMin, previousOrientation):
            player.increase_y_axis(player.currentSpeed + int(player.levelSpeedBoost))
        screen.blit(player.down, (player.x, player.y))
    else:
        screen.blit(player.neutral, (player.x, player.y))
    if neutralCount <= (GameSettings.hoverLimit * fpsOverMin):
        neutralCount = 0
    player.increase_speed_counter(2, fpsOverMin)
    return neutralCount

def neutral_key_state(screen, player: Player, neutralCount: int, fpsOverMin: float):
    """ Logic to execute when no relevant key is pressed. Returns updated neutralCount """
    previousOrientation = player.orientation
    if player.speedCounter.direction == DIRECTIONS.get(1):
        player.reset_speed()
        player.orientation = DIRECTIONS.get(0)
        screen.blit(player.neutral, (player.x, player.y))
    elif player.rect.bottom < GameSettings.height:
        if player.can_move(player.currentSpeed, previousOrientation):
            player.increase_y_axis(player.currentSpeed + int(player.levelSpeedBoost))
        player.orientation = DIRECTIONS.get(2)
        screen.blit(player.down, (player.x, player.y))
    else:
        screen.blit(player.neutral, (player.x, player.y))
    return neutralCount + fpsOverMin

def move_obstacles(screen, obstacles: list, player: Player, fps: int):
    removedObstacles = []
    for obstacle in obstacles:
        xShift = obstacle.speed + player.game.obstacleSpeed
        screen.blit(GameSettings.background.image,
                    (obstacle.rect.x + int(obstacle.width/2), obstacle.rect.y),
                    (obstacle.rect.x + int(obstacle.width/2), obstacle.rect.y, int(obstacle.width/2), obstacle.height))
        obstacle.x -= xShift
        obstacle.rect.move_ip(-(xShift), 0)
        if obstacle.x < -obstacle.width:
            removedObstacles.append(obstacle)
        else:
            screen.blit(obstacle.image, (obstacle.x, obstacle.y))
    for obstacle in removedObstacles:
        obstacles.remove(obstacle)

def quit_game():
    """ Exit game. Executed when 'x' is clicked. """
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def wait_for_return():
    """ Hangs game on current screen until player hits Return or quits. """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True

def loss_screen(player: Player, screen: pygame.display):
    """ Screen to display after player has collided with an obstacle. """
    screen.blit(GameSettings.lossScreen.image, GameSettings.lossScreen.rect)

    lossFont = pygame.font.SysFont("Ariel", 100)
    lossText = lossFont.render("Game Over", True, WHITE)
    screen.blit(lossText,
                lossText.get_rect(center=(int(GameSettings.width/2), int(GameSettings.height/4))))

    highScoreFont = pygame.font.SysFont("Ariel", 50)
    highScoreText = highScoreFont.render(f"High Score: {int(Score.highScore)}", True, WHITE)
    screen.blit(highScoreText,
                highScoreText.get_rect(center=(int(GameSettings.width/2), int(GameSettings.height/3))))

    scoreFont = pygame.font.SysFont("Ariel", 50)
    scoreText = scoreFont.render(f"Your Score: {int(player.score.score)}", True, WHITE)
    screen.blit(scoreText,
                scoreText.get_rect(center=(int(GameSettings.width/2), int(GameSettings.height/2))))

    retryFont = pygame.font.SysFont("Ariel", 30)
    retryText = retryFont.render("Press Enter to try again.", True, WHITE)
    screen.blit(retryText,
                retryText.get_rect(center=(int(GameSettings.width/2), int(GameSettings.height/2 + scoreText.get_height()))))
    pygame.display.update()
    return wait_for_return()

def score_HUD(screen, player: Player):
    """ Displays up-to-date score during gameplay. """
    font = pygame.font.SysFont("Ariel", 20)
    text = font.render(f"Score: {int(player.score.score)} Level: {player.score.level}", True, BLACK)
    screen.blit(GameSettings.background.image, text.get_rect(), text.get_rect())
    screen.blit(text, text.get_rect())

def tick_adjustments(player: Player, obstacles: list, fps: int, fpsOverMin: float):
    """
    Updates to score and game based on current tick.

    RETURN: Updated fps
    """
    if round(player.score.score, 3) % player.game.obstacleFrequency == 0:
        obstacles.append(Obstacle(random.randrange(GameSettings.width, GameSettings.width + 50), 
                        random.randrange(0, GameSettings.height)))
    if round(player.score.score, 3) % GameSettings.levelTick == 0:
        player.score.level += 1
        if fps < GameSettings.maxFps:
            fps += GameSettings.fpsTick
            fpsOverMin = fps / GameSettings.minFps
        else:
            player.game.obstacleSpeed += GameSettings.obstacleTickSpeedAdjust
            player.levelSpeedBoost += GameSettings.obstacleTickSpeedAdjust / 2
    if round(player.score.score, 3) % GameSettings.frequencyTick == 0:
        if player.game.obstacleFrequency > GameSettings.obstacleTickAdjust:
            player.game.obstacleFrequency -= GameSettings.obstacleTickAdjust
        else:
            newFrequency = int(player.game.obstacleFrequency/2)
            player.game.obstacleFrequency = newFrequency
    return fps, fpsOverMin

def main(player: Player, screen: pygame.display):
    """ Main tag. Initializes game settings and main game loop. """
    gameFps = GameSettings.minFps
    fpsOverMin = 1
    fpsClock = pygame.time.Clock()
    endState = False
    neutralCount = 0
    obstacles = []
    screen.blit(GameSettings.background.image, GameSettings.background.rect)

    while not endState:
        player.score.score += GameSettings.minFps/gameFps
        screen.blit(GameSettings.background.image, player.rect, player.rect)
        score_HUD(screen, player)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            neutralCount = up_key_state(screen, player, fpsOverMin)
        elif keys[pygame.K_DOWN] or (neutralCount > GameSettings.hoverLimit * fpsOverMin):
            neutralCount = down_key_state(screen, player, neutralCount, fpsOverMin)
        else:
            neutralCount = neutral_key_state(screen, player, neutralCount, fpsOverMin)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        gameFps, fpsOverMin = tick_adjustments(player, obstacles, gameFps, fpsOverMin)
        move_obstacles(screen, obstacles, player, gameFps)
        pygame.display.update()

        for hitbox in player.hitboxes:
            if hitbox.orientation == player.orientation:
                if len(pygame.sprite.spritecollide(hitbox, obstacles, False)) > 0:
                    endState = True

        fpsClock.tick(gameFps)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Sky Scroller")
    currentPlayer = Player(0, Player.yBottomBarrier)
    currentScreen = pygame.display.set_mode((GameSettings.width, GameSettings.height))

    play = True
    while play is True:
        main(currentPlayer, currentScreen)
        currentPlayer.adjust_highscores()
        play = loss_screen(currentPlayer, currentScreen)
        currentPlayer.prepare_new_game()
