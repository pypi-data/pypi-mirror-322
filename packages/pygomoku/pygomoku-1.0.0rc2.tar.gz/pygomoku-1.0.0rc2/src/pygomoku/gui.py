import logging
import sys
import time
from dataclasses import dataclass, field
from typing import Annotated, NoReturn, Self

import pygame

from pygomoku.board.abstract import BoardABC
from pygomoku.score import Player


@dataclass
class GomokuUI:
    game: BoardABC

    cell_size: Annotated[int, 'Pixel Number'] = 50
    caption: Annotated[str, 'Window Caption'] = '24435015 Gomoku'
    font_size: Annotated[int, 'Font Size'] = 30
    info_font_size: Annotated[int, 'Info Font Size'] = 20

    grid_line_thickness: Annotated[int, 'Grid Line Thickness'] = 1
    piece_line_thickness: Annotated[int, 'Piece Line Thickness'] = 3
    info_text_offset_x: Annotated[int, 'X Offset for Info Text'] = 10
    info_text_offset_y: Annotated[int, 'Y Offset for Info Text'] = 15
    winner_text_offset_x: Annotated[int, 'X Offset for Winner Text'] = 10
    winner_text_offset_y: Annotated[int, 'Y Offset for Winner Text'] = 30
    circle_margin: Annotated[int, 'Margin for Circle Pieces'] = 10
    info_area_height: Annotated[int, 'Height of Info Area'] = 40

    # Colors
    board_background_color: tuple[int, int, int] = (255, 255, 200)
    grid_line_color: tuple[int, int, int] = (0, 0, 0)
    info_background_color: tuple[int, int, int] = (220, 220, 220)
    player_x_color: tuple[int, int, int] = (255, 0, 0)
    player_o_color: tuple[int, int, int] = (0, 0, 255)

    # Game information display
    info_text: Annotated[str, 'Display Computer Move Time'] = ''
    winner_text: Annotated[str, 'Display The Winner'] = ''

    screen: pygame.Surface = field(init=False)
    width: int = field(init=False)
    height: int = field(init=False)

    game_over: bool = False

    def __post_init__(self) -> None:
        self.width = self.cell_size * self.game.grid_size
        self.height = self.cell_size * self.game.grid_size + self.info_area_height

        pygame.init()  # noqa
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)

        self.font = pygame.font.SysFont(None, self.font_size)
        self.info_font = pygame.font.SysFont(None, self.info_font_size)
        self.draw_grid()

    def draw_grid(self) -> Self:
        self.screen.fill(self.board_background_color)
        for row in range(self.game.grid_size):
            for col in range(self.game.grid_size):
                rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, self.grid_line_color, rect, self.grid_line_thickness)  # Draw grid lines
        self.draw_info_area()

        return self

    def draw_info_area(self) -> Self:
        """Draw the information area below the grid."""
        info_rect = pygame.Rect(0, self.height - self.info_area_height, self.width, self.info_area_height)
        pygame.draw.rect(self.screen, self.info_background_color, info_rect)

        # Display computer move time in smaller font, aligned to the left
        info_surface = self.info_font.render(self.info_text, True, (0, 0, 0))
        info_text_rect = info_surface.get_rect(
            left=self.info_text_offset_x,
            centery=self.height - self.info_area_height // 2,
        )
        self.screen.blit(info_surface, info_text_rect)

        # Display the winner information in larger font, aligned to the right
        winner_surface = self.font.render(self.winner_text, True, (0, 0, 0))
        winner_text_rect = winner_surface.get_rect(
            right=self.width - self.winner_text_offset_x,
            centery=self.height - self.info_area_height // 2,
        )
        self.screen.blit(winner_surface, winner_text_rect)

        return self

    def draw_piece(self, row: int, col: int) -> Self:
        center = (
            col * self.cell_size + self.cell_size // 2,
            row * self.cell_size + self.cell_size // 2,
        )
        radius = self.cell_size // 2 - self.circle_margin

        # match self.game.board[row][col]:
        match self.game.board[(row, col)]:
            case Player.MIN:
                pygame.draw.line(
                    self.screen,
                    self.player_x_color,
                    (center[0] - radius, center[1] - radius),
                    (center[0] + radius, center[1] + radius),
                    self.piece_line_thickness,
                )
                pygame.draw.line(
                    self.screen,
                    self.player_x_color,
                    (center[0] + radius, center[1] - radius),
                    (center[0] - radius, center[1] + radius),
                    self.piece_line_thickness,
                )
            case Player.MAX:
                pygame.draw.circle(
                    self.screen,
                    self.player_o_color,
                    center,
                    radius,
                    self.piece_line_thickness,
                )
            case _:
                raise ValueError('Invalid Player')

        return self

    def display_text(self, text: str) -> Self:
        text_surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (10, self.height - 40))

        return self

    def handle_click(self, pos: tuple[int, int]) -> Self:
        if self.game_over:  # Stop accepting input if the game is over
            return self

        col = pos[0] // self.cell_size
        row = pos[1] // self.cell_size

        if self.game.make_move(row, col):
            self.draw_piece(row, col)
            pygame.display.flip()

            if winner := self.game.check_winner(row, col):
                self.winner_text = f"Player {winner} wins!"
                self.info_text = ''
                self.game_over = True
                self.draw_info_area()
                pygame.display.flip()
                return self

            self.computer_move()

        return self

    def computer_move(self) -> None:
        start_time = time.time()

        row, col = self.game.calculate_next_move()  # maybe none
        elapsed_time = time.time() - start_time
        logging.debug(
            'Computer move: %d, %d, %.2f seconds, Nodes expanded: %d', row, col, elapsed_time, self.game.nodes_expanded
        )
        if self.game.make_move(row, col):
            self.draw_piece(row, col)
            self.info_text = f"Computer moved in {elapsed_time:.2f} seconds"
            self.draw_info_area()

            if winner := self.game.check_winner(row, col):
                self.info_text = f"Player {winner} wins!"
                self.game_over = True
                self.draw_info_area()

    def run(self) -> NoReturn:
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    case pygame.MOUSEBUTTONDOWN:
                        self.handle_click(event.pos)
                    case _:
                        ...

            pygame.display.flip()
