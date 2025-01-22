from dataclasses import dataclass
from typing import Annotated, cast

from pygomoku.board.alpha import AlphaBeta
from pygomoku.score import Col, DirectionIterator, HeuristicScore, Player, Row, Score


@dataclass
class AlphaBetaHeuristic(AlphaBeta):
    """AlphaBeta Pruning with Heuristic Evaluation.

    Extends the AlphaBeta algorithm by incorporating heuristic evaluation to score board positions.
    This enables deeper and more accurate searches by estimating the potential value of non-terminal states.
    """

    max_depth: Annotated[int, 'Maximum Depth'] = 3

    def _calculate_heuristic_score(self, row: Row, col: Col) -> Score:
        """Calculate the heuristic score for the current board state."""
        scores = cast(Score, 0)

        for r, c in self.cells:
            player = self.board[(r, c)]

            if player == Player.EMPTY:
                continue

            if player == self.current_player:
                scores += self._calculate_current_score(r, c, player)
                scores += self._evaluate_center(r, c)
            else:
                scores -= self._calculate_opponent_score(r, c, player)

        return scores if self.current_player == Player.MAX else -scores

    def _calculate_current_score(self, row: Row, col: Col, player: Player) -> Score:
        """Calculate the score for the current player at a specific position."""
        return sum(
            HeuristicScore.evaluate(
                self._count_consecutive(row, col, dr, dc, player),
            )
            for dr, dc in DirectionIterator
        )

    def _calculate_opponent_score(self, row: Row, col: Col, opponent: Player) -> Score:
        """Calculate the score for the opponent at a specific position."""
        return sum(
            HeuristicScore.evaluate(
                self._count_consecutive(row, col, dr, dc, opponent),
                True,
            )
            for dr, dc in DirectionIterator
        )

    def _evaluate_center(self, row: Row, col: Col) -> Score:
        """Evaluate the score based on proximity to the board center."""
        distance_to_center = abs(self.center - row) + abs(self.center - col)
        return max(0, (self.grid_size - distance_to_center) * 2)

    @classmethod
    def _apply_max_pruning(cls, alpha: float, max_score: Score, beta: Score) -> tuple[Score, bool]:

        alpha = max(alpha, max_score)
        return alpha, alpha > beta

    @classmethod
    def _apply_min_pruning(cls, alpha: float, min_score: float, beta: float) -> tuple[Score, bool]:

        beta = min(beta, min_score)
        return beta, alpha > beta
