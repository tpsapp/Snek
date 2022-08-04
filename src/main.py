import pygame
import sys
import settings
from game import GAME

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

clock = pygame.time.Clock()
game = GAME()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, settings.timer_rate)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            game.handle_keydown(event.key)

    game.draw_elements()
    pygame.display.update()
    clock.tick(settings.framerate)
