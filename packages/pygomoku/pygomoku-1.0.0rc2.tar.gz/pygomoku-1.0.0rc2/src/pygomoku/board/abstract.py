from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import Annotated, Iterator, Self, cast

from pygomoku.score import Col, DirectionIterator, GoalScore, Player, Position, Row, Score


@dataclass
class BoardABC(ABC):
    """Abstract Base Class for Gomoku Board Management.

    This class provides the foundational methods for managing a Gomoku board,
    including move simulation, heuristic evaluation, winner detection, and board representation.
    It serves as the base class for AI algorithms Including MinMax, AlphaBeta,AlphaBeta Heuristic, and MCTS.

    Attributes:
        grid_size (int): The size of the board (default is 9).
        board (dict): A dictionary mapping positions (row, col) to players (Player.X, Player.O, or EMPTY).
        current_move (Position): The most recent move made on the board.
        next_player (Player): The player to make the next move (default is Player.MIN).
        max_depth (int): Maximum search depth for AI algorithms (default is 3).

    max_depth specifies the maximum search depth for algorithms like MinMax and AlphaBeta.

    While theoretically not required for MinMax and AlphaBeta, these algorithms can be computationally
    expensive when searching the entire game tree. Limiting the search depth ensures the algorithm
    returns a result in a reasonable amount of time.

    To disable depth limitation, set max_depth to a value greater than the total number of cells
    (e.g., grid_size * grid_size + 1). However, this is generally impractical except for very small boards.

    """

    grid_size: Annotated[int, 'Grid Size'] = 9
    max_depth: Annotated[int, 'Maximum Depth'] = 3

    board: dict[Position, Player] = field(default_factory=dict)
    current_move: Position = (-1, -1)
    next_player: Annotated[Player, 'Default Set To User Side'] = Player.MIN

    nodes_expanded: Annotated[int, 'Number of nodes expanded, for performance tracking'] = 0

    def __post_init__(self) -> None:
        """Initialize the board with empty positions."""
        self.board = self.board or {pos: Player.EMPTY for pos in self.cells}

    @abstractmethod
    def calculate_next_move(self) -> Position:
        """Abstract method to calculate the next move.

        This method should be implemented in subclasses for specific algorithms
        Including MinMax, AlphaBeta, or MCTS.
        """

        raise NotImplementedError('This method should be implemented in the subclass.')

    def simulate_move(self, row: Row, col: Col) -> bool:
        """Simulate placing a piece on the board.

        Return True if the move is valid and simulated, False otherwise.
        """

        if not 0 <= row < self.grid_size or not 0 <= col < self.grid_size:
            return False

        if not self.board[(row, col)] == Player.EMPTY:
            return False

        self.board[(row, col)] = self.next_player
        self.next_player = Player.get_opponent(self.next_player)

        return True

    def undo_simulate_move(self, row: Row, col: Col) -> Self:
        """Undo a simulated move.

        Returns The board instance after undoing the move.
        """

        if self.board[(row, col)] == Player.EMPTY:
            return self

        self.board[(row, col)] = Player.EMPTY
        self.next_player = Player.get_opponent(self.next_player)

        return self

    def make_move(self, row: Row, col: Col) -> bool:
        """Make an actual move on the board.

        Returns True if the move was successfully made, False otherwise.
        """

        moved = self.simulate_move(row, col)
        if moved:
            self.current_move = (row, col)
            self.nodes_expanded = 0
        return moved

    def check_winner(self, row: Row, col: Col) -> Player | None:
        """Check if the current move resulted in a win."""
        player = self.board[(row, col)]

        if player == Player.EMPTY:
            return None

        for dr, dc in DirectionIterator:
            count, _ = self._count_consecutive(row, col, dr, dc, player)
            if count >= 5:
                return player

        return None

    def simulate_check_winner(self, row: Row, col: Col, player: Player) -> bool:
        """Simulate check winner for the given player.

        If player makes a move at (row, col), will it win?
        """
        if not self.board[(row, col)] == Player.EMPTY:
            raise ValueError(f"Cell {(row, col)} is not empty.")

        self.simulate_move(row, col)
        winner = self.check_winner(row, col)
        self.undo_simulate_move(row, col)

        return winner == player

    def get_empty_cells(self) -> deque[Position]:
        return deque(
            (r, c)
            for r in range(self.grid_size)
            for c in range(
                self.grid_size,
            )
            if self.board[(r, c)] == Player.EMPTY
        )

    @property
    def center(self) -> int:
        return self.grid_size // 2

    @property
    def cells(self) -> Iterator[Position]:
        yield from ((r, c) for r in range(self.grid_size) for c in range(self.grid_size))

    @property
    def current_player(self) -> Player:
        return Player.get_opponent(self.next_player)

    def _static_evaluation(self, row: Row, col: Col) -> tuple[Player | None, Score]:
        """Perform static evaluation of the board after a move.

        Returns: (Winner, Score) where Winner is the Player instance or None,
            and Score is the evaluation score for the move.
        """

        match winner := self.check_winner(row, col):
            case Player.MIN:
                evaluated = winner, GoalScore.MIN_WIN  # type: ignore
            case Player.MAX:
                evaluated = winner, GoalScore.MAX_WIN  # type: ignore
            case _:
                evaluated = winner, GoalScore.DRAW  # type: ignore
        return evaluated

    def _check_cutoff(self, empty_cells: deque[Position], current_depth: int) -> tuple[bool, Score, Position]:
        """Check whether the search should be terminated (cut-off)."""
        row, col = empty_cells[0]
        self.simulate_move(row, col)

        end, score = False, cast(Score, GoalScore.DRAW)
        if len(empty_cells) == 1:
            end = True
            _, score = self._static_evaluation(row, col)

        elif current_depth >= self.max_depth:
            end = True
            score = self._calculate_heuristic_score(row, col)

        self.undo_simulate_move(row, col)

        return end, score, (row, col)

    def _calculate_heuristic_score(self, row: Row, col: Col) -> Score:
        """Calculate the heuristic score for the current board position.

        In this base class, this function only checks if there is a winner
        for the current position and assigns the corresponding score.
        It does not perform any advanced heuristic evaluations.

        This method is designed to be overridden by subclasses implementing heuristic algorithms,
        allowing for more sophisticated evaluations.
        """

        _, score = self._static_evaluation(row, col)
        return score

    def _count_consecutive(self, row: Row, col: Col, dr: int, dc: int, player: Player) -> tuple[int, int]:
        """Count consecutive pieces of a player in a given direction.

        Returns the count and the open ends count.
        Example:
            (4,1) means there are 4 consecutive pieces and 1 open end.
        """

        count, open_ends = 1, 0
        r, c = row + dr, col + dc

        while self._inboard(r, c) and self.board[(r, c)] == player:
            count += 1
            r += dr
            c += dc

        if self._inboard(r, c) and self.board[(r, c)] == Player.EMPTY:
            open_ends += 1

        r, c = row - dr, col - dc
        while self._inboard(r, c) and self.board[(r, c)] == player:
            count += 1
            r -= dr
            c -= dc

        if self._inboard(r, c) and self.board[(r, c)] == Player.EMPTY:
            open_ends += 1

        return count, open_ends

    def _inboard(self, row: Row, col: Col) -> bool:
        return 0 <= row < self.grid_size and 0 <= col < self.grid_size

    def __get_piece(self, row: Row, col: Col) -> str:
        player = self.board[(row, col)]
        return 'X' if player == Player.MAX else 'O' if player == Player.MIN else Player.EMPTY.value

    def __get_row(self, row: Row) -> str:
        return ' '.join(self.__get_piece(row, col) for col in range(self.grid_size))

    def __repr__(self):
        """Nicely formatted board for debugging."""

        return '\n'.join(self.__get_row(row) for row in range(self.grid_size))
