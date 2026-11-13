import pygame
import random
import settings
from pygame.math import Vector2


class FRUIT:
    def __init__(self) -> None:
        self.respawn()

    def respawn(self, occupied=None):
        if occupied:
            occupied_coords = {(int(pos.x), int(pos.y)) for pos in occupied}
            available = [
                (x, y)
                for x in range(settings.cell_count)
                for y in range(settings.cell_count)
                if (x, y) not in occupied_coords
            ]
            if not available:
                return False
            self.x, self.y = random.choice(available)
        else:
            self.x = random.randint(0, settings.cell_count - 1)
            self.y = random.randint(0, settings.cell_count - 1)
        self.pos = Vector2(self.x, self.y)
        return True

    def draw(self, screen):
        fruit_rect = pygame.Rect(int(self.pos.x * settings.cell_size), int(self.pos.y *
                                 settings.cell_size), settings.cell_size, settings.cell_size)
        pygame.draw.rect(screen, settings.red, fruit_rect)
