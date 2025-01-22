from dataclasses import dataclass
from typing import Annotated

from pygomoku.board.abstract import BoardABC
from pygomoku.score import Position, Score


@dataclass
class MinMax(BoardABC):
    """MinMax Algorithm.

    MinMax is a fundamental adversarial search algorithm used to determine the optimal move
    by simulating all possible moves for both players. The algorithm maximizes the AI's score
    while minimizing the opponent's score.

    However, MinMax can be computationally expensive as it searches the entire game tree.
    To address this, a `max_depth` parameter is introduced to limit the search depth. Default set to 3.

    Notes:
        Larger `max_depth` may result in impractical computation times on larger boards.
    """

    max_depth: Annotated[int, 'Maximum Depth'] = 3

    def calculate_next_move(self) -> Position:
        _, best_move = self._maximize(0, -float('inf'), float('inf'))
        return best_move

    def _maximize(self, current_depth: int, alpha: Score, beta: Score) -> tuple[Score, Position]:
        """Maximizing player's turn in the MinMax algorithm."""

        empty_cells = self.get_empty_cells()
        cut_off, cut_off_score, move = self._check_cutoff(empty_cells, current_depth)
        if cut_off:
            return cut_off_score, move

        max_score, best_move = -float('inf'), empty_cells[0]
        while empty_cells:
            r, c = empty_cells.popleft()
            self.simulate_move(r, c)
            self.nodes_expanded += 1
            winner, score = self._static_evaluation(r, c)

            if winner:  # Early termination if a winner is found
                self.undo_simulate_move(r, c)
                return score, (r, c)
            else:
                score, _ = self._minimize(current_depth + 1, alpha, beta)
                if score > max_score:
                    max_score, best_move = score, (r, c)

            self.undo_simulate_move(r, c)

            # Apply Alpha-Beta pruning (can be overridden by subclasses)
            alpha, prune = self._apply_max_pruning(alpha, max_score, beta)
            if prune:
                break

        return max_score, best_move

    def _minimize(self, current_depth: int, alpha: Score, beta: Score) -> tuple[Score, Position]:
        """Minimizing player's turn in the MinMax algorithm."""

        empty_cells = self.get_empty_cells()
        cut_off, cut_off_score, move = self._check_cutoff(empty_cells, current_depth)
        if cut_off:
            return cut_off_score, move

        min_score, best_move = float('inf'), empty_cells[0]
        while empty_cells:
            r, c = empty_cells.popleft()
            self.simulate_move(r, c)
            self.nodes_expanded += 1
            winner, score = self._static_evaluation(r, c)

            if winner:  # Early termination if a winner is found
                self.undo_simulate_move(r, c)
                return score, (r, c)
            else:
                score, _ = self._maximize(current_depth + 1, alpha, beta)
                if score < min_score:
                    min_score, best_move = score, (r, c)

            self.undo_simulate_move(r, c)
            # Apply Alpha-Beta pruning (can be overridden by subclasses)
            beta, prune = self._apply_min_pruning(alpha, min_score, beta)
            if prune:
                break

        return min_score, best_move

    # pylint: disable=unused-argument
    @classmethod
    def _apply_max_pruning(cls, alpha: Score, max_score: Score, beta: Score) -> tuple[Score, bool]:
        """Apply Alpha-Beta pruning logic for the Max player.

        Returns:
            tuple[Score, bool]: Updated alpha value and a boolean indicating whether to prune.
        """

        return alpha, False  # No pruning for basic MinMax

    # pylint: disable=unused-argument
    @classmethod
    def _apply_min_pruning(cls, alpha: Score, min_score: Score, beta: Score) -> tuple[Score, bool]:  # noqa
        """Apply Alpha-Beta pruning logic for the Min player.

        Returns:
            tuple[Score, bool]: Updated beta value and a boolean indicating whether to prune.
        """
        return beta, False  # No pruning for basic MinMax
