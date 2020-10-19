import pygame
from side_scroller.game import Game
from side_scroller.settings import GameSettings
from side_scroller.player import Player, DIRECTIONS

def should_pause_game(keys: list) -> bool:
    return keys[pygame.K_ESCAPE]

def is_player_moving_up(keys: list) -> bool:
    return keys[pygame.K_UP]

def up_key_state(game: Game):
    """ Logic to execute when the up arrow is pressed. Returns updated neutral_count """
    player = game.player
    previous_orientation = player.orientation
    player.orientation = DIRECTIONS.get(1)
    if player.y != 0:
        if player.can_move(player.get_current_speed() / game.fps_over_min, previous_orientation):
            player.decrease_y_axis(
                player.get_current_speed() + int(player.get_level_speed_boost()))
        player.increase_speed_counter(1, game.fps_over_min)
    game.screen.blit(player.up, (player.x, player.y))
    return 0

def is_player_moving_down(keys: list, game: Game) -> bool:
    return keys[pygame.K_DOWN] or game.is_hover_limit_reached()

def down_key_state(game: Game):
    """ Logic to execute when the down arrow is pressed. Returns updated neutral_count """
    player = game.player
    previous_orientation = player.orientation
    player.orientation = DIRECTIONS.get(2)
    if player.y < Player.y_bottom_barrier:
        if player.can_move(player.get_current_speed() / game.fps_over_min, previous_orientation):
            player.increase_y_axis(player.get_current_speed() + int(player.get_level_speed_boost()))
        game.screen.blit(player.down, (player.x, player.y))
    else:
        game.screen.blit(player.neutral, (player.x, player.y))
    if game.neutral_count <= (GameSettings.hoverLimit * game.fps_over_min):
        game.neutral_count = 0
    player.increase_speed_counter(2, game.fps_over_min)
    return game.neutral_count

def neutral_key_state(game: Game):
    """ Logic to execute when no relevant key is pressed. Returns updated neutral_count """
    player = game.player
    previous_orientation = player.orientation
    if player.get_direction() == DIRECTIONS.get(1):
        player.reset_speed()
        player.orientation = DIRECTIONS.get(0)
        game.screen.blit(player.neutral, (player.x, player.y))
    elif player.rect.bottom < GameSettings.height:
        if player.can_move(player.get_current_speed(), previous_orientation):
            player.increase_y_axis(player.get_current_speed() + int(player.get_level_speed_boost()))
        player.orientation = DIRECTIONS.get(2)
        game.screen.blit(player.down, (player.x, player.y))
    else:
        game.screen.blit(player.neutral, (player.x, player.y))
    return game.neutral_count + game.fps_over_min
