import pygame
import settings
from pygame.math import Vector2


class SNAKE:
    def __init__(self) -> None:
        self.respawn()

    def respawn(self):
        self.body = [Vector2(11, 10), Vector2(10, 10), Vector2(9, 10)]
        self.direction = Vector2(1, 0)
        self.add_section = False
        self.direction_changed = False

    def draw(self, screen):
        for block in self.body:
            block_rect = pygame.Rect(
                int(block.x * settings.cell_size), int(block.y * settings.cell_size), settings.cell_size, settings.cell_size)
            pygame.draw.rect(screen, settings.blue, block_rect)

    def move(self):
        self.direction_changed = False
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_section:
            self.add_section = False
        else:
            self.body.pop()

    def grow(self):
        self.add_section = True
