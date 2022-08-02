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
        self.font = pygame.font.Font(settings.font_face, settings.font_size)
        self.error_sound = pygame.mixer.Sound('src/Sounds/error.wav')
        self.fruit = FRUIT()
        self.snake = SNAKE()

    def draw_elements(self):
        self.screen.fill(settings.green)
        self.snake.draw(self.screen)
        self.fruit.draw(self.screen)
        self.draw_score(self.screen)

    def update(self):
        if settings.paused:
            return
        self.snake.move()
        self.check_collision()

    def handle_keydown(self, key):
        settings.paused = False
        if key == pygame.K_UP:
            if self.snake.direction.y != 1:
                self.snake.direction = Vector2(0, -1)
        elif key == pygame.K_DOWN:
            if self.snake.direction.y != -1:
                self.snake.direction = Vector2(0, 1)
        elif key == pygame.K_LEFT:
            if self.snake.direction.x != 1:
                self.snake.direction = Vector2(-1, 0)
        elif key == pygame.K_RIGHT:
            if self.snake.direction.x != -1:
                self.snake.direction = Vector2(1, 0)

        if key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if key == pygame.K_SPACE:
            settings.paused = not settings.paused

    def check_collision(self):
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

            if block == self.fruit.pos:
                self.fruit.respawn()

        if not 0 <= self.snake.body[0].x < settings.cell_count or not 0 <= self.snake.body[0].y < settings.cell_count:
            self.game_over()

        if self.snake.body[0] == self.fruit.pos:
            self.snake.grow()
            self.fruit.respawn()

    def game_over(self):
        settings.paused = True
        self.error_sound.play()
        self.snake.respawn()

    def draw_score(self, screen):
        score_text = str(len(self.snake.body) - 3)
        score_surface = self.font.render(score_text, True, settings.black)
        label_surface = self.font.render("Score:", True, settings.black)
        score_x = int(settings.cell_count * settings.cell_size - 64)
        score_y = int(settings.cell_count * settings.cell_size - 32)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        label_rect = label_surface.get_rect(
            midright=(score_rect.left - 16, score_rect.centery))
        screen.blit(score_surface, score_rect)
        screen.blit(label_surface, label_rect)
