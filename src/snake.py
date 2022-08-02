import pygame
import settings
from pygame.math import Vector2


class SNAKE:
    def __init__(self) -> None:
        self.respawn()
        self.collect_sound = pygame.mixer.Sound('src/Sounds/beep.wav')

    def respawn(self):
        self.body = [Vector2(11, 10), Vector2(10, 10), Vector2(9, 10)]
        self.direction = Vector2(1, 0)
        self.add_section = False

    def draw(self, screen):
        for block in self.body:
            block_rect = pygame.Rect(
                int(block.x * settings.cell_size), int(block.y * settings.cell_size), settings.cell_size, settings.cell_size)
            pygame.draw.rect(screen, settings.blue, block_rect)

    def move(self):
        if self.add_section == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.add_section = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def grow(self):
        self.add_section = True
        self.collect_sound.play()
