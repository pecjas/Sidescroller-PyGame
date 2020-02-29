import sys
import os
import random
import pygame
from side_scroller.score import Score
from side_scroller.obstacle import Obstacle, move_obstacles
from side_scroller.player import Player
from side_scroller.settings import GameSettings
from side_scroller.states import up_key_state, neutral_key_state, down_key_state

#region Initializing Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#endregion

def change_to_file_directory():
    absolute_path = os.path.abspath(__file__)
    directory_name = os.path.dirname(absolute_path)
    os.chdir(directory_name)

def start_game():
    pygame.init()
    pygame.display.set_caption("Sky Scroller")
    current_player = Player(0, Player.y_bottom_barrier)
    current_screen = pygame.display.set_mode((GameSettings.width, GameSettings.height))

    play = True
    while play is True:
        main(current_player, current_screen)
        current_player.adjust_high_scores()
        play = loss_screen(current_player, current_screen)
        current_player.prepare_new_game()

def main(player: Player, screen: pygame.display):
    """ Main tag. Initializes game settings and main game loop. """
    game_fps = GameSettings.minFps
    fps_over_min = 1
    fps_clock = pygame.time.Clock()
    end_state = False
    neutral_count = 0
    obstacles = []
    screen.blit(GameSettings.background.image, GameSettings.background.rect)

    while not end_state:
        score_adjustment = GameSettings.minFps/game_fps
        player.score.score += score_adjustment
        player.score.countToObstacleTick += score_adjustment
        player.score.countToLevelTick += score_adjustment

        screen.blit(GameSettings.background.image, player.rect, player.rect)
        score_hud(screen, player)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            neutral_count = up_key_state(screen, player, fps_over_min)
        elif keys[pygame.K_DOWN] or (neutral_count > GameSettings.hoverLimit * fps_over_min):
            neutral_count = down_key_state(screen, player, neutral_count, fps_over_min)
        else:
            neutral_count = neutral_key_state(screen, player, neutral_count, fps_over_min)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        game_fps, fps_over_min = tick_adjustments(player, obstacles, game_fps, fps_over_min)
        move_obstacles(screen, obstacles, player)
        pygame.display.update()

        for hitbox in player.hitboxes:
            if hitbox.orientation == player.orientation:
                if len(pygame.sprite.spritecollide(hitbox, obstacles, False)) > 0:
                    end_state = True

        fps_clock.tick(game_fps)

def score_hud(screen, player: Player):
    """ Displays up-to-date score during gameplay. """
    font = pygame.font.SysFont("Ariel", 20)
    text = font.render(f"Score: {int(player.score.score)} Level: {player.score.level}", True, BLACK)
    screen.blit(GameSettings.background.image, text.get_rect(), text.get_rect())
    screen.blit(text, text.get_rect())

def tick_adjustments(player: Player, obstacles: list, fps: int, fps_over_min: float):
    """
    Updates to score and game based on current tick.

    RETURN: Updated fps
    """
    if player.score.countToObstacleTick > player.game.obstacleFrequency:
        obstacles.append(Obstacle(random.randrange(GameSettings.width, GameSettings.width + 50),
                                  random.randrange(0, GameSettings.height)))
        player.score.countToObstacleTick -= player.game.obstacleFrequency
    if player.score.countToLevelTick > GameSettings.levelTick:
        player.score.level += 1
        player.score.countToLevelTick -= GameSettings.levelTick
        if fps < GameSettings.maxFps:
            fps += GameSettings.fpsTick
            fps_over_min = fps / GameSettings.minFps
        else:
            player.game.obstacleSpeed += GameSettings.obstacleTickSpeedAdjust
            player.adjust_level_speed_boost(GameSettings.obstacleTickSpeedAdjust / 2)
    if player.score.countToFrequencyTick > GameSettings.frequencyTick:
        player.score.countToFrequencyTick -= GameSettings.frequencyTick
        if player.game.obstacleFrequency > GameSettings.obstacleTickAdjust:
            player.game.obstacleFrequency -= GameSettings.obstacleTickAdjust
        else:
            new_frequency = int(player.game.obstacleFrequency/2)
            player.game.obstacleFrequency = new_frequency
    return fps, fps_over_min

def loss_screen(player: Player, screen: pygame.display):
    """ Screen to display after player has collided with an obstacle. """
    screen.blit(GameSettings.lossScreen.image, GameSettings.lossScreen.rect)

    loss_font = pygame.font.SysFont("Ariel", 100)
    loss_text = loss_font.render("Game Over", True, WHITE)
    screen.blit(loss_text,
                loss_text.get_rect(center=(int(GameSettings.width/2), int(GameSettings.height/4))))

    high_score_font = pygame.font.SysFont("Ariel", 50)
    high_score_text = high_score_font.render(f"High Score: {int(Score.high_score.get('score'))}", True, WHITE)
    screen.blit(high_score_text,
                high_score_text.get_rect(center=(int(GameSettings.width/2), int(GameSettings.height/3))))

    score_font = pygame.font.SysFont("Ariel", 50)
    score_text = score_font.render(f"Your Score: {int(player.score.score)}", True, WHITE)
    screen.blit(score_text,
                score_text.get_rect(center=(int(GameSettings.width/2), int(GameSettings.height/2))))

    retry_font = pygame.font.SysFont("Ariel", 30)
    retry_text = retry_font.render("Press Enter to try again.", True, WHITE)
    screen.blit(retry_text,
                retry_text.get_rect(
                    center=(int(GameSettings.width/2),
                    int(GameSettings.height/2 + score_text.get_height()))))
    pygame.display.update()
    return wait_for_return()

def wait_for_return():
    """ Hangs game on current screen until player hits Return or quits. """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True

def quit_game():
    """ Exit game. Executed when 'x' is clicked. """
    pygame.display.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    change_to_file_directory()
    start_game()
