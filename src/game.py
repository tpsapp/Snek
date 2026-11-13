import sys
import pygame
import settings
from fruit import FRUIT
from snake import SNAKE
from pygame.math import Vector2


class GAME:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(
            (settings.width, settings.height))
        pygame.display.set_caption("Snek")
        self.font = pygame.font.Font(settings.font_face, settings.font_size)
        self.small_font = pygame.font.Font(settings.font_face, 24)
        self.score_label_surface = self.font.render("Score:", True, settings.black)

        self.error_sound = self._load_sound(settings.sound_error)
        self.collect_sound = self._load_sound(settings.sound_beep)

        self.is_paused: bool = True
        self.is_game_over: bool = False
        self.score: int = 0
        self.high_score: int = 0

        self.fruit = FRUIT()
        self.snake = SNAKE()

    @property
    def paused(self) -> bool:
        return self.is_paused

    @paused.setter
    def paused(self, value: bool) -> None:
        self.is_paused = value

    def _load_sound(self, path: str):
        if pygame.mixer.get_init():
            try:
                return pygame.mixer.Sound(path)
            except pygame.error:
                return None
        return None

    def play_sound(self, sound) -> None:
        if sound is not None and pygame.mixer.get_init():
            try:
                sound.play()
            except pygame.error:
                pass

    def reset_game(self) -> None:
        self.snake.respawn()
        self.fruit.respawn(self.snake.body)
        self.score = 0
        self.is_game_over = False
        self.is_paused = False

    def draw_elements(self):
        self.screen.fill(settings.green)
        self.snake.draw(self.screen)
        self.fruit.draw(self.screen)
        self.draw_score(self.screen)

        if self.is_game_over:
            self.draw_banner([
                "GAME OVER",
                f"SCORE: {self.score}   HIGH: {self.high_score}",
                "PRESS SPACE TO RESTART"
            ])
        elif self.is_paused and self.score == 0:
            self.draw_banner([
                "SNEK",
                "PRESS ARROWS OR SPACE TO PLAY"
            ])
        elif self.is_paused:
            self.draw_banner([
                "PAUSED",
                "PRESS SPACE TO RESUME"
            ])

    def draw_banner(self, lines: list[str]) -> None:
        overlay = pygame.Surface((settings.width, settings.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        start_y = settings.height // 2 - ((len(lines) - 1) * 22)
        for i, line in enumerate(lines):
            text_surf = self.small_font.render(line, True, settings.white)
            rect = text_surf.get_rect(center=(settings.width // 2, start_y + i * 44))
            overlay.blit(text_surf, rect)
        self.screen.blit(overlay, (0, 0))

    def update(self):
        if self.is_paused or self.is_game_over:
            return
        self.snake.move()
        self.check_collision()

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if key == pygame.K_SPACE:
            if self.is_game_over:
                self.reset_game()
            else:
                self.is_paused = not self.is_paused
            return

        new_direction = None
        if key == pygame.K_UP:
            new_direction = Vector2(0, -1)
        elif key == pygame.K_DOWN:
            new_direction = Vector2(0, 1)
        elif key == pygame.K_LEFT:
            new_direction = Vector2(-1, 0)
        elif key == pygame.K_RIGHT:
            new_direction = Vector2(1, 0)

        if new_direction is not None:
            if self.is_game_over:
                return
            self.is_paused = False
            # Prevent 180-degree self-collision against neck
            if len(self.snake.body) > 1 and (self.snake.body[0] + new_direction) == self.snake.body[1]:
                return
            # Prevent multiple direction changes within a single tick
            if getattr(self.snake, 'direction_changed', False):
                return
            # Prevent opposing axis reversal
            if (new_direction.x != 0 and self.snake.direction.x == -new_direction.x) or \
               (new_direction.y != 0 and self.snake.direction.y == -new_direction.y):
                return
            self.snake.direction = new_direction
            self.snake.direction_changed = True

    def check_collision(self):
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                return

            if block == self.fruit.pos:
                self.fruit.respawn(self.snake.body)

        if not 0 <= self.snake.body[0].x < settings.cell_count or not 0 <= self.snake.body[0].y < settings.cell_count:
            self.game_over()
            return

        if self.snake.body[0] == self.fruit.pos:
            self.score += 1
            self.high_score = max(self.high_score, self.score)
            self.snake.grow()
            self.play_sound(self.collect_sound)
            self.fruit.respawn(self.snake.body)

    def game_over(self):
        self.is_game_over = True
        self.is_paused = True
        self.high_score = max(self.high_score, self.score)
        self.play_sound(self.error_sound)

    def draw_score(self, screen):
        score_text = str(self.score)
        score_surface = self.font.render(score_text, True, settings.black)
        score_x = int(settings.cell_count * settings.cell_size - 64)
        score_y = int(settings.cell_count * settings.cell_size - 32)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        label_rect = self.score_label_surface.get_rect(
            midright=(score_rect.left - 16, score_rect.centery))
        screen.blit(score_surface, score_rect)
        screen.blit(self.score_label_surface, label_rect)

