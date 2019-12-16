import pygame
import sys
import os

os.chdir("C:/Users/pecja/Development/Python/PyGame")

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

class SpeedCounter:
    def __init__(self, direction):
        self.count = 0
        self.direction = directions.get(direction)

class Player:
    up = pygame.image.load("SideScroller/img/up_state.png")
    neutral = pygame.image.load("SideScroller/img/neutral_state.png")
    down = pygame.image.load("SideScroller/img/down_state.png")
    width = max(up.get_width(), neutral.get_width(), down.get_width())
    height = max(up.get_height(), neutral.get_height(), down.get_height())

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.currentSpeed = 1
        self.speedCounter = SpeedCounter(1)

    def reset_speed(self):
        self.speedCounter.count = 0
        self.currentSpeed = GameSettings.minSpeed

    def increase_speed_counter(self, direction:int):
        """ Wrapper for increasing speed counter. If the direction has changed, we'll create a new counter
            and start the count over.
        """
        if self.speedCounter.direction != directions.get(direction):
            player.reset_speed()
            player.speedCounter = SpeedCounter(direction)
        if self.currentSpeed == GameSettings.maxSpeed:
            return
        self.speedCounter.count += 1
        if self.speedCounter.count % GameSettings.speedIncrementCount == 0:
            self.currentSpeed += 1
    
    def increase_y_axis(self, val):
        if self.y + val > GameSettings.yBottomBarrier:
            self.y = GameSettings.yBottomBarrier
        else:
            self.y += val
    
    def decrease_y_axis(self, val):
        if self.y - val < self.height:
            self.y = self.height
        else:
            self.y -= val


class GameSettings:
    height = 300
    width = 400
    hoverLimit = 5
    maxSpeed = 4
    minSpeed = 1
    speedIncrementCount = 10
    yBottomBarrier = height - Player.height

def up_key_state(screen, player:Player):
    """ Logic to execute when the up arrow is pressed. Returns updated neutralCount """
    screen.blit(player.up, (player.x, player.y))
    if player.y != Player.height:
        player.decrease_y_axis(1 * player.currentSpeed)
        player.increase_speed_counter(1)
    return 0

def down_key_state(screen, player:Player, neutralCount:int):
    """ Logic to execute when the down arrow is pressed. Returns updated neutralCount """
    if player.y < GameSettings.yBottomBarrier:
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

pygame.init()
screen = pygame.display.set_mode((GameSettings.width, GameSettings.height))
pygame.display.set_caption("Jason's Game")

player = Player(0, GameSettings.yBottomBarrier)

fps = 30
fpsClock = pygame.time.Clock()

endState = False

neutralCount = 0

while not endState:
    keys = pygame.key.get_pressed()
    screen.fill(white)

    if keys[pygame.K_UP]:
        neutralCount = up_key_state(screen, player)
    elif keys[pygame.K_DOWN] or (neutralCount > GameSettings.hoverLimit):
        neutralCount = down_key_state(screen, player, neutralCount)
    else:
        neutralCount = neutral_key_state(screen, player, neutralCount)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        #DEBUG
        #print(event)
        #ENDDEBUG
    pygame.display.update()
    print(neutralCount)
    fpsClock.tick(fps)