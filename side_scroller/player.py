import pygame
from side_scroller.score import Score
from side_scroller.settings import GameSettings
from side_scroller.constants import PLAYER_PATH

DIRECTIONS = {
    0: 'Neutral',
    1: 'Up',
    2: 'Down'}

class SpeedCounter:
    """ Tracks direction and distance traveled. Used to determine object speed. """
    def __init__(self, direction):
        self.count = 0
        self.direction = DIRECTIONS.get(direction)

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, orientation):
        self.rect = rect
        self.orientation = orientation

class Player(pygame.sprite.Sprite):
    up = pygame.image.load(f"{PLAYER_PATH}up_state.png")
    neutral = pygame.image.load(f"{PLAYER_PATH}neutral_state.png")
    down = pygame.image.load(f"{PLAYER_PATH}down_state.png")

    width = max(up.get_width(), neutral.get_width(), down.get_width())
    height = max(up.get_height(), neutral.get_height(), down.get_height())
    y_bottom_barrier = GameSettings.height - height

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, Player.width, Player.height)

        self.hitboxes = [Hitbox(pygame.Rect(x, y, Player.width, Player.height), DIRECTIONS.get(0))]

        #Upstate hitboxes
        self.hitboxes.append(
            Hitbox(pygame.Rect(x, y, Player.width, round(Player.height/2)),
                   DIRECTIONS.get(1)))
        self.hitboxes.append(
            Hitbox(pygame.Rect(x, y, round(Player.width/2), Player.height),
                   DIRECTIONS.get(1)))

        #Downstate hitboxes
        self.hitboxes.append(
            Hitbox(pygame.Rect(x, y + round(Player.height/2), Player.width, round(Player.height/2)),
                   DIRECTIONS.get(2)))
        self.hitboxes.append(
            Hitbox(pygame.Rect(x, y, round(Player.width/2), Player.height),
                   DIRECTIONS.get(2)))

        self.orientation = DIRECTIONS.get(0)
        self.current_speed = 1
        self.level_speed_boost = 0
        self.speed_counter = SpeedCounter(1)
        self.progress_to_move = 0

        self.score = Score()
        self.game_settings = GameSettings()

    def get_current_speed(self):
        return self.current_speed

    def get_level_speed_boost(self):
        return self.level_speed_boost

    def adjust_level_speed_boost(self, adjustment: int):
        self.level_speed_boost += adjustment

    def get_direction(self):
        return self.speed_counter.direction

    def reset_speed(self):
        self.speed_counter.count = 0
        self.current_speed = GameSettings.minSpeed
        self.level_speed_boost = 0
        self.progress_to_move = 0

    def increase_speed_counter(self, direction: int, fps_over_min: float):
        """
            Wrapper for increasing speed counter. If the direction has changed, we'll create a new
            counter and start the count over.
        """
        if self.speed_counter.direction != DIRECTIONS.get(direction):
            self.reset_speed()
            self.speed_counter = SpeedCounter(direction)
        if self.current_speed == GameSettings.maxSpeed:
            return
        self.speed_counter.count += 1
        if (self.speed_counter.count / int(fps_over_min)) % GameSettings.speed_increment_count == 0:
            self.current_speed += 1

    def increase_y_axis(self, val: int):
        """ Move player down. Includes handling to avoid leaving screen. """
        if self.y + val > self.y_bottom_barrier:
            y_adjust = self.y_bottom_barrier - self.y
            self.y = self.y_bottom_barrier
        else:
            y_adjust = val
            self.y += val
        self.rect.move_ip(0, y_adjust)
        for hitbox in self.hitboxes:
            hitbox.rect.move_ip(0, y_adjust)

    def decrease_y_axis(self, val: int):
        """ Move player up. Includes handling to avoid leaving screen. """
        if self.y - val < 0:
            y_adjust = self.y
            self.y = 0
        else:
            y_adjust = val
            self.y -= val
        self.rect.move_ip(0, -y_adjust)
        for hitbox in self.hitboxes:
            hitbox.rect.move_ip(0, -y_adjust)

    def adjust_high_scores(self):
        self.score.set_high_score(self.score.score, True)

    def can_move(self, movement: int, direction: str):
        """
        Checks if player has made enough progress to move a pixel
        and updates progress_to_move accordingly
        RETURNS: True if player can move
        """
        if direction != self.orientation:
            self.progress_to_move = movement
            return False
        self.progress_to_move += movement
        if self.progress_to_move < 1:
            return False
        self.progress_to_move -= 1
        return True

    def is_colliding_with_obstacles(self, obstacles: list) -> bool:
        for hitbox in self.hitboxes:
            if hitbox.orientation == self.orientation:
                if len(pygame.sprite.spritecollide(hitbox, obstacles, False)) > 0:
                    return True
        return False

    def prepare_new_game(self):
        self.reset_speed()
        self.score.reset_score()
        self.game_settings.set_defaults()
