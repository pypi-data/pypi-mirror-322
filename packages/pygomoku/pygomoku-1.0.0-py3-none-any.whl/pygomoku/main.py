from pygomoku.board import MCTS, AlphaBeta, AlphaBetaHeuristic, MinMax
from pygomoku.gui import GomokuUI


def main() -> None:
    """Run the Gomoku game with the algorithm."""
    grid_size = 9  # set the grid size
    # uncomment one of the following lines to choose the algorithm
    game = MinMax(grid_size=grid_size)
    game = AlphaBeta(grid_size=grid_size, max_depth=3)
    game = AlphaBetaHeuristic(grid_size=grid_size)
    game = MCTS(grid_size=grid_size)  # type: ignore

    ui = GomokuUI(game)
    ui.run()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)
    main()
