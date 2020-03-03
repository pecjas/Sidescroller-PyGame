import unittest
import pygame
from side_scroller.obstacle import Obstacle, move_obstacles
from side_scroller.game import Game

class ObstacleTests(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.obstacles = list()

    def test_move_obstacles_all_on_screen(self):
        x_coordinates = [100, 200, 300]
        for i in x_coordinates:
            self.append_obstacle_at_coordinate(i, 300)

        move_obstacles(self.game)
        self.assertEqual(len(self.game.obstacles), len(x_coordinates))

    def test_move_obstacles_all_off_screen(self):
        x_coordinates = [-1000, -1500, -2000]
        for i in x_coordinates:
            self.append_obstacle_at_coordinate(i, 300)

        move_obstacles(self.game)
        self.assertEqual(len(self.game.obstacles), 0)

    def test_move_obstacles_some_on_screen(self):
        x_coordinates = [-2000, 0, 200]
        for i in x_coordinates:
            self.append_obstacle_at_coordinate(i, 300)

        move_obstacles(self.game)
        self.assertEqual(len(self.game.obstacles), 2)

    def append_obstacle_at_coordinate(self, x: int, y: int):
        self.game.obstacles.append(Obstacle(x, y))
