import unittest
import pygame
from side_scroller.game import Game
from side_scroller.player import Player, DIRECTIONS
from side_scroller.states import (is_player_moving_up, is_player_moving_down, up_key_state,
                                  down_key_state, neutral_key_state)

def close_display_window():
    pygame.display.quit()
    pygame.quit()

class StatesTest(unittest.TestCase):

    game = Game()
    close_display_window()

    def setUp(self):
        pygame.init()
        self.game.fps_over_min = 1
        self.game.player.current_speed = 1

    def tearDown(self):
        close_display_window()

    def test_is_player_moving_up(self):
        keys = pygame.key.get_pressed()
        self.assertFalse(is_player_moving_up(keys))

        keys = mock_key_press(pygame.K_UP)
        self.assertTrue(is_player_moving_up(keys))

    def test_is_player_moving_down(self):
        keys = pygame.key.get_pressed()
        self.assertFalse(is_player_moving_down(keys, self.game))

        keys = mock_key_press(pygame.K_DOWN)
        self.assertTrue(is_player_moving_down(keys, self.game))

    def test_up_key_state_return(self):
        open_game = Game()
        self.assertEqual(up_key_state(open_game), 0)

    def test_down_key_state_return(self):
        open_game = Game()
        test_neutral_count = 1000
        open_game.neutral_count = test_neutral_count
        self.assertEqual(down_key_state(open_game), test_neutral_count)

        open_game.neutral_count = 1
        self.assertEqual(down_key_state(open_game), 0)
        close_display_window()

    def test_neutral_key_state_return(self):
        open_game = Game()
        open_game.neutral_count = 0
        self.assertEqual(
            neutral_key_state(open_game),
            open_game.neutral_count + open_game.fps_over_min)
        close_display_window()

    def test_up_key_state_moves_up_when_possible(self):
        open_game = Game()
        open_game.player.y = Player.y_bottom_barrier
        open_game.player.orientation = DIRECTIONS.get(1) #Up
        original_y = open_game.player.y

        up_key_state(open_game)
        self.assertLess(open_game.player.y, original_y)
        close_display_window()

    def test_up_key_state_stays_when_movement_impossible(self):
        open_game = Game()
        open_game.player.y = 0
        up_key_state(open_game)
        self.assertEqual(open_game.player.y, 0)

        open_game.player.y = open_game.player.y_bottom_barrier
        open_game.player.orientation = DIRECTIONS.get(2) #Down
        up_key_state(open_game)
        self.assertEqual(open_game.player.y, open_game.player.y_bottom_barrier)

    def test_down_key_state_moves_down_when_possible(self):
        open_game = Game()
        open_game.player.y = 0
        open_game.player.orientation = DIRECTIONS.get(2) #Down
        original_y = open_game.player.y

        down_key_state(open_game)
        self.assertGreater(open_game.player.y, original_y)
        close_display_window()

    def test_down_key_state_stays_when_movement_impossible(self):
        open_game = Game()
        open_game.player.y = 0
        up_key_state(open_game)
        self.assertEqual(open_game.player.y, 0)

        open_game.player.y = open_game.player.y_bottom_barrier
        open_game.player.orientation = DIRECTIONS.get(2) #Down
        up_key_state(open_game)
        self.assertEqual(open_game.player.y, open_game.player.y_bottom_barrier)
        close_display_window()

    def test_neutral_key_state_when_oriented_up(self):
        open_game = Game()
        open_game.player.orientation = DIRECTIONS.get(1) #Up
        neutral_key_state(open_game)
        self.assertEqual(open_game.player.orientation, DIRECTIONS.get(0))

    def test_neutral_key_state_when_not_oriented_up(self):
        open_game = Game()

        open_game.player.orientation = DIRECTIONS.get(2) #Down
        neutral_key_state(open_game)

        self.assertNotEqual(open_game.player.orientation, DIRECTIONS.get(1))
        close_display_window()

def mock_key_press(pressed_key):
    keys = [0] * 300
    keys[pressed_key] = 1
    return keys
