# Snek

A classic grid-based Snake game clone written in Python and Pygame, built with clean domain separation, robust input handling, and automated test coverage.

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-%3E%3D2.0.0-green.svg)
![Tests](https://img.shields.io/badge/tests-20%20passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-orange.svg)

---

## Features

- **Decoupled Architecture:** Core simulation models (`snake.py`, `fruit.py`) run headlessly without display or audio dependencies.
- **Robust Input Handling:** Single-tick input lock and neck-collision guards eliminate 180° accidental self-suicide.
- **Vacancy-Guaranteed Fruit Spawning:** Prevents fruit from overlapping the snake's body, handling board saturation gracefully.
- **Visual Overlays & Score Tracking:** Start, Pause, and Game Over banners with real-time score and session high score tracking.
- **Asset Portability:** Dynamic path resolution allows seamless execution regardless of working directory.
- **Zero-Dependency Headless Testing:** Full test suite running under both `unittest` and `pytest` with dummy SDL drivers.

---

## Controls

| Key | Action |
| :--- | :--- |
| **Arrow Keys** (`↑`, `↓`, `←`, `→`) | Change movement direction (also unpauses/starts game) |
| **Spacebar** | Toggle Pause / Resume (or Restart game after Game Over) |
| **Escape** | Exit game immediately |

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Pygame $\ge 2.0.0$

### Installation

```bash
git clone git@github.com:tpsapp/Snek.git
cd Snek
pip install -r requirements.txt
```

### Running the Game

Launch from repository root or directly from `src/`:

```bash
python3 src/main.py
```

---

## Running Tests

Execute the comprehensive unit and regression test suites:

```bash
# Using pytest
pytest -v

# Or using the Python standard library runner
python3 -m unittest discover tests/
```

---

## Attributions

- **Font:** [DS-Digital](https://www.dafont.com/ds-digital.font) by Dusit Supasawat
- **Audio:** Beep and Error sound effects from [Freesound.org](https://freesound.org/)

---

## License

This project is licensed under the terms of the GNU General Public License v3.0 ([LICENSE](LICENSE)).
