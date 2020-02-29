import random
import pygame
from side_scroller.settings import GameSettings
from side_scroller.player import Player
from side_scroller.constants import OBSTACLE_PATH

class Obstacle(pygame.sprite.Sprite):
    images = [
        pygame.image.load(f"{OBSTACLE_PATH}obstacle.png"),
        pygame.image.load(f"{OBSTACLE_PATH}obstacle2.png"),
        pygame.image.load(f"{OBSTACLE_PATH}obstacle3.png")]

    def __init__(self, x, y):
        self.image = Obstacle.images[random.randrange(0, len(Obstacle.images))]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = random.randint(1, 2)

        self.y_bottom_barrier = GameSettings.height - self.height
        self.x = x + self.width
        if y > self.y_bottom_barrier:
            self.y = self.y_bottom_barrier
        else:
            self.y = y
        self.rect = pygame.Rect(x + self.width, self.y, self.width, self.height)

def move_obstacles(screen, obstacles: list, player: Player):
    """ Move obstacles and refresh background for past obstacle positions. """
    #Clear current obstalce locations to refresh background
    for obstacle in obstacles:
        screen.blit(
            GameSettings.background.image,
            (obstacle.rect.x + int(obstacle.width/2), obstacle.rect.y),
            (obstacle.rect.x + int(obstacle.width/2), obstacle.rect.y, int(obstacle.width/2), obstacle.height))

    #Blit obstacles at new position
    removed_obstacles = []
    for obstacle in obstacles:
        x_shift = int(player.game.obstacleSpeed + player.score.level + obstacle.speed)
        obstacle.x -= x_shift
        obstacle.rect.move_ip(-(x_shift), 0)
        if obstacle.x < -obstacle.width:
            removed_obstacles.append(obstacle)
        else:
            screen.blit(obstacle.image, (obstacle.x, obstacle.y))
    for obstacle in removed_obstacles:
        obstacles.remove(obstacle)
