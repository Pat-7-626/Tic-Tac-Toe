# Tic-Tac-Toe Pro

A portfolio-quality Tic-Tac-Toe game built with Python and Tkinter. Features a modern dark UI, a robust game engine, and an unbeatable AI opponent using the Minimax algorithm.

## Features

- **Modern UI**: Sleek, dark-themed interface inspired by the Catppuccin Mocha palette with winning line highlights.
- **Scoreboard**: Tracks wins, losses, and draws for the session.
- **Game Modes**:
  - **PvP**: Player vs Player on the same device.
  - **PvAI**: Challenge the Computer with adjustable difficulty (Easy, Medium, Hard).
- **AI Difficulty**:
  - **Easy**: Makes random moves.
  - **Medium**: A balanced challenge.
  - **Hard**: Unbeatable Minimax algorithm.
- **Sound**: Toggleable sound effects for moves and Game Over.

## Installation & Running

1.  Ensure you have Python installed.
2.  Run the game:
    ```bash
    python main.py
    ```

## Project Structure

- `main.py`: Entry point.
- `ui.py`: Handles the Graphical User Interface (View).
- `game_logic.py`: Core game rules and state management (Model).
- `ai_opponent.py`: AI logic implementation.
- `test_game_logic.py`: Unit tests ensuring game correctness.

## Tech Stack

- **Language**: Python 3
- **GUI**: Tkinter
- **Algorithm**: Minimax (for AI)
