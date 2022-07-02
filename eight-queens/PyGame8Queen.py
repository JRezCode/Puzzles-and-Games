from qt import QtGui, QtWidgets, QtCore, _enum, _exec
import uuid

# python 8 queens problem
DEBUG = False
GAME_REPR = True
DATA_REPR = True
BOARD_STATUS = True


class Chesssquare():
    def __init__(self, file, rank):
        self.file = (file)
        self.rank = (rank)
        self.piece = Gamepiece(None,file,rank)
        self.reset_square()

    def get_location(self):
        return 

    def get_position(self):
        return (self.file,self.rank)
    
    def has_piece(self):
        if self.piece.piece_type is None:
            return False
        return True

    def set_piece(self,type):
        self.piece = Gamepiece(type,self.file,self.rank)

    def get_piece(self):
        return self.piece

    def reset_square(self):
        file = self.file
        rank = self.rank
        self.piece = Gamepiece(None,file,rank)

    def __str__(self):
        if self.piece.piece_type is None:
            return "%s%s" % (self.file, self.rank) + ":  \t"
        return "%s%s" % (self.file, self.rank) + ":" + "%s\t" % (self.piece)

    def __repr__(self):
        return "Square" + str(self.get_piece())


class Board():
    def __init__(self, grid_size):
        self.b_id = uuid.uuid1()
        self.b_move_history = []
        global board
        board = self.board_structure(grid_size)  #assigned to a global board
        self.make_chessboard(grid_size)
        # global games
        # games = {}
        # games[self.b_id] = self

    def game_summary(self):
        summary = "".join(str(x) for x in self.b_move_history)
        return summary

    @staticmethod
    def board_structure(size):
        brd = []
        for i in range(size):
            brd.append([])
            for j in range(size):
                brd[i].append(None)         #filled with null/none
        return brd

    @staticmethod
    def make_chessboard(size):
        for i in range(size):
            for j in range(size):
                board[i][j] = (Chesssquare(i,j))        # now filled with chesssquares

    def __repr__(self):
        if DEBUG:
            print("Board __repr__ was called")
        return str(CLI_Output(self))

class Queens(Board):
    def __init__(self, g_size):
        ##call constructor of Board returns a 2-d data structure
        super().__init__(g_size)
        self.b_solved = False
        self.setup_queens()

    @staticmethod
    def setup_queens():
        for i in board:
            i[0].set_piece("Qu")
 
    def board_solved(self):
        algorithm_flag = 1
        if algorithm_flag == 1:
            self.board_solved_brute()
        if algorithm_flag == 2:
            self.board_solved_backtracking()
        
    def board_solved_backtracking(self):
        return False

    def board_solved_brute(self):
        # O(n) algorithm for rows
        for row in board:
            if [x.has_piece() for x in row].count(True) > 1:
                print("unsolved - row with 2 pieces")
                return False
        # Algorithm for columns
        for i in range(len(board)):
            if [col[i].has_piece() for col in board].count(True) > 1:
                print("unsolved - col with 2 pieces")
                return False

    def checkdiagonals():
    # Algorithm to check diagonals
        # for a in [0,1,2,3]:
        #     if [board[i+1][i].has_piece() for i in range(len(board))].count(True) > 1:
        #         print("unsolved - diagonal with 2 pieces on it")
        #     return False
        # for a,b in [(0,0),(1,0),(0,1),(2,0),(0,2),(3,0),(0,3)]:
        #     if [board[i+a][i+b].has_piece() for i in range(len(board))].count(True) > 1:
        #         print("unsolved - diagonal with 2 pieces on it")
        #     return False
        return True
    
class CLI_Output(Board):
    def __init__(self,boardgame):
        return None

    def __str__(self):
        my_repr = ''
        chess_repr = "Chessboard (CLI) Representation:\n"
        file = 'A'
        for i in range(len(board)):
            if i > 0:
                chess_repr += "\n"
            rank = 1
            if i > 0:
                file = chr(ord(file) + 1)
            for j in range(len(board)):
                if j > 0:
                    rank += 1
                chess_repr += file + str(rank) +':'+ str(board[i][j])[-3:-1]+"\t"
        chess_repr += "\n"
        my_repr += chess_repr
        if DATA_REPR:
            data_repr = "Data Representation:\n"
            my_repr += data_repr + "".join(map(''.join,str(board)))
        return my_repr



