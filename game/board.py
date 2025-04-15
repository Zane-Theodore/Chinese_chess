import os
import numpy as np

from .pieces import Chariot, Cannon, Horse, Elephant, Soldier, Advisor, Lord
from .config import RED_SIDE, BLUE_SIDE, WIN_HEIGHT, WIN_WIDTH

class Board:
    def __init__(self):
        self.rows = 9
        self.cols = 8
        self.gap = WIN_WIDTH // 15
        self.border = 20
        self.width = self.cols * self.gap
        self.height = self.rows * self.gap

        self.grid = [[None for _ in range(self.cols + 1)] for _ in range(self.rows + 1)]
        self.activePieces = []
        self.movables = []
        self.turn = RED_SIDE
        self.blueLord = None
        self.redLord = None

        self.calculatePosition()
        self.makeGrid()

    def calculatePosition(self):
        self.x = 50
        self.y = (WIN_HEIGHT - self.height) / 2

    def readPreset(self):
        directory = os.path.dirname(__file__)
        presetPath = os.path.join(directory, "presets/standard.cfg")
        with open(presetPath, "r") as f:
            lines = f.readlines()

        result = []
        for line in lines:
            line = line.strip()
            piece, row, col, side = line.split(" ******** ")
            row, col = int(row), int(col)
            side = RED_SIDE if side == "red" else BLUE_SIDE
            result.append((piece, (row, col), side))
        return result

    def makeGrid(self):
        chessTypes = {
            "chariot": Chariot,
            "cannon": Cannon,
            "horse": Horse,
            "elephant": Elephant,
            "soldier": Soldier,
            "advisor": Advisor,
            "lord": Lord,
        }

        for piece, position, side in self.readPreset():
            centre = self.getCoordinateFromPosition(position)
            newPiece = chessTypes[piece](centrePoint=centre, position=position, side=side)
            self.activePieces.append(newPiece)
            if isinstance(newPiece, Lord):
                if newPiece.side == RED_SIDE:
                    self.redLord = newPiece
                else:
                    self.blueLord = newPiece
            row, col = position
            self.grid[row][col] = newPiece

        for piece in self.activePieces:
            piece.checkPossibleMove(self.grid)

    def getCoordinateFromPosition(self, position):
        row, col = position
        x = self.x + self.gap * col
        y = self.y + self.gap * row
        return (x, y)

    def getPositionFromCoordinate(self, coordinate):
        x, y = coordinate
        col = round((x - self.x) / self.gap)
        row = round((y - self.y) / self.gap)
        return (row, col)

    def getPiece(self, position):
        row, col = position
        return self.grid[row][col]

    def getLord(self, side):
        return self.redLord if side == RED_SIDE else self.blueLord

    def isClicked(self, clickedPos):
        if not clickedPos:
            return False
        x, y = clickedPos
        if x < self.x - self.border or x > self.x + self.width + self.border:
            return False
        if y < self.y - self.border or y > self.y + self.height + self.border:
            return False
        return True

    def deselectPiece(self, piecePos):
        piece = self.getPiece(piecePos)
        piece.deselect()
        self.movables = []
        return None

    def movePiece(self, oldPos, newPos):
        lord = self.getLord(self.turn)
        lord.mated = False

        oldRow, oldCol = oldPos
        newRow, newCol = newPos

        self.deselectPiece(oldPos)

        if self.grid[newRow][newCol]:
            self.activePieces.remove(self.grid[newRow][newCol])

        piece = self.grid[oldRow][oldCol]
        self.grid[oldRow][oldCol] = None
        self.grid[newRow][newCol] = piece

        centre = self.getCoordinateFromPosition(newPos)
        piece.moveToNewSpot(centrePoint=centre, position=newPos)

        self.turn = RED_SIDE if self.turn == BLUE_SIDE else BLUE_SIDE

    def lordTolord(self):
        row1, col1 = self.redLord.getPosition()
        row2, col2 = self.blueLord.getPosition()
        if col1 == col2:
            up, down = max(row1, row2), min(row1, row2)
            column = np.array(self.grid)[:, col1]
            for i in range(down + 1, up):
                if column[i] is not None:
                    return False
            return True
        return False
