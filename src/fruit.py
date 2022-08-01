import pygame
import random
import settings
from pygame.math import Vector2


class FRUIT:
    def __init__(self) -> None:
        self.respawn()

    def respawn(self):
        self.x = random.randint(0, settings.cell_count - 1)
        self.y = random.randint(0, settings.cell_count - 1)
        self.pos = Vector2(self.x, self.y)

    def draw(self, screen):
        fruit_rect = pygame.Rect(int(self.pos.x * settings.cell_size), int(self.pos.y *
                                 settings.cell_size), settings.cell_size, settings.cell_size)
        pygame.draw.rect(screen, settings.red, fruit_rect)
