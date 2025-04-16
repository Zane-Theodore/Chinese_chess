import pygame

class Piece:
    def __init__(self, position, team, board, type):
        self.team = team
        self.type = type
        self.position = position
        self.x, self.y = position
        self.board = board
        self.has_moved = False

    def get_possible_moves(self, board):
        pass

    """ Only valid moves are taken into account
    To sort moves that are valid, perform a fake move first and check if team's king 
    is in check or not"""
    def get_valid_moves(self, board):
        valid_moves = []
        possible_moves = self.get_possible_moves(board)
        for goal_x, goal_y in possible_moves:
            captured = board.get_piece((goal_x,goal_y))
            board.set_piece((goal_x,goal_y), self)
            board.set_piece((self.x,self.y), None)
            if not board.is_inCheck(self.team) and not board.General_face_each_other():
                valid_moves.append((goal_x, goal_y))
            board.set_piece((goal_x,goal_y), captured)
            board.set_piece((self.x,self.y), self)
        return valid_moves

    def move(self, board, coords:tuple):
        captured = board.get_piece((coords[0],coords[1])) 
        board.set_piece((coords[0],coords[1]), self)
        board.set_piece((self.x,self.y), None)
        self.x, self.y = coords       
        return captured
    
class Advisor(Piece):
    def __init__(self, position, team, board, type='a'):
        super().__init__(position, team, board, type)
        self.position = position
        self.x, self.y = position
        self.image = pygame.image.load('assets/images/' + self.team +'_Advisor.png')
        self.notation = 'A'

    def get_possible_moves(self, board):
        moves = []
        # advisor can only move diagonally in palace
        positions = {'b':[(0,3),(0,5), (1,4), (2,3), (2,5)],
                    'r': [(9,3), (9,5), (8,4), (7,3), (7,5)]}
        for (x,y) in positions[self.team]:
            if (board.get_piece((x,y)) == None or board.get_piece((x,y)) .team != self.team) \
                and y!=self.y and abs(self.y-y)==1:
                moves.append((x,y))
        return moves
    
class Cannon(Piece):
    def __init__(self, position, team, board, type='c'):
        super().__init__(position, team, board, type)
        self.position = position
        self.x, self.y = position
        self.image = pygame.image.load('assets/images/' + self.team +'_Cannon.png')
        self.notation = 'C'
    
    def get_possible_moves(self, board):
        moves = []

        cross = [[[self.x + i, self.y] for i in range(1, 10 - self.x)],
                [[self.x - i, self.y] for i in range(1, self.x + 1)],
                [[self.x, self.y + i] for i in range(1, 9 - self.y)],
                [[self.x, self.y - i] for i in range(1, self.y + 1)]]

        for direction in cross:
            may_jump = False
            for positions in direction:
                if board.on_board(positions):
                    if board.get_piece((positions[0],positions[1])) == None and not may_jump:
                        moves.append((positions[0], positions[1]))
                    elif board.get_piece((positions[0],positions[1])) and not may_jump:
                        may_jump = True
                    elif board.get_piece((positions[0],positions[1]))  and may_jump:
                        if board.get_piece((positions[0],positions[1])).team!=self.team:
                            moves.append((positions[0], positions[1]))
                        break
        return moves
    
class Chariot(Piece):
    def __init__(self, position, team, board, type='r'):
        super().__init__(position, team, board, type)
        self.position = position
        self.x, self.y = position
        self.image = pygame.image.load('assets/images/' + self.team +'_Chariot.png')
        self.notation = 'R'

    
    def get_possible_moves(self, board):
        moves = []

        cross = [[[self.x + i, self.y] for i in range(1, 10 - self.x)],
                [[self.x - i, self.y] for i in range(1, self.x + 1)],
                [[self.x, self.y + i] for i in range(1, 9 - self.y)],
                [[self.x, self.y - i] for i in range(1, self.y + 1)]]

        for direction in cross:
            for positions in direction:
                if board.on_board(positions):
                    if board.get_piece((positions[0],positions[1])) == None:
                        moves.append((positions[0], positions[1]))
                    else:
                        if board.get_piece((positions[0],positions[1])).team != self.team:
                            moves.append((positions[0], positions[1]))
                        break
        return moves
    
