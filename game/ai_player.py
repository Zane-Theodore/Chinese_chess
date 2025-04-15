import copy
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
                    if piece.side == side:
                        score += value
                    else:
                        score -= value
        return score

    def minimax(self, board, depth, maximizingPlayer, alpha, beta, side):
        """
        Minimax algorithm with Alpha-Beta Pruning.
        """
        if depth == 0 or board.getLord(1).mated or board.getLord(0).mated:
            return self.evaluateBoard(board, side), None

        valid_moves = self.getAllValidMoves(board, side if maximizingPlayer else self.getOpponent(side))

        best_move = None
        if maximizingPlayer:
            max_eval = float('-inf')
            for piece, moves in valid_moves.items():
                for move in moves:
                    # Simulate move
                    board_copy = copy.deepcopy(board)
                    board_copy.movePiece(piece.getPosition(), move)

                    eval = self.minimax(board_copy, depth - 1, False, alpha, beta, side)[0]
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
                    board_copy = copy.deepcopy(board)
                    board_copy.movePiece(piece.getPosition(), move)

                    eval = self.minimax(board_copy, depth - 1, True, alpha, beta, side)[0]
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
        for piece in board.activePieces:
            if piece.side == side:
                moves = piece.checkPossibleMove(board.grid, update=False)
                if moves:
                    valid_moves[piece] = moves
        return valid_moves

    def getOpponent(self, side):
        """
        Get the opponent's side.
        """
        return 1 if side == 0 else 0

    def findBestMove(self, board, side):
        """
        Find the best move for the given side using Minimax.
        """
        _, best_move = self.minimax(board, self.depth, True, float('-inf'), float('inf'), side)
        return best_move