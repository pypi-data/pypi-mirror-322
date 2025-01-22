"""Gomoku game with AI"""

__title__ = 'pygomoku'
__version__ = '1.0.0rc2'
__author__ = 'HE RUI'
__license__ = 'MIT'
__description__ = 'Gomoku game with AI'
__name__ = 'pygomoku'


from pygomoku.board import MCTS, AlphaBeta, AlphaBetaHeuristic, MinMax
from pygomoku.gui import GomokuUI

__all__ = [
    'GomokuUI',
    'MinMax',
    'AlphaBeta',
    'AlphaBetaHeuristic',
    'MCTS',
]
