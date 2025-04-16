from .pieces import Cannon, Chariot, Advisor, Horse, Elephant, General, Soldier, Piece

class Board:
    def __init__(self, gameUI):
        self.gameUI = gameUI
        self.current_turn = 'r'
        self.fromPos = None
        self.lastPos = None
        self.picked_up_piece = None
        self.possible_moves = []
        self.config = [[None for i in range(9)] for i in range(10)]
        self.setup_new_board()
    
    def setup_new_board(self):
    
        self.config[0] = [Chariot((0,0), 'b', self), Horse((0,1), 'b', self), Elephant((0,2), 'b', self), \
                Advisor((0,3), 'b', self), General((0,4), 'b', self), Advisor((0,5), 'b', self), \
                    Elephant((0,6), 'b', self), Horse((0,7), 'b', self), Chariot((0,8), 'b', self)]
        self.config[2] = [None, Cannon((2,1), 'b', self), None, None, None, None, None, Cannon((2,7), 'b', self), None]

        self.config[9] = [Chariot((9,0), 'r', self), Horse((9,1), 'r', self), Elephant((9,2), 'r', self), \
                Advisor((9,3), 'r', self), General((9,4), 'r', self), Advisor((9,5), 'r', self), \
                    Elephant((9,6), 'r', self), Horse((9,7), 'r', self), Chariot((9,8), 'r', self)]
        self.config[7] = [None, Cannon((7, 1), 'r', self), None, None, None, None, None, Cannon((7, 7), 'r', self), None]    

        for i in range(0,9,2):
            self.config[3][i] = Soldier((3, i), 'b', self)
            self.config[6][i] = Soldier((6, i), 'r', self)
    
    def get_piece(self, pos:tuple)->Piece:
        return self.config[pos[0]][pos[1]]
    
    def set_piece(self, pos:tuple, piece:Piece):
        self.config[pos[0]][pos[1]] = piece
    
    def on_board(self, position:tuple)->bool:
        if position[0] > -1 and position[1] > -1 and position[0] < 10 and position[1] < 9:
            return True

    def is_inCheck(self, team: str) ->bool:
        if team!=self.current_turn:
            return False
        General_pos = self.find_General(team)
        #opponent's all possible moves:
        for row in self.config:
            for piece in row:
                if(piece and piece.team!=team):
                    if General_pos in piece.get_possible_moves(self):
                        return True     
        return False
    def isCheckMated(self):
        for row in self.config:
            for piece in row:
                if(piece and piece.team==self.current_turn):
                    if(piece.get_valid_moves(self)):
                        return False
        return True

    def find_General(self, team:str):
        for i in range(10):
            for j in range(9):
                piece = self.config[i][j]
                if(piece and piece.team==team and piece.type=='k'):
                    return (i, j)

    def General_face_each_other(self) ->bool:
        red_General_pos = self.find_General('r')
        black_General_pos = self.find_General('b')
        if red_General_pos[1] != black_General_pos[1]:
            return False
        return all(not self.config[x][red_General_pos[1]] for x in range(black_General_pos[0]+1, red_General_pos[0]))
    
    def Find_Node(self, pos: tuple, WIDTH):
        interval = WIDTH // 9
        y, x = pos
        rows = y // interval
        columns = x // interval
        return int(rows), int(columns)

    def handle_click(self, pos: tuple):
        
        my, mx = pos
        y = my // self.tile_width
        x = mx // self.tile_width
        
        if (x, y) in self.possible_moves and self.selected_pos:
            # performing a valid move
            row, col = self.selected_pos ## coords of the chess piece we picked up
            chessPiece = self.config[row][col]

            chessPiece.move(self, (x,y))  
            self.selected_pos = []
            self.possible_moves = []
            self.current_turn = 'b' if self.current_turn=='r' else 'r'

            print(self.convert_to_readable())
        
        elif(self.config[x][y] and self.config[x][y].team==self.current_turn):                    
            self.possible_moves = self.config[x][y].get_valid_moves(self)
            if self.possible_moves:
                self.selected_pos = x,y
        else:
                self.selected_pos = []
                self.possible_moves = []
                print('Can\'t select')
    
    def get_game_state(self):
        return [self.possible_moves, self.fromPos, self.lastPos, self.picked_up_piece]
                
    def handle_mouse_down(self, pos):
        x, y = pos
        if (x, y) in self.possible_moves and self.fromPos:
            # performing a valid move
            row, col = self.fromPos ## coords of the chess piece we picked up
            self.lastPos = (row, col)
            chessPiece = self.config[row][col]

            captured = chessPiece.move(self, (x,y))  
            if captured:
                self.gameUI.play_sound('capture')
            else:
                self.gameUI.play_sound('move')
            self.fromPos = None
            self.possible_moves = []
            self.current_turn = 'b' if self.current_turn=='r' else 'r'
            
            #print(convert_to_readable(board))
        
        elif(self.config[x][y] and self.config[x][y].team==self.current_turn):     
            # pick up a piece
            self.possible_moves = self.config[x][y].get_valid_moves(self)
            if self.possible_moves:
                self.fromPos = x,y
                self.picked_up_piece = self.config[x][y]
        
        else:
                self.fromPos = None
                self.possible_moves = []
                print('Can\'t select')
                
    def handle_mouse_up(self, pos):
        x, y = pos
        if (x, y) in self.possible_moves and self.picked_up_piece and self.fromPos:
            row, col = self.fromPos
            self.lastPos = (row, col)
            
            captured = self.picked_up_piece.move(self, (x,y))  
            if captured:
                self.gameUI.play_sound('capture')
            else:
                self.gameUI.play_sound('move')  
            self.fromPos = None
            self.possible_moves = []
            self.current_turn = 'b' if self.current_turn=='r' else 'r'
            
        self.picked_up_piece = None

    def convert_to_readable(self):
        output = ''
        for i in self.config:
            for j in i:
                try:
                    output += j.team + j.type + ', '
                except:
                    output +=  '  , '
            output += '\n'
        return output