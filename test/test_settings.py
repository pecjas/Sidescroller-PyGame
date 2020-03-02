import unittest
import pygame
from side_scroller.settings import GameSettings, Background

class SettingsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_set_defaults(self):
        game_settings_default = GameSettings()
        game_settings_changed = GameSettings()

        change_game_settings_instance_variables(game_settings_changed)
        game_settings_changed.set_defaults()

        attribute_list = get_game_setting_attributes(game_settings_changed)
        for attribute in attribute_list:
            self.assertEqual(
                getattr(game_settings_changed, attribute),
                getattr(game_settings_default, attribute))

    def test_background_rect_size(self):
        background = Background("background.jpg")
        self.assertEqual(background.rect.width, GameSettings.width)
        self.assertEqual(background.rect.height, GameSettings.height)

    def test_background_position(self):
        background = Background("background.jpg")
        self.assertEqual(background.rect.left, 0)
        self.assertEqual(background.rect.top, 0)

def change_game_settings_instance_variables(game_settings: GameSettings):
    game_settings.obstacle_frequency = 300
    game_settings.obstacle_speed = 5
    game_settings.game_fps = 5676
    game_settings.fps_over_min = 34

def get_game_setting_attributes(game_settings: GameSettings):
    return [a for a in dir(game_settings)
            if not a.startswith('__') and not
            str(getattr(game_settings, a)).startswith('<bound method')]
