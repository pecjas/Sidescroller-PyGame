import unittest
import pygame
from side_scroller.player import Player, Hitbox, SpeedCounter, DIRECTIONS
from side_scroller.settings import GameSettings

class PlayerTests(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def tearDown(self):
        pass

    def test_player_rect_has_same_dimensions(self):
        self.assertEqual(self.player.width, self.player.rect.width)
        self.assertEqual(self.player.height, self.player.rect.height)

    def test_get_current_speed(self):
        for i in range(5):
            self.player.current_speed = i
            self.assertEqual(self.player.get_current_speed(), i)

    def test_get_level_speed_boost(self):
        for i in range(5):
            self.player.level_speed_boost = i
            self.assertEqual(self.player.get_level_speed_boost(), i)

    def test_adjust_level_speed_boost(self):
        current_boost = 0
        for i in range(1, 6):
            self.player.adjust_level_speed_boost(i)
            self.assertEqual(self.player.level_speed_boost, current_boost + i)
            current_boost += i

    def test_get_direction(self):
        for direction in DIRECTIONS.values():
            self.player.speed_counter.direction = direction
            self.assertEqual(self.player.get_direction(), direction)

    def test_reset_speed(self):
        self.player.speed_counter.counter = 100
        self.player.current_speed = 100
        self.player.level_speed_boost = 100
        self.player.progress_to_move = 100

        self.player.reset_speed()
        self.assertEqual(self.player.speed_counter.count, 0)
        self.assertEqual(self.player.level_speed_boost, 0)
        self.assertEqual(self.player.progress_to_move, 0)

        self.assertEqual(self.player.current_speed, GameSettings.minSpeed)

    def test_increase_speed_counter_same_direction(self):
        starting_speed_count = 0
        starting_direction = DIRECTIONS.get(1)
        self.player.speed_counter.count = starting_speed_count
        self.player.speed_counter.direction = starting_direction

        self.player.increase_speed_counter(1, 1)

        self.assertEqual(self.player.speed_counter.direction, starting_direction)

    def test_increase_speed_counter_different_direction(self):
        starting_speed_count = 3
        starting_direction = DIRECTIONS.get(1)
        self.player.speed_counter.count = starting_speed_count
        self.player.speed_counter.direction = starting_direction
        self.player.increase_speed_counter(2, 1)

        self.assertNotEqual(self.player.speed_counter.direction, starting_direction)

    def test_increase_speed_counter_at_max_speed(self):
        self.player.current_speed = GameSettings.maxSpeed
        self.player.speed_counter.direction = DIRECTIONS.get(1)

        self.player.increase_speed_counter(1, 1)
        self.assertEqual(self.player.current_speed, GameSettings.maxSpeed)

    def test_increase_y_axis(self):
        previous_y = 0
        self.player.y = previous_y
        self.set_hitbox_y_to_player_y(self.player.hitboxes, previous_y)

        self.player.increase_y_axis(1)
        self.assertGreater(self.player.y, previous_y)
        self.verify_hitbox_y_matches_player_y(self.player.hitboxes, self.player.y)

        previous_y = self.player.y_bottom_barrier - 1
        self.player.y = previous_y
        self.set_hitbox_y_to_player_y(self.player.hitboxes, previous_y)

        self.player.increase_y_axis(5)
        self.assertEqual(self.player.y, self.player.y_bottom_barrier)
        self.verify_hitbox_y_matches_player_y(self.player.hitboxes, self.player.y)

    def test_decrease_y_axis(self):
        previous_y = 400
        self.player.y = previous_y
        self.set_hitbox_y_to_player_y(self.player.hitboxes, previous_y)

        self.player.decrease_y_axis(1)
        self.assertLess(self.player.y, previous_y)
        self.verify_hitbox_y_matches_player_y(self.player.hitboxes, self.player.y)

        previous_y = 1
        self.player.y = previous_y
        self.set_hitbox_y_to_player_y(self.player.hitboxes, previous_y)

        self.player.decrease_y_axis(5)
        self.assertEqual(self.player.y, 0)
        self.verify_hitbox_y_matches_player_y(self.player.hitboxes, self.player.y)

    def set_hitbox_y_to_player_y(self, hitboxes: list, player_y: int):
        for hitbox in hitboxes:
            hitbox.rect.y = player_y

    def verify_hitbox_y_matches_player_y(self, hitboxes: list, player_y: int):
        for hitbox in hitboxes:
            self.assertEqual(hitbox.rect.y, player_y)

    def test_prepare_new_game(self):
        self.player.current_speed = 10
        self.player.score.score = 200
        self.player.game_settings.obstacle_frequency = 10
        self.player.game_settings.obstacle_speed = 10
        self.player.game_settings.game_fps = 60
        self.player.game_settings.fps_over_min = 5

        self.player.prepare_new_game()
        self.assertEqual(self.player.current_speed, GameSettings.minSpeed)
        self.assertEqual(self.player.score.score, 0)

        self.assertEqual(
            self.player.game_settings.obstacle_frequency,
            GameSettings.obstacle_frequency)
        self.assertEqual(self.player.game_settings.obstacle_speed, 0)
        self.assertEqual(self.player.game_settings.game_fps, GameSettings.minFps)
        self.assertEqual(self.player.game_settings.fps_over_min, 1)
