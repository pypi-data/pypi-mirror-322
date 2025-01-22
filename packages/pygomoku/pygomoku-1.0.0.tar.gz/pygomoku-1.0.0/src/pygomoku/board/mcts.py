from __future__ import annotations

import logging
import math
import random
import time
from collections import defaultdict, deque
from copy import copy
from dataclasses import dataclass, field
from typing import Annotated, Iterable, Self

from pygomoku.board.abstract import BoardABC
from pygomoku.score import Player, Position


@dataclass
class _Node(BoardABC):
    """Internal Node for Monte Carlo Tree Search (MCTS).

    Represents a single node in the MCTS tree, tracking its parent, children, and statistical data
    such as visits and wins for each player.
    """

    parent: Annotated[_Node | None, 'The parent node in the tree'] = None
    available_moves: Annotated[deque[Position], 'Available moves from this state.'] = field(default_factory=deque)

    _children: Annotated[dict[Position, _Node], 'Child nodes, indexed by move.'] = field(default_factory=dict)
    _winning_info: Annotated[dict[Player, int], 'Tracks the number of wins for each player.'] = field(
        default_factory=lambda: defaultdict(int)
    )
    _unexplored_moves: Annotated[deque[Position], 'Moves not yet expanded.'] = field(init=False)

    winner: Annotated[Player | None, 'The winner at this node, if any.'] = Player.EMPTY

    EXPLORATION_WEIGHT: Annotated[float, 'Controls the balance between exploration and exploitation.'] = 1.4
    TIME_LIMIT_SECONDS: Annotated[float, 'Time limit for MCTS simulations.'] = 15

    def __post_init__(self):
        self._unexplored_moves = copy(self.available_moves)

    def calculate_next_move(self) -> Position:
        raise NotImplementedError('This method should be called on the MCTS node.')

    def iterate(self) -> _Node:
        """Perform a single MCTS iteration (selection, expansion, simulation, and backpropagation)."""
        leaf = self.select()
        child = leaf.expand()
        winner = child.simulate()
        child.back_propagate(winner)
        return self

    def select(self) -> _Node:
        """Select the most promising node to expand using UCB1.

        Returns the selected leaf node.
        """
        leaf = self

        while leaf.is_fully_expanded:
            leaf = leaf.best_child
        return leaf

    def expand(self) -> _Node:
        """Expand the tree by creating a new child node for an unexplored move."""
        child_move = self._unexplored_moves.popleft()

        available_moves = copy(self.available_moves)
        available_moves.remove(child_move)

        child = _Node(
            current_move=child_move,
            parent=self,
            next_player=self.next_player,
            available_moves=available_moves,
            board=copy(self.board),
            grid_size=self.grid_size,
        )
        child.make_move(*child_move)
        child.winner = child.check_winner(*child.current_move)
        self._children[child_move] = child

        return child

    def simulate(self) -> Player:
        """Simulate a random playout from the current node to a terminal state."""
        if self.winner:
            return self.winner

        empty_cells = self.get_empty_cells()
        undo_simulate, result = copy(empty_cells), Player.EMPTY
        while empty_cells:
            r, c = random.choice(empty_cells)
            self.simulate_move(r, c)

            empty_cells.remove((r, c))
            if winner := self.check_winner(r, c):
                result = winner
                break

        self.undo_simulate(undo_simulate)
        return result

    def undo_simulate(self, undo_simulate: Iterable[Position]) -> Self:
        """Undo all simulated moves.

        Purpose:
        Instead of using Python's `deepcopy` to copy the board state, this method efficiently reverts the board
        to its previous state by undoing all simulated moves.

        Why not `deepcopy`?
        - `deepcopy` is computationally expensive and can significantly slow down the algorithm.
        - Only the board state needs to be reverted; copying the entire object is unnecessary.

        Usage:
        This method ensures that the current node's state is restored after running simulations so it can be passed.
        """
        for r, c in undo_simulate:
            self.undo_simulate_move(r, c)

        return self

    def back_propagate(self, winner: Player) -> Self:
        """Update the tree with simulation results."""
        node = self
        while node is not None:
            node.update(winner)
            node = node.parent  # type: ignore
        return self

    def update(self, winner: Player) -> Self:
        """Update the node's win statistics."""
        self._winning_info[winner] += 1
        return self

    @property
    def is_fully_expanded(self) -> bool:
        """Check if all possible moves have been expanded.

        If all moves have been expanded, the node is considered fully expanded.
        """
        return len(self._unexplored_moves) == 0

    @property
    def visits(self) -> int:
        """Total number of simulations for this node.

        Return 1 if no simulations have been made to avoid division by zero.
        """
        return sum(self._winning_info.values()) or 1  # Avoid division by zero

    @property
    def wins(self) -> int:
        """Number of wins for the current player."""
        return self._winning_info[self.current_player]

    @property
    def ucb1(self) -> float:
        """Calculate the Upper Confidence Bound (UCB1) score.

        Returns:
            float: UCB1 value for balancing exploration and exploitation.
        """
        if self.parent is None:
            raise ValueError('Root node has no parent')
        return self.wins / self.visits + self.EXPLORATION_WEIGHT * math.sqrt(math.log(self.parent.visits) / self.visits)

    @property
    def best_child(self) -> _Node:
        """Select the child node with the highest UCB1 score."""
        return max(self._children.values(), key=lambda child: child.ucb1)

    @property
    def best_final_move(self) -> Position:
        """Select the best move based on simulation results.

        This method prioritizes moves that guarantee a win for the next player.
        If no such move exists, it selects the most visited child node, which represents
        the move that has been explored the most during simulations.

        Key Difference:
        - `best_final_move`: Focuses exclusively on maximizing the real win rate, disregarding the exploration factor.
        - `best_child`: Considers the UCB1 score, which balances both exploitation (wins) and exploration (visits).

        Use Case:
        `best_final_move` is used for the final move decision, as the exploration factor is no longer relevant.
        """
        for c in self._children.values():
            if c.winner == self.next_player:
                return c.current_move
        return max(self._children.values(), key=lambda child: child.visits).current_move

    def __repr__(self):
        return f"<_Node: {self.current_move}, visits: {self.visits}, wins: {self.wins}, ucb1: {self.ucb1}>"


class MCTS(BoardABC):
    """Monte Carlo Tree Search (MCTS) Algorithm.

    Combines exploration and exploitation to select optimal moves based on simulations.
    """

    def calculate_next_move(self) -> Position:
        """Calculate the next optimal move using MCTS.

        Runs simulations for a fixed time period and selects the best move.
        """
        root = _Node(
            current_move=self.current_move,
            next_player=self.next_player,
            available_moves=self.get_empty_cells(),
            board=copy(self.board),
            grid_size=self.grid_size,
        )

        count, start_time = 0, time.time()
        while time.time() - start_time < _Node.TIME_LIMIT_SECONDS:
            root.iterate()
            count += 1
        logging.debug('Simulated %d times', count)

        return root.best_final_move
