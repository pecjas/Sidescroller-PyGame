import sys
import os
import random
import pygame
from side_scroller.game import Game
from side_scroller.obstacle import Obstacle, move_obstacles
from side_scroller.settings import GameSettings
from side_scroller.loss_screen import LossScreen
from side_scroller.states import (up_key_state, neutral_key_state, down_key_state,
                                  is_player_moving_up, is_player_moving_down)

def change_to_file_directory():
    absolute_path = os.path.abspath(__file__)
    directory_name = os.path.dirname(absolute_path)
    os.chdir(directory_name)

def start_game():
    continue_playing = True

    current_game = Game()
    while continue_playing is True:
        main_game_loop(current_game)

        current_game.update_high_score()
        continue_playing = display_loss_screen(current_game)

        current_game.prepare_new_game()

def main_game_loop(current_game: Game):
    end_state = False

    while not end_state:
        current_game.set_per_loop_adjustment()
        current_game.player.score.increase_score(current_game.per_loop_adjustment)

        current_game.refresh_background()
        current_game.update_score_hud()

        current_game.neutral_count = respond_to_key_press(current_game)

        if_necessary_quit_game()

        tick_adjustments(current_game)
        move_obstacles(current_game)
        pygame.display.update()

        end_state = current_game.player.is_colliding_with_obstacles(current_game.obstacles)
        current_game.tick_game_fps_clock()

def respond_to_key_press(game: Game):
    keys = pygame.key.get_pressed()
    if is_player_moving_up(keys):
        return up_key_state(game)
    elif is_player_moving_down(keys, game):
        return down_key_state(game)
    else:
        return neutral_key_state(game)

def tick_adjustments(game: Game):
    game.increase_count_to_obstacle_tick()
    game.increase_count_to_level_tick()

    if_necessary_add_obstacles(game)
    if if_necessary_increase_level(game):
        increase_obstacle_speed(game)
    if_necessary_increase_obstacle_frequency(game)

def if_necessary_add_obstacles(game: Game):
    if game.player.score.countToObstacleTick > game.player.game_settings.obstacle_frequency:
        game.obstacles.append(Obstacle(random.randrange(GameSettings.width, GameSettings.width + 50),
                                  random.randrange(0, GameSettings.height)))
        game.player.score.countToObstacleTick -= game.player.game_settings.obstacle_frequency

def if_necessary_increase_level(game: Game) -> bool:
    if game.player.score.countToLevelTick > GameSettings.levelTick:
        game.player.score.level += 1
        game.player.score.countToLevelTick -= GameSettings.levelTick
        return True
    return False

def increase_obstacle_speed(game: Game):
    if game.game_fps < GameSettings.maxFps:
        game.game_fps += GameSettings.fpsTick
        game.fps_over_min = game.game_fps / GameSettings.minFps
    else:
        game.player.game_settings.obstacle_speed += GameSettings.obstacle_tick_speed_adjustments
        game.player.adjust_level_speed_boost(GameSettings.obstacle_tick_speed_adjustments / 2)

def if_necessary_increase_obstacle_frequency(game: Game):
    if game.player.score.countToFrequencyTick > GameSettings.frequencyTick:
        game.player.score.countToFrequencyTick -= GameSettings.frequencyTick
        if game.player.game_settings.obstacle_frequency > GameSettings.obstacle_tick_adjustment:
            game.player.game_settings.obstacle_frequency -= GameSettings.obstacle_tick_adjustment
        else:
            new_frequency = int(game.player.game_settings.obstacle_frequency/2)
            game.player.game_settings.obstacle_frequency = new_frequency

def display_loss_screen(game: Game):
    loss_screen = LossScreen(game.player)
    loss_screen.display(game.screen)
    return wait_for_return_key_press()

def wait_for_return_key_press():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True

def if_necessary_quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

def quit_game():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    change_to_file_directory()
    start_game()
