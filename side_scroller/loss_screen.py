import pygame
from side_scroller.settings import GameSettings, Fonts
from side_scroller.constants import WHITE
from side_scroller.player import Player
from side_scroller.score import Score

class LossScreen():

    def __init__(self, player: Player):
        self.loss_text = Fonts.loss_font.render("Game Over", True, WHITE)
        self.retry_text = Fonts.retry_font.render("Press Enter to try again.", True, WHITE)
        self.high_score_text = Fonts.high_score_font.render(
            f"High Score: {int(Score.high_score.get('score'))}",
            True,
            WHITE)

        self.score_text = Fonts.score_font.render(
            f"Your Score: {int(player.score.score)}",
            True,
            WHITE)

    def display(self, screen: pygame.surface):
        screen.blit(GameSettings.lossScreen.image, GameSettings.lossScreen.rect)
        screen.blit(self.loss_text,
                    self.loss_text.get_rect(
                        center=(int(GameSettings.width/2), int(GameSettings.height/4))))

        screen.blit(self.high_score_text,
                    self.high_score_text.get_rect(
                        center=(int(GameSettings.width/2), int(GameSettings.height/3))))

        screen.blit(self.score_text,
                    self.score_text.get_rect(
                        center=(int(GameSettings.width/2), int(GameSettings.height/2))))

        screen.blit(self.retry_text,
                    self.retry_text.get_rect(
                        center=(int(GameSettings.width/2),
                                int(GameSettings.height/2 + self.score_text.get_height()))))
        pygame.display.update()
