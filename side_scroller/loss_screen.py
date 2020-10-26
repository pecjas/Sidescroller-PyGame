import pygame
from side_scroller.settings import GameSettings, Fonts
from side_scroller.constants import WHITE, RED, BLACK
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
        screen.fill(BLACK)
        self._draw_boundaries(screen)

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

    def _draw_boundaries(self, screen: pygame.surface):
        horizontal_bar_height = GameSettings.loss_screen.get("horizontal_bar_height")
        vertical_bar_width = GameSettings.loss_screen.get("vertical_bar_width")

        red_bars = {
            "top": pygame.Rect(
                0,
                0,
                GameSettings.width,
                horizontal_bar_height
            ),
            "bottom": pygame.Rect(
                0,
                GameSettings.height - horizontal_bar_height,
                GameSettings.width,
                horizontal_bar_height
            ),
            "left": pygame.Rect(
                0,
                0,
                vertical_bar_width,
                GameSettings.height
            ),
            "right": pygame.Rect(
                GameSettings.width - vertical_bar_width,
                0,
                vertical_bar_width,
                GameSettings.height
            )
        }

        for rect in red_bars.values():
            pygame.draw.rect(
                screen,
                RED,
                rect
            )
