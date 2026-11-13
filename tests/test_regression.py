import os
import sys
import unittest

# Ensure headless execution before pygame imports
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Add src to path
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import pygame
import settings
from fruit import FRUIT
from snake import SNAKE
from game import GAME
from pygame.math import Vector2


class TestSnekRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

    def setUp(self):
        self.game = GAME()
        self.game.is_paused = True

    def test_fix_01_spacebar_unpause(self):
        """FIX-01: Pressing SPACE when paused must unpause the game."""
        self.game.is_paused = True
        self.game.handle_keydown(pygame.K_SPACE)
        self.assertFalse(self.game.is_paused, "Pressing SPACE while paused failed to unpause the game")

    def test_fix_02_rapid_key_180_reversal(self):
        """FIX-02: Rapid perpendicular inputs in a single tick must not cause 180° suicide."""
        # Initial snake is at [(11, 10), (10, 10), (9, 10)], direction is (1, 0) (RIGHT)
        self.game.is_paused = False
        # Rapidly press UP then LEFT before update tick
        self.game.handle_keydown(pygame.K_UP)
        self.game.handle_keydown(pygame.K_LEFT)

        # Update should NOT crash into its own body from 180 degree reversal
        self.game.update()
        self.assertFalse(
            self.game.is_game_over,
            "Rapid perpendicular keys caused snake to reverse 180° into its neck and die"
        )

    def test_fix_03_collision_fallthrough_post_game_over(self):
        """FIX-03: game_over() in check_collision must immediately return without processing fruit."""
        self.game.is_paused = False
        # Place fruit at head position
        self.game.fruit.pos = Vector2(11, 10)
        # Move snake head out of bounds to trigger wall collision game_over
        self.game.snake.body[0] = Vector2(-1, 10)

        self.game.check_collision()

        # game_over should be triggered
        self.assertTrue(self.game.is_game_over)
        # It must NOT have consumed the fruit at (11, 10)
        self.assertFalse(
            self.game.snake.add_section,
            "Snake erroneously consumed fruit on the same frame it died"
        )
        self.assertEqual(self.game.score, 0)

    def test_fix_04_fruit_spawns_outside_snake_body(self):
        """FIX-04: fruit.respawn() must never spawn on top of snake body cells."""
        fruit = FRUIT()
        occupied = [Vector2(x, y) for x in range(10) for y in range(10)]
        # Respawn 100 times, none should fall inside occupied
        for _ in range(100):
            fruit.respawn(occupied)
            self.assertNotIn(
                fruit.pos,
                occupied,
                f"Fruit spawned on occupied cell: {fruit.pos}"
            )

    def test_fix_05_asset_paths_resolve_outside_root(self):
        """FIX-05: Loading assets should succeed even if CWD is changed to src/."""
        orig_cwd = os.getcwd()
        try:
            os.chdir(SRC_DIR)
            # Re-verifying asset path resolution
            font = pygame.font.Font(settings.font_face, settings.font_size)
            self.assertIsNotNone(font)
            sound = pygame.mixer.Sound(settings.sound_beep if hasattr(settings, 'sound_beep') else 'src/Sounds/beep.wav')
            self.assertIsNotNone(sound)
        finally:
            os.chdir(orig_cwd)


if __name__ == "__main__":
    unittest.main()
