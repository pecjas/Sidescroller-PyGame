from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from side_scroller.game import Game
import pygame
from side_scroller.settings import GameSettings

def display_player_death_animation(current_game: Game):
    obstacles_in_player_path_y = [(obstacle.image, obstacle.rect) for obstacle in current_game.get_obstacles_in_player_path_y()]

    _move_player_up(current_game, obstacles_in_player_path_y)
    _drop_player_off_screen(current_game, obstacles_in_player_path_y)

def _move_player_up(current_game: Game, obstacles_in_player_path_y: list):
    for _ in range(1, GameSettings.death_raise_duration):
        current_game.refresh_player_location_background()

        current_game.player.decrease_y_axis(GameSettings.death_raise_speed, False)
        current_game.screen.blit(
            current_game.player.neutral,
            (current_game.player.x, current_game.player.y)
        )

        current_game.screen.blits(
            obstacles_in_player_path_y
        )

        pygame.display.update()
        current_game.tick_game_fps_clock()

def _drop_player_off_screen(current_game: Game, obstacles_in_player_path_y: list):
    count = 0
    player_height = current_game.player.down.get_rect().height

    while not _is_player_off_screen_bottom(current_game, player_height):
        current_game.refresh_player_location_background()

        current_game.player.increase_y_axis(
            current_game.player.game_settings.death_fall_speed,
            False)

        current_game.screen.blit(
            current_game.player.down,
            (current_game.player.x, current_game.player.y)
        )
        current_game.screen.blits(
            obstacles_in_player_path_y
        )

        pygame.display.update()
        current_game.tick_game_fps_clock()

        count += 1
        if count % current_game.player.game_settings.death_acceleration_frequency == 0:
            current_game.player.game_settings.increase_death_fall_speed()
            count = 0

def _is_player_off_screen_bottom(current_game: Game, player_height: int=None):
    """
    Determines if player has fallen below the bottom of the screen.
    If no player_height is specified, it will be calculated for each call.
    """
    player_y = current_game.player.y
    if player_height is None:
        player_height = current_game.player.down.height

    return (player_y > (current_game.player.y_bottom_barrier + player_height))
