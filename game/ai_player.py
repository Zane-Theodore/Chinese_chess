import numpy as np
from .config import RED_SIDE, BLUE_SIDE


class AIPlayer:
    def __init__(self, depth=3):
        """
        Initialize the AI Player with a search depth.
        """
        self.depth = depth

    def evaluateBoard(self, board, side):
        """
        Evaluate the board and return a score for the given side.
        Positive score favors the given side, negative score favors the opponent.
        """
        piece_values = {
            "Lord": 1000,
            "Chariot": 50,
            "Horse": 30,
            "Cannon": 30,
            "Elephant": 10,
            "Advisor": 10,
            "Soldier": 5,
        }

        score = 0
        for row in board.grid:
            for piece in row:
                if piece is not None:
                    value = piece_values.get(piece.NAME, 0)
                    # Thêm trọng số dựa trên vị trí
                    row_modifier = 1 if piece.side == RED_SIDE else -1
                    position_value = row_modifier * piece.position[0] * 0.1
                    if piece.side == side:
                        score += value + position_value
                    else:
                        score -= value + position_value
        return score

    def minimax(self, board, depth, maximizingPlayer, alpha, beta, side):
        """
        Minimax algorithm with Alpha-Beta Pruning.
        """
        if depth == 0 or board.getLord(RED_SIDE).mated or board.getLord(BLUE_SIDE).mated:
            return self.evaluateBoard(board, side), None

        valid_moves = self.getAllValidMoves(board, side if maximizingPlayer else self.getOpponent(side))

        # Sắp xếp nước đi để ưu tiên các nước ăn quân
        valid_moves = self.sortMoves(valid_moves, board)

        best_move = None
        if maximizingPlayer:
            max_eval = float('-inf')
            for piece, moves in valid_moves.items():
                for move in moves:
                    # Simulate move
                    captured_piece = board.getPiece(move)
                    self.simulateMove(board, piece, move)

                    eval = self.minimax(board, depth - 1, False, alpha, beta, side)[0]

                    # Undo move
                    self.undoMove(board, piece, move, captured_piece)

                    if eval > max_eval:
                        max_eval = eval
                        best_move = (piece, move)

                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for piece, moves in valid_moves.items():
                for move in moves:
                    # Simulate move
                    captured_piece = board.getPiece(move)
                    self.simulateMove(board, piece, move)

                    eval = self.minimax(board, depth - 1, True, alpha, beta, side)[0]

                    # Undo move
                    self.undoMove(board, piece, move, captured_piece)

                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece, move)

                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval, best_move

    def getAllValidMoves(self, board, side):
        """
        Get all valid moves for the given side.
        Returns a dictionary with pieces as keys and their possible moves as values.
        """
        valid_moves = {}
        for piece in board.activePices:
            if piece.side == side:
                moves = piece.checkPossibleMove(board.grid, update=False)
                if moves:
                    valid_moves[piece] = moves
        return valid_moves

    def sortMoves(self, valid_moves, board):
        """
        Sort moves to prioritize capturing pieces.
        """
        sorted_moves = {}
        for piece, moves in valid_moves.items():
            # Sort moves by the value of the captured piece (if any)
            sorted_moves[piece] = sorted(
                moves,
                key=lambda move: (
                    board.getPiece(move).NAME if board.getPiece(move) else "",
                    board.getPiece(move).side if board.getPiece(move) else "",
                ),
                reverse=True,
            )
        return sorted_moves

    def simulateMove(self, board, piece, move):
        """
        Simulate a move on the board.
        """
        captured_piece = board.getPiece(move)
        board.movePiece(piece.getPosition(), move)
        return captured_piece

    def undoMove(self, board, piece, move, captured_piece):
        """
        Undo a simulated move on the board.
        """
        board.movePiece(move, piece.getPosition())
        if captured_piece:
            board.placePiece(captured_piece, move)

    def getOpponent(self, side):
        """
        Get the opponent's side.
        """
        return RED_SIDE if side == BLUE_SIDE else BLUE_SIDE

    def findBestMove(self, board, side):
        """
        Find the best move for the given side using Minimax.
        """
        _, best_move = self.minimax(board, self.depth, True, float('-inf'), float('inf'), side)
        return best_move
