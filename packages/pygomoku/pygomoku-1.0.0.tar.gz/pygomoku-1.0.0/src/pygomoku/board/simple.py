from random import choice

from pygomoku.board.abstract import BoardABC
from pygomoku.score import Position


class Simple(BoardABC):
    """Simple Random Move Generator.

    This class is primarily for testing purposes and is used to verify whether the GUI integration
    works correctly. It selects the next move randomly from the available empty cells on the board.

    Limitations:
    - Does not implement any intelligent move selection logic.
    - Should not be used in actual gameplay as it only serves for GUI testing.
    """

    def calculate_next_move(self) -> Position:
        return choice(self.get_empty_cells()) if self.get_empty_cells() else (-1, -1)
