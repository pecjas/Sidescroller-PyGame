import json
from side_scroller.constants import SCORE_PATH

class Score:
    """ Tracks score. Intance tracks a given play's score/level. """
    high_score = {}

    def __init__(self):
        self.score = 0
        self.level = 1
        self.countToObstacleTick = 0
        self.countToLevelTick = 0
        self.countToFrequencyTick = 0

    def get_high_score(self):
        return self.high_score.get('score', 0)

    def reset_score(self):
        """ Reset score and update HIGHSCORE if needed. """
        #TODO: Determine if this can replace adjust_high_score
        if self.score > self.get_high_score():
            self.set_high_score(self.score, True)

        self.score = 0
        self.level = 1

        self.countToObstacleTick = 0
        self.countToLevelTick = 0
        self.countToFrequencyTick = 0

    def set_high_score(self, score: int, save: bool = False):
        """
        Updates high_score if passed in score is higher.

        RETURNS: True if score is higher than previous highscore. Otherwise, False.
        """
        updated = False
        if score > self.get_high_score():
            self.high_score.update({'score': score})
            updated = True
        if updated is True and save is True:
            try:
                json.dump(self.high_score, open(f'{SCORE_PATH}highscore.txt', 'w'))
            except:
                raise Exception("Failed to save highscore to file.")
        return updated

    def load_high_score(self, score_path: str):
        """
        Attempts to load highscore from file.

        RETURNS: highscore info as dictionary. If it's not already within game, retrieves
        from file in same directory.
        """
        try:
            score_file = open(f'{score_path}highscore.txt')
            high_score = json.load(score_file)
            self.set_high_score(high_score.get('score'))
            score_file.close()
        except:
            score_file.close()
            self.high_score = {}

    def increase_score(self, adjustment: int):
        self.score += adjustment
