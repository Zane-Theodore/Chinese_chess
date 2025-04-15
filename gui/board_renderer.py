import pygame
from game.config import Color

class BoardRenderer:
    def __init__(self, board):
        self.board = board

    def draw(self, win):
        board = self.board

        riverCoordinate = ()

        pygame.draw.rect(
            win,
            (252, 182, 40),
            pygame.Rect(
                board.x - board.border,
                board.y - board.border,
                board.width + board.border * 2,
                board.height + board.border * 2,
            ),
        )

        pygame.draw.rect(
            win,
            (255, 203, 97),
            pygame.Rect(board.x, board.y, board.width, board.height),
        )

        for row in range(board.rows + 1):
            pygame.draw.line(
                win,
                Color.GREY,
                (board.x, board.y + row * board.gap),
                (board.x + board.width, board.y + row * board.gap),
                2,
            )

            if row == board.rows // 2:
                riverCoordinate = (board.x + 2, board.y + row * board.gap + 2)

            for col in range(board.cols + 1):
                pygame.draw.line(
                    win,
                    Color.GREY,
                    (col * board.gap + board.x, board.y),
                    (col * board.gap + board.x, board.height + board.y),
                    2,
                )

        # Draw the palace
        palaceCoors = [
            ((board.x + board.gap * 3, board.y), (board.x + board.gap * 5, board.y + board.gap * 2)),
            ((board.x + board.gap * 5, board.y), (board.x + board.gap * 3, board.y + board.gap * 2)),
            ((board.x + board.gap * 3, board.y + board.gap * 7), (board.x + board.gap * 5, board.y + board.gap * 9)),
            ((board.x + board.gap * 5, board.y + board.gap * 7), (board.x + board.gap * 3, board.y + board.gap * 9)),
        ]
        for point1, point2 in palaceCoors:
            pygame.draw.line(win, Color.GREY, point1, point2, 2)

        # Draw the river
        pygame.draw.rect(
            win,
            (252, 182, 40),
            pygame.Rect(*riverCoordinate, board.width - 2, board.gap - 2),
        )

        # Border
        pygame.draw.rect(
            win,
            (252, 182, 40),
            (
                board.x - board.border,
                board.y - board.border,
                board.width + board.border * 2,
                board.height + board.border * 2,
            ),
            10,
        )

        # Draw pieces
        for piece in board.activePieces:
            piece.draw(win)

        # Highlight movables
        for pos in board.movables:
            coor = board.getCoordinateFromPosition(pos)
            pygame.draw.circle(win, Color.GREEN, coor, 7)
