import unittest
from side_scroller.score import Score

class ScoreTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_increase_score(self):
        score = Score()
        current_score = score.score
        for i in range(1, 10):
            score.increase_score(i)
            self.assertEqual(score.score, current_score + i)
            current_score = score.score

    def test_load_high_score(self):
        score = Score()
        score.load_high_score("test/score/")
        self.assertEqual(score.get_high_score(), 795.14)

    def test_set_high_score(self):
        score = Score()
        test_score = 100000000
        score.set_high_score(test_score)
        self.assertEqual(score.get_high_score(), test_score)

    def test_reset_score(self):
        score = Score()

        score.score = 5
        score.level = 3

        score.countToObstacleTick = 4
        score.countToLevelTick = 1
        score.countToFrequencyTick = 3

        score.reset_score()

        self.assertEqual(score.score, 0)
        self.assertEqual(score.level, 1)

        self.assertEqual(score.countToObstacleTick, 0)
        self.assertEqual(score.countToLevelTick, 0)
        self.assertEqual(score.countToFrequencyTick, 0)
