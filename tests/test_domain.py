import os
import sys
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import pygame
from pygame.math import Vector2
import settings
from snake import SNAKE
from fruit import FRUIT
from game import GAME


class TestSnekDomain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

    def setUp(self):
        self.game = GAME()

    def test_tc01_forward_movement(self):
        """TC-01: Snake moves forward in current direction, shifting segments."""
        snake = SNAKE()
        self.assertEqual(snake.body, [Vector2(11, 10), Vector2(10, 10), Vector2(9, 10)])
        snake.move()
        self.assertEqual(snake.body, [Vector2(12, 10), Vector2(11, 10), Vector2(10, 10)])
        self.assertEqual(len(snake.body), 3)

    def test_tc02_growth_expands_body(self):
        """TC-02: grow() then move() expands body length by 1 and resets add_section."""
        snake = SNAKE()
        snake.grow()
        self.assertTrue(snake.add_section)
        snake.move()
        self.assertEqual(len(snake.body), 4)
        self.assertFalse(snake.add_section)
        self.assertEqual(snake.body[0], Vector2(12, 10))
        self.assertEqual(snake.body[-1], Vector2(9, 10))

    def test_tc03_wall_collision_left(self):
        """TC-03: Snake head at x = -1 triggers game_over."""
        self.game.is_paused = False
        self.game.snake.body[0] = Vector2(-1, 10)
        self.game.check_collision()
        self.assertTrue(self.game.is_game_over)
        self.assertTrue(self.game.is_paused)

    def test_tc04_wall_collision_right(self):
        """TC-04: Snake head at x = cell_count triggers game_over."""
        self.game.is_paused = False
        self.game.snake.body[0] = Vector2(settings.cell_count, 10)
        self.game.check_collision()
        self.assertTrue(self.game.is_game_over)

    def test_tc05_wall_collision_top(self):
        """TC-05: Snake head at y = -1 triggers game_over."""
        self.game.is_paused = False
        self.game.snake.body[0] = Vector2(10, -1)
        self.game.check_collision()
        self.assertTrue(self.game.is_game_over)

    def test_tc06_wall_collision_bottom(self):
        """TC-06: Snake head at y = cell_count triggers game_over."""
        self.game.is_paused = False
        self.game.snake.body[0] = Vector2(10, settings.cell_count)
        self.game.check_collision()
        self.assertTrue(self.game.is_game_over)

    def test_tc07_self_collision_triggers_game_over(self):
        """TC-07: Snake head intersecting body[3] triggers game_over."""
        self.game.is_paused = False
        # Create a 5-block body where head loops back onto block 4
        self.game.snake.body = [
            Vector2(10, 10),
            Vector2(11, 10),
            Vector2(11, 11),
            Vector2(10, 11),
            Vector2(10, 10)
        ]
        self.game.check_collision()
        self.assertTrue(self.game.is_game_over)

    def test_tc08_neck_reversal_rejection(self):
        """TC-08: Attempting to move into snake.body[1] (180° turn) is rejected."""
        self.game.is_paused = False
        self.assertEqual(self.game.snake.direction, Vector2(1, 0))
        # Moving LEFT is directly opposite neck at (10, 10)
        self.game.handle_keydown(pygame.K_LEFT)
        self.assertEqual(self.game.snake.direction, Vector2(1, 0))

    def test_tc09_single_tick_direction_lock(self):
        """TC-09: Only one directional shift allowed per game update tick."""
        self.game.is_paused = False
        self.game.handle_keydown(pygame.K_UP)
        self.assertEqual(self.game.snake.direction, Vector2(0, -1))
        # Second direction within same tick is ignored
        self.game.handle_keydown(pygame.K_RIGHT)
        self.assertEqual(self.game.snake.direction, Vector2(0, -1))

        # After update(), direction lock resets
        self.game.update()
        self.game.handle_keydown(pygame.K_RIGHT)
        self.assertEqual(self.game.snake.direction, Vector2(1, 0))

    def test_tc10_fruit_spawn_non_overlap(self):
        """TC-10: fruit.respawn(occupied) never spawns inside occupied cells."""
        fruit = FRUIT()
        occupied = [Vector2(x, y) for x in range(10) for y in range(10)]
        for _ in range(100):
            result = fruit.respawn(occupied)
            self.assertTrue(result)
            self.assertNotIn(fruit.pos, occupied)

    def test_tc11_grid_saturation_handling(self):
        """TC-11: Full grid saturation returns False safely without infinite loop."""
        fruit = FRUIT()
        all_cells = [
            Vector2(x, y)
            for x in range(settings.cell_count)
            for y in range(settings.cell_count)
        ]
        result = fruit.respawn(all_cells)
        self.assertFalse(result)

    def test_tc12_space_toggles_pause_and_halts_movement(self):
        """TC-12: K_SPACE when running pauses game and halts movement updates."""
        self.game.is_paused = False
        initial_head = Vector2(self.game.snake.body[0])
        self.game.handle_keydown(pygame.K_SPACE)
        self.assertTrue(self.game.is_paused)

        self.game.update()
        self.assertEqual(self.game.snake.body[0], initial_head)

    def test_tc13_space_unpauses_game(self):
        """TC-13: K_SPACE when paused unpauses the game and allows updates."""
        self.game.is_paused = True
        initial_head = Vector2(self.game.snake.body[0])
        self.game.handle_keydown(pygame.K_SPACE)
        self.assertFalse(self.game.is_paused)

        self.game.update()
        self.assertNotEqual(self.game.snake.body[0], initial_head)

    def test_tc14_game_over_preserves_score_until_space_restart(self):
        """TC-14: Game over preserves score and high score; K_SPACE resets game."""
        self.game.is_paused = False
        self.game.score = 5
        self.game.snake.body[0] = Vector2(-1, 0)
        self.game.check_collision()

        self.assertTrue(self.game.is_game_over)
        self.assertEqual(self.game.score, 5)
        self.assertEqual(self.game.high_score, 5)

        # Press space to restart
        self.game.handle_keydown(pygame.K_SPACE)
        self.assertFalse(self.game.is_game_over)
        self.assertFalse(self.game.is_paused)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.high_score, 5)  # High score preserved
        self.assertEqual(len(self.game.snake.body), 3)

    def test_tc15_headless_pure_domain_isolation(self):
        """TC-15: SNAKE and FRUIT operate purely in-memory without audio mixer or display."""
        snake = SNAKE()
        fruit = FRUIT()
        snake.move()
        snake.grow()
        snake.move()
        self.assertEqual(len(snake.body), 4)
        fruit.respawn(snake.body)
        self.assertNotIn(fruit.pos, snake.body)


if __name__ == "__main__":
    unittest.main()
