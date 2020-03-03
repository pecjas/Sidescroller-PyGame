import unittest
import pygame
from side_scroller.settings import GameSettings
from side_scroller.game import Game
import side_scroller.side_scroller as side_scroller

def get_current_count_to_obstacle_tick(game: Game):
    return game.player.score.countToObstacleTick

def get_current_count_to_level_tick(game: Game):
    return game.player.score.countToLevelTick

def get_current_level(game: Game):
    return game.player.score.level

def get_game_fps(game: Game):
    return game.game_fps

def get_obstacle_frequency(game: Game):
    return game.player.game_settings.obstacle_frequency

def get_obstacle_speed(game: Game):
    return game.player.game_settings.obstacle_speed

def set_count_to_obstacle_tick(game: Game, new_count: int):
    game.player.score.countToObstacleTick = new_count

def set_count_to_level_tick(game: Game, new_count: int):
    game.player.score.countToLevelTick = new_count

def set_count_to_frequency_tick(game: Game, new_count: int):
    game.player.score.countToFrequencyTick = new_count

def set_game_fps(game: Game, new_fps: int):
    game.game_fps = new_fps

def set_obstacle_frequency(game: Game, new_frequency: int):
    game.player.game_settings.obstacle_frequency = new_frequency

class SideScrollerTest(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def tearDown(self):
        pass

    def test_tick_adjustment_increases_counts(self):
        initial_count_to_obstacle_tick = get_current_count_to_obstacle_tick(self.game)
        initial_count_to_level_tick = get_current_count_to_level_tick(self.game)

        side_scroller.tick_adjustments(self.game)

        self.assertGreater(get_current_count_to_obstacle_tick(self.game), initial_count_to_obstacle_tick)
        self.assertGreater(get_current_count_to_level_tick(self.game), initial_count_to_level_tick)

    def test_if_necessary_add_obstacle_when_not_necessary(self):
        original_obstacle_count = len(self.game.obstacles)
        set_count_to_obstacle_tick(
            self.game,
            self.game.player.game_settings.obstacle_frequency - 1)

        side_scroller.tick_adjustments(self.game)

        self.assertEqual(len(self.game.obstacles), original_obstacle_count)

    def test_if_necessary_add_obstacle_when_necessary(self):
        original_obstacle_count = len(self.game.obstacles)
        set_count_to_obstacle_tick(
            self.game,
            self.game.player.game_settings.obstacle_frequency + 1)

        side_scroller.tick_adjustments(self.game)

        self.assertGreater(len(self.game.obstacles), original_obstacle_count)

    def test_if_necessary_increase_level_when_not_necessary(self):
        original_level = get_current_level(self.game)
        set_count_to_level_tick(
            self.game,
            GameSettings.levelTick - 1)

        side_scroller.tick_adjustments(self.game)

        self.assertEqual(get_current_level(self.game), original_level)

    def test_if_necessary_increase_level_when_necessary(self):
        original_level = get_current_level(self.game)
        set_count_to_level_tick(
            self.game,
            GameSettings.levelTick + 1)

        side_scroller.tick_adjustments(self.game)

        self.assertGreater(get_current_level(self.game), original_level)

    def test_increase_obstacle_speed_before_max_fps(self):
        original_fps = get_game_fps(self.game)
        original_obstacle_speed = get_obstacle_speed(self.game)

        side_scroller.increase_obstacle_speed(self.game)

        self.assertGreater(get_game_fps(self.game), original_fps)
        self.assertEqual(get_obstacle_speed(self.game), original_obstacle_speed)

    def test_increase_obstacle_speed_after_max_fps(self):
        set_game_fps(self.game, GameSettings.maxFps)
        original_fps = get_game_fps(self.game)
        original_obstacle_speed = get_obstacle_speed(self.game)

        side_scroller.increase_obstacle_speed(self.game)

        self.assertEqual(get_game_fps(self.game), original_fps)
        self.assertGreater(get_obstacle_speed(self.game), original_obstacle_speed)

    def test_if_necessary_increase_obstacle_frequency_when_not_necessary(self):
        original_obstacle_frequency = get_obstacle_frequency(self.game)
        set_count_to_frequency_tick(self.game, GameSettings.frequencyTick - 1)

        side_scroller.if_necessary_increase_obstacle_frequency(self.game)
        self.assertEqual(get_obstacle_frequency(self.game), original_obstacle_frequency)

    def test_if_necessary_increase_obstacle_frequency_when_necessary(self):
        set_obstacle_frequency(self.game, GameSettings.obstacle_tick_adjustment + 1)
        original_obstacle_frequency = get_obstacle_frequency(self.game)
        set_count_to_frequency_tick(self.game, GameSettings.frequencyTick + 1)

        side_scroller.if_necessary_increase_obstacle_frequency(self.game)
        self.assertLess(get_obstacle_frequency(self.game), original_obstacle_frequency)

        set_obstacle_frequency(self.game, GameSettings.obstacle_tick_adjustment - 1)
        original_obstacle_frequency = get_obstacle_frequency(self.game)
        set_count_to_frequency_tick(self.game, GameSettings.frequencyTick + 1)

        side_scroller.if_necessary_increase_obstacle_frequency(self.game)
        #Lower means more frequent
        self.assertLess(get_obstacle_frequency(self.game), original_obstacle_frequency)