class Gamepiece():
    def __init__(self, type, file, rank):
        self.piece_type = type
        self.piece_location = (file,rank)
        if type is not None:
            self.place_piece(file, rank, type)
    #         self.place_piece(file,rank,type)  #returns a file,rank tuple
        self.capture = False    #capture

    def place_piece(self, file, rank,type):
        board[file][rank].piece = self
        return file,rank

    def get_square(self):
        file = self.piece_location[0]
        rank = self.piece_location[1]
        return board[file][rank]

    # def show_square(self):
    #     return str(self) + '@' + ''.join(map(str,self.piece_location))

    def move_piece(self, x,y):
        if self.islglmove(x,y):
            # save location for reset
            old = self.get_square()
            b_move_history.append([self.piece_type,(old.file,old.rank),self.piece_location])
            if board[x][y].has_piece():
                #logic for capture made including points, and replacement(?)
                print("Capture")
                capture = board[x][y].piece
                b_move_history[-1].extend(['captures',str(capture)])
            self.piece_location = self.place_piece(x,y,self.piece_type)
            old.reset_square()
            # if self.get_square().location.board_solved():
            if DEBUG:
                print("debug - Move " + str(len(b_move_history)) + ":" + str(b_move_history[-1]))
            return True
        else:
            print("illegal move!")
        return False 

    def __str__(self):
        if self.piece_type is None:
            return ""
        return str(self.piece_type)

class Queen(Gamepiece):
    def __init__(self,f,r):
        super().__init__("Qu",f,r)
    
    def islglmove(self,x,y):
        #logic for move by a queen along file or rank
        if self.piece_location[0] is x or self.piece_location[1] is y:
            return True
        #logic for move by queen along diag
        elif abs(x - self.piece_location[0]) is abs(y - self.piece_location[1]):
            return True
        else:
            return False

def main():
    b = Queens(8)
    print(b)


# #Unit Tests for Queen Gamepieces
#     q2 = Queen(0,1)
#     #test a move that is allowed
#     q2.move_piece(2,1)
#     print(b)

#     #test a move that is not allowed
#     q2.move_piece(0,2)    
#     print(b)

#     #test a move that is allowed
#     q2.move_piece(2,3)
#     print(b)

#     #test a move to where another piece is, i.e. takes piece
#     q2.move_piece(0,3)    
#     print(b)

    # print(b.game_summary())

    # user input/output for game start
    #choice = input()
    # board = new_game(game_type,game_difficulty_interactive)
    # b.place_queen(1,1)
    # b.place_queen(0,0)
    # print(b.board)
    # print(b.board[0])

main()

# class queen(boardpiece):
#     def __init__(self, piece_type):
#         super().__init__(piece_type)

#     def place_queen(self,file,rank):
#         self.board[file][rank] = 'q'


# def printSolution(board):
#     for i in range(N):
#         for j in range(N):
#             print(board[i][j], end = " ")
#         print()

    # define options for entering queen position by rank/file, rank or file
    # input/output with error handling


   # def board_Nqueens(self,n):
    #     self.board_structure(n)

    #     result = []
    #     #with alphabet list
    #     start = ord('A')
    #     files = []
    #     for i in range(grid):
    #         files.append(chr(start + i))
    #     for file in files:
    #         result.append([])
    #         for ranks in range(grid):
    #             val = file + str(ranks+1)
    #             result[ord(file)-ord('A')].append(val)
    #     return result
    
    # def new_board_game(board):
    #     dict


#  b. pieces - object

# 2. Functions 
#  a.  the rules of the game
#  b.  helping functions (New board / Losing board / Winning board)
#  c.  undo -  optional if it is not a lot of extra programming
# 3. Graphics
#  a. qt for ctype python rendering
#  b. board empty
#  c. redrawing the board with pieces
# 4. Main program (menu)
#  a. Manual
#  b. Automatic
#  c. Run gaming loop with while(true) statement


