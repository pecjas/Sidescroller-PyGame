import pygame
from side_scroller.settings import GameSettings, Fonts
from side_scroller.constants import WHITE, BLACK, TINT_ALPHA_PAUSE
from side_scroller.player import Player
from side_scroller.score import Score

class PauseScreen():

    def __init__(self):
        self.pause_text1 = Fonts.pause_font.render("Paused", True, WHITE)
        self.pause_text2 = Fonts.pause_font.render("Press Enter to continue", True, WHITE)

        self.previous_screen = None

    def tint_screen(self, screen: pygame.surface, tint_color):
        display_tint = pygame.Surface(screen.get_size())
        display_tint.fill(tint_color)
        display_tint.set_alpha(TINT_ALPHA_PAUSE)

        screen.blit(display_tint, (0, 0))

    def display(self, screen: pygame.surface):
        self.previous_screen = screen.copy()

        self.tint_screen(screen, BLACK)

        screen.blit(self.pause_text1,
                    self.pause_text1.get_rect(
                        center=(int(GameSettings.width/2), int(GameSettings.height/4))
                    ))

        screen.blit(self.pause_text2,
                    self.pause_text2.get_rect(
                        center=(int(GameSettings.width/2), int(GameSettings.height/2))))
        pygame.display.update()

    def undisplay(self, screen: pygame.surface):
        screen.blit(self.previous_screen, (0, 0))
