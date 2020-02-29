import pygame
from side_scroller.settings import GameSettings
from side_scroller.player import Player, DIRECTIONS

def up_key_state(screen, player: Player, fps_over_min: int):
    """ Logic to execute when the up arrow is pressed. Returns updated neutralCount """
    previous_orientation = player.orientation
    player.orientation = DIRECTIONS.get(1)
    if player.y != 0:
        if player.can_move(player.get_current_speed() / fps_over_min, previous_orientation):
            player.decrease_y_axis(player.get_current_speed() + int(player.get_level_speed_boost()))
        player.increase_speed_counter(1, fps_over_min)
    screen.blit(player.up, (player.x, player.y))
    return 0

def down_key_state(screen: pygame.display, player: Player, neutralCount: int, fps_over_min: int):
    """ Logic to execute when the down arrow is pressed. Returns updated neutralCount """
    previous_orientation = player.orientation
    player.orientation = DIRECTIONS.get(2)
    if player.y < Player.y_bottom_barrier:
        if player.can_move(player.get_current_speed() / fps_over_min, previous_orientation):
            player.increase_y_axis(player.get_current_speed() + int(player.get_level_speed_boost()))
        screen.blit(player.down, (player.x, player.y))
    else:
        screen.blit(player.neutral, (player.x, player.y))
    if neutralCount <= (GameSettings.hoverLimit * fps_over_min):
        neutralCount = 0
    player.increase_speed_counter(2, fps_over_min)
    return neutralCount

def neutral_key_state(screen, player: Player, neutralCount: int, fps_over_min: float):
    """ Logic to execute when no relevant key is pressed. Returns updated neutralCount """
    previous_orientation = player.orientation
    if player.get_direction() == DIRECTIONS.get(1):
        player.reset_speed()
        player.orientation = DIRECTIONS.get(0)
        screen.blit(player.neutral, (player.x, player.y))
    elif player.rect.bottom < GameSettings.height:
        if player.can_move(player.get_current_speed(), previous_orientation):
            player.increase_y_axis(player.get_current_speed() + int(player.get_level_speed_boost()))
        player.orientation = DIRECTIONS.get(2)
        screen.blit(player.down, (player.x, player.y))
    else:
        screen.blit(player.neutral, (player.x, player.y))
    return neutralCount + fps_over_min
