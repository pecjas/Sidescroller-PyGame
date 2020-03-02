import unittest
import pygame
from side_scroller.game import Game
from side_scroller.player import Player
from side_scroller.settings import GameSettings

def close_display_window():
    pygame.display.quit()
    pygame.quit()

class GameTests(unittest.TestCase):

    game = Game()
    close_display_window()

    def setUp(self):
        pass

    def test_set_per_loop_adjustment(self):
        for i in range(1, 5):
            self.game.game_fps += i
            self.game.set_per_loop_adjustment()

            self.assertEqual(
                self.game.per_loop_adjustment,
                GameSettings.minFps / self.game.game_fps)

    def test_set_current_fps_over_min_fps(self):
        for i in range(1, 5):
            self.game.game_fps += i
            self.game.set_current_fps_over_min_fps()

            self.assertEqual(
                self.game.fps_over_min,
                self.game.game_fps / GameSettings.minFps)

    def test_is_hover_limit_reached(self):
        self.game.neutral_count = GameSettings.hoverLimit - 1
        self.assertFalse(self.game.is_hover_limit_reached())

        self.game.neutral_count += 1
        self.assertFalse(self.game.is_hover_limit_reached())

        self.game.neutral_count += 1
        self.assertTrue(self.game.is_hover_limit_reached())
