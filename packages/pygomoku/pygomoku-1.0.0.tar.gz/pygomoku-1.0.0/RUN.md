# Gomoku AI Project

This project implements four adversarial search algorithms for the game Gomoku (`MinMax`, `AlphaBeta`, `AlphaBetaHeuristic`, and `MCTS`) with a Python-based GUI.

## **Prerequisites**
- Python version: **>= 3.12**
- Install required packages:
  ```bash
  pip install pygame
  ```
- If you are using `Visual Code` and encoutered error `ModuleNotFoundError: No module named 'pygomoku'` you may run with `export PYTHONPATH=. && python pygomoku/main.py`

## **How to Run**
1. Navigate to the project folder: `pygomoku`.`pygomoku` serves as the `codes` directory.
2. The main executable file is `pygomoku/main.py`.
3. Inside `main.py`, you can switch between the algorithms by uncommenting the corresponding lines:
   ```python
   from pygomoku.board import MCTS, AlphaBeta, AlphaBetaHeuristic, MinMax
   from pygomoku.gui import GomokuUI

   def main() -> None:
       """Run the Gomoku game with the algorithm."""
       grid_size = 9  # set the grid size
       # Uncomment one of the following lines to choose the algorithm:
       # game = MinMax(grid_size=grid_size)
       # game = AlphaBeta(grid_size=grid_size)
       # game = AlphaBetaHeuristic(grid_size=grid_size)
       game = MCTS(grid_size=grid_size)  # type: ignore

       ui = GomokuUI(game)
       ui.run()

   if __name__ == '__main__':
       import logging
       logging.basicConfig(level=logging.DEBUG)
       main()
   ```
4. By default, the `MCTS` algorithm is enabled. Uncomment the desired algorithm and comment out the rest to switch.
5. Run the program:
   ```bash
   python main.py
   ```

## **Code Structure**
- **`pygomoku/board`**: Contains all algorithm implementations (`MinMax`, `AlphaBeta`, `AlphaBetaHeuristic`, and `MCTS`).
- **`pygomoku/gui`**: Handles the graphical user interface using `pygame`.

Enjoy playing Gomoku with advanced AI!