class Elephant(Piece):
    def __init__(self, position, team, board, type='e'):
        super().__init__(position, team, board, type)
        self.position = position
        self.x, self.y = position
        self.image = pygame.image.load('assets/images/' + self.team +'_Elephant.png')
        self.notation = 'E'
    
    def get_possible_moves(self, board):
        # elephant's movement is restricted to only 7 board positions
        positions = {'b':[(0,2),(0,6), (2,0), (2,4), (2,8), (4,2), (4,6)],
                    'r': [(9,2), (9,6), (7,0), (7,4), (7,8), (5,2), (5,6)]
                    }
        moves = []
        for (x,y) in positions[self.team]:
            if (board.get_piece((x,y)) == None or board.get_piece((x,y)).team != self.team) \
                and x!=self.x and y!=self.y and abs(self.y-y)==2 \
                and not board.get_piece(((self.x+x)//2,(self.y+y)//2)):
                moves.append((x,y))

        return moves
    
class Horse(Piece):
    def __init__(self, position, team, board, type='h'):
        super().__init__(position, team, board, type)
        self.poistion = position
        self.x, self.y = position
        self.image = pygame.image.load('assets/images/' + self.team +'_Horse.png')
        self.notation = 'H'

    def get_possible_moves(self, board):
        moves = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i ** 2 + j ** 2 == 5 and board.on_board((self.x + i, self.y + j)):
                    if board.get_piece((self.x + i,self.y + j)) == None or \
                    board.get_piece((self.x + i,self.y + j)).team != self.team:
                        if i**2==4 and not board.get_piece((self.x+i//2,self.y)):
                            moves.append((self.x + i, self.y+j))
                        elif j**2==4 and not board.get_piece((self.x,self.y+j//2)):
                            moves.append((self.x+i, self.y + j))

        return moves
    
class General(Piece):
    def __init__(self, position, team, board, type='k'):
        super().__init__(position, team, board, type)
        self.position = position
        self.x, self.y = position
        self.image = pygame.image.load('assets/images/' + self.team +'_General.png')
        self.notation = 'G'
    
    def get_possible_moves(self, board):
        moves = []
        # King can only move orthogonally in palace
        positions = {'b':[(0,3), (0,4),(0,5), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5)],
                    'r': [(9,3), (9,4), (9,5), (8,3), (8,4), (8,5), (7,3), (7,4), (7,5)]}
        for (x,y) in positions[self.team]:
            if (board.get_piece((x,y))  == None or board.get_piece((x,y)) .team != self.team) \
                and (self.x-x)**2+(self.y-y)**2==1:
                moves.append((x,y))

        return moves
    
class Soldier(Piece):
    def __init__(self, position, team, board, type='s'):
        super().__init__(position, team, board, type)
        self.position = position
        self.x, self.y = position
        self.image = pygame.image.load('assets/images/' + self.team + '_Soldier.png')
        self.notation = 'S'

    def get_possible_moves(self, board):
        moves = []

        # black and red Soldiers have different directions
        if self.team == 'b':
            l = [(self.x+1,self.y), (self.x,self.y-1), (self.x,self.y+1)] if self.x>=5 else [(self.x+1,self.y)]
            for x, y in l:
                if  board.on_board((x,y)) and (board.get_piece((x,y))==None or board.get_piece((x,y)).team!=self.team):
                    moves.append((x,y))    
        else:
            l = [(self.x-1,self.y), (self.x,self.y-1), (self.x,self.y+1)] if self.x<=4 else [(self.x-1,self.y)]
            for x, y in l:
                if board.on_board((x,y)) and (board.get_piece((x,y))==None or board.get_piece((x,y)).team!=self.team):
                    moves.append((x,y))
        return moves