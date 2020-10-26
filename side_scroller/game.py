import pygame
from side_scroller.constants import BLACK
from side_scroller.settings import GameSettings, Fonts
from side_scroller.player import Player, Hitbox
from side_scroller.constants import GAME_NAME

class Game():

    def __init__(self):
        self.player = Player(0, Player.y_bottom_barrier)
        #TODO: FULLSCREEN locks player in game window
        self.screen = pygame.display.set_mode((GameSettings.width, GameSettings.height))#, pygame.FULLSCREEN) #TODO: Should we force fullscreen or handle resizing?

        self.game_fps = GameSettings.minFps
        self.fps_clock = pygame.time.Clock()
        self.fps_over_min = 1
        self.per_loop_adjustment = 1

        self.neutral_count = 0
        self.obstacles = list()

        self.initialize_game()

    def initialize_game(self):
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        self.initialize_background()

    def initialize_background(self):
        self.screen.blit(GameSettings.background.image, GameSettings.background.rect)

    def refresh_player_location_background(self):
        self.screen.blit(GameSettings.background.image, self.player.rect, self.player.rect)

    def update_score_hud(self):
        score_text = Fonts.hud_font.render(
            f"Score: {int(self.player.score.score)}", True, BLACK
        )

        self.screen.blit(
            GameSettings.background.image,
            score_text.get_rect(),
            score_text.get_rect())

        self.screen.blit(score_text, score_text.get_rect())

    def update_high_score(self):
        self.player.adjust_high_scores()

    def prepare_new_game(self):
        self.player.prepare_new_game()
        self.obstacles = list()
        self.initialize_background()
        self.neutral_count = 0

    def set_current_fps_over_min_fps(self):
        self.fps_over_min = self.game_fps / GameSettings.minFps

    def set_per_loop_adjustment(self):
        self.per_loop_adjustment = GameSettings.minFps / self.game_fps

    def is_hover_limit_reached(self):
        return self.neutral_count > GameSettings.hoverLimit * self.fps_over_min

    def increase_count_to_obstacle_tick(self):
        self.player.score.countToObstacleTick += self.per_loop_adjustment

    def increase_count_to_level_tick(self):
        self.player.score.countToLevelTick += self.per_loop_adjustment

    def tick_game_fps_clock(self):
        self.fps_clock.tick(self.game_fps)
    
    def get_obstacles_in_player_path_y(self) -> list:
        """
        Returns a list of obstacles that could be hit if the player moved along y axis.
        """
        player_path_y = Hitbox(
            pygame.Rect(
                0,
                0,
                self.player.width,
                10000
            ),
            "neutral"
        )

        return pygame.sprite.spritecollide(player_path_y, self.obstacles, False)
