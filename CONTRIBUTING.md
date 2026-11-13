# Contributing to Snek

Thank you for your interest in contributing to **Snek**! We welcome bug reports, feature suggestions, and pull requests that keep the project lean, robust, and clean.

## Engineering Directives & Standards

All contributions must adhere to the engineering philosophy of the codebase:
- **Standard Library Primacy:** Avoid third-party dependencies unless absolutely necessary.
- **Explicit Control Flow & Clean Domain Separation:** Keep domain logic (`snake.py`, `fruit.py`) decoupled from presentation and hardware APIs.
- **Defensive Input Handling:** Validate all bounds and inputs with guard clauses.
- **Deterministic Testing:** Any bug fix or feature addition must include accompanying unit or regression tests under `tests/`.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:tpsapp/Snek.git
   cd Snek
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python3 src/main.py
   ```

4. **Run the test suite:**
   ```bash
   pytest
   # or using the standard library runner:
   python3 -m unittest discover tests/
   ```

## Commit Conventions

Commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat:` for new capabilities or mechanics
- `fix:` for bug fixes and defect remediation
- `test:` for test additions or fixtures
- `docs:` for documentation updates
- `refactor:` for code restructurings without behavioral changes
- `chore:` for repository maintenance and toolchain updates
