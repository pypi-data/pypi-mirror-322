from dataclasses import dataclass
from typing import Annotated

from pygomoku.board.minmax import MinMax
from pygomoku.score import Score


@dataclass
class AlphaBeta(MinMax):
    """AlphaBeta Pruning Algorithm.

    The AlphaBeta algorithm optimizes the `MinMax` algorithm by pruning branches that do not need to be explored,
    significantly reducing time complexity. This enables deeper searches within limited computational resources.

    Compared to `MinMax`, AlphaBeta achieves similar results with less computation.
    The acceptable range of `max_depth` is generally higher for AlphaBeta than for `MinMax`.

    On a 5x5 grid, an upper bound of `max_depth = 7` usually takes around 5 seconds to compute.
    For larger grids, the value of `max_depth` may need adjustment based on the available time and resources.

    Attributes:
        max_depth (int): The maximum depth for the search tree. Defaults to 5.
    """

    max_depth: Annotated[int, 'Maximum Depth'] = 5

    @classmethod
    def _apply_max_pruning(cls, alpha: float, max_score: Score, beta: Score) -> tuple[Score, bool]:
        """Perform Alpha-Beta pruning for the Max player.

        AlphaBeta pruning works by maintaining two bounds: `alpha` (the best score that the Max player is assured of)
        and `beta` (the best score that the Min player is assured of). During the Max player's turn:

        Returns:
            tuple: The updated `alpha` value and a boolean indicating whether the branch should be pruned.
        """

        alpha = max(alpha, max_score)
        return alpha, alpha >= beta

    @classmethod
    def _apply_min_pruning(cls, alpha: float, min_score: float, beta: float) -> tuple[Score, bool]:
        """Perform Alpha-Beta pruning for the Min player.

        Similar to Max pruning, AlphaBeta pruning for Min ensures that branches yielding scores
        greater than or equal to `alpha` (Max's best assured score) are pruned:

        - If the current score for Min (`min_score`) is less than or equal to `alpha`,
          the Max player will never choose this branch. Therefore, this branch can be pruned.
        - Otherwise, update `beta` to the minimum of its current value and `min_score`.

        Returns:
            tuple: The updated `beta` value and a boolean indicating whether the branch should be pruned.
        """

        beta = min(beta, min_score)
        return beta, alpha >= beta
