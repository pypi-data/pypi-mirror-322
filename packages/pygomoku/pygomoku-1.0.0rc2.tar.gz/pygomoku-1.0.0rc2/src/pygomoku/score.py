from collections import defaultdict
from enum import Enum, StrEnum
from typing import Annotated

# Annotated types for better readability and type hinting
Consecutive = Annotated[int, 'Consecutive Pieces']
OpenEnds = Annotated[
    int,
    'Open Ends, 0: both ends are blocked, 1: one end is open, 2: both ends are open',
]
Score = Annotated[float, 'Score Of The Board']
Row = Annotated[int, 'Row']
Col = Annotated[int, 'Column']
Position = Annotated[tuple[Row, Col], 'Position On The Board']


class Player(StrEnum):
    MIN = 'X'  # User's side, minimizes the score
    MAX = 'O'  # AI's side, maximizes the score
    EMPTY = '-'  # Empty cell on the board

    @classmethod
    def get_opponent(cls, player: 'Player') -> 'Player':
        if player == cls.EMPTY:
            raise ValueError(f"Player cannot be {cls.EMPTY}")

        return cls.MAX if player == cls.MIN else cls.MIN


class DirectionIterator(Enum):
    """Iterator for directional movements."""

    VERTICAL = (1, 0)
    HORIZONTAL = (0, 1)
    POSITIVE_DIAGONAL = (1, 1)
    NEGATIVE_DIAGONAL = (1, -1)

    def __iter__(self):
        return iter(self.value)


class GoalScore:
    """Constants for goal evaluation scores."""

    MIN_WIN = -float('inf')  # Winning score for MIN player
    MAX_WIN = float('inf')  # Winning score for MAX player
    DRAW = 0  # Score for a draw


class HeuristicScore:
    """Scores for heuristic evaluation."""

    CONSECUTIVE_4 = 1000
    CONSECUTIVE_3 = 50
    CONSECUTIVE_2 = 5

    _WEIGHT = 1.2  # Weight for blocking strategies
    BLOCKING_4 = 1000 * _WEIGHT
    BLOCKING_3 = int(CONSECUTIVE_3 * _WEIGHT)  # 60
    BLOCKING_2 = int(CONSECUTIVE_2 * _WEIGHT)  # 6

    OPEN_ENDS_TWO_WEIGHT = 1.1

    # Scores for consecutive pieces
    __CONSECUTIVE_SCORES__ = defaultdict(
        int,
        {
            (4, 2): CONSECUTIVE_4 * OPEN_ENDS_TWO_WEIGHT,  # Guaranteed win
            (4, 1): CONSECUTIVE_4,
            (3, 2): CONSECUTIVE_3 * OPEN_ENDS_TWO_WEIGHT,
            (3, 1): CONSECUTIVE_3,
            (2, 2): CONSECUTIVE_2 * OPEN_ENDS_TWO_WEIGHT,
            (2, 1): CONSECUTIVE_2,
        },
    )
    # Scores for blocking opponent's pieces
    __BLOCKING_SCORES__ = defaultdict(
        int,
        {
            (4, 2): BLOCKING_4,  # Must block opponent's 4
            (4, 1): BLOCKING_4,
            (3, 2): BLOCKING_3 * OPEN_ENDS_TWO_WEIGHT,
            (3, 1): BLOCKING_3,
            (2, 2): BLOCKING_2,
            (2, 1): BLOCKING_2,
        },
    )

    @classmethod
    def evaluate(cls, con: tuple[Consecutive, OpenEnds], is_opponent: bool = False) -> Score:
        """Evaluate the score based on consecutive pieces and open ends."""
        return cls.__BLOCKING_SCORES__[con] if is_opponent else cls.__CONSECUTIVE_SCORES__[con]
