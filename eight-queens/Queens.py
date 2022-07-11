import uuid
import Solutions
import sys

#TODO: 
# 1) cleanup and simplify the design in this code, 
#   a) place queens at locations by choice
#   b) move placed queens from location to location by choice (no restriction other than has piece or not)
#   c) logic for solutions of 8 queens game only, remove the regular chess elements like legal moves, etc.
# 2) introduce gui elements, 
# 3) introduce new functionality
#   a) Finding more solutions using alg1, specify how many, maybe randomize the seed and count the # of operations
#   b) Implement Backtracking algorithm, compare the efficiency of the two algorithms
#   c) Also create interactive way to cycle through solutions, maybe using a file to store them and implement a check solution button that verifies etc.
#   d) If possible create some kind of HINT feature that helps provide some AI to the program

# python 8 queens problem
DEBUG = True
MODE_GAME = 2

class Game():
    def __init__(self):
        global games
        games = {}

        global move_history
        move_history = {}
  
        self.b_game_mode = MODE_GAME    # 1,2  for auto/interactive

    def fetch_board(self,uuid):
        return games[uuid]

    @staticmethod
    def new_game(board):
        if DEBUG:
            print("newboard: " + str(board.b_id))
        games[board.b_id] = board
        move_history[board.b_id] = []

class Square():
    def __init__(self, board, file, rank):
        self.board = board
        self.location = (file,rank) #location[0], location[1]
        self.piece = Queen(None,file,rank, board)
        self.reset_square()

    def set_piece(self,type):
        self.piece = Queen(type,self.location[0],self.location[1],self.board)
        return True

    def has_piece(self):
        if self.piece.piece_type is None:
            return False
        return True

    def get_piece(self):
        return self.piece

    def get_piece_type(self):
        return self.piece.piece_type

    def get_board(self):
        return self.board.brd

    def get_board_id(self):
        return self.board.b_id

    def reset_square(self):
        self.set_piece(None)

    def __str__(self):
        if self.piece.piece_type is None:
            return "%s%s" % (self.location[0], self.location[1]) + ":  \t"
        return "%s%s" % (self.location[0], self.location[1]) + ":" + "%s\t" % (self.piece)

    def __repr__(self):
        return "Square" + str(self.get_piece())
       
class Board():
    def __init__(self, grid_size):
        self.b_id = uuid.uuid1()
        self.size = grid_size
        self.brd = self.board_structure(grid_size)
        self.b_solved = False
        
        games[self.b_id] =  self.brd    #games is global
        self.make_chessboard()          #initial piece placement method
        move_history[self.b_id] = []
        self.add_to_games()
    
    def add_to_games(self):
        games[self.b_id] =  self.brd    #map board to games

    def make_chessboard(self):
        for i in range(self.size):
            for j in range(self.size):
                self.brd[i][j] = (Square(self,i,j))        # chessboard with chesssquares

    def board_solved(self):
        algorithm_flag = 1
        if algorithm_flag == 1:
            self.board_solved_brute()
        if algorithm_flag == 2:
            self.board_solved_backtracking()
        
    def game_summary(self):
        return "".join(str(x) for x in self.b_move_history)
        
    def get_board(self):
        return games[self.b_id]

    @staticmethod
    def board_structure(size):
        return [[None for i in range(size)] for i in range(size)]
        
    @staticmethod
    def setup_queens(board):
        for i in board:
            i[0].set_piece("Qu")
 
    def __repr__(self):
        return str(CLI_Output(self))

class CLI_Output(Board):
    def __init__(self,boardgame):
        self.b_id = boardgame.b_id
        self.game = boardgame
        return None

    def __repr__(self):
        my_repr = ''
        if True:
            chess_repr = "Chessboard (CLI) Representation:\n"
            file = 'A'
            for i in range(self.game.size):
                rank = 1
                if i > 0:
                    chess_repr += "\n"
                    file = chr(ord(file) + 1)
                for j in range(self.game.size):
                    if j > 0:
                        rank += 1
                    chess_repr += file + str(rank) +':'+ str(self.game.brd[i][j])[-3:-1]+"\t"
            chess_repr += "\n"
            my_repr += chess_repr
        if False:
            data_repr = "Data Representation:\n"
            my_repr += data_repr + "".join(map(''.join,str(games[self.b_id].brd)))
        return my_repr

class Queen():
    def __init__(self, type, file, rank, board):
        self.piece_type = type
        self.file = file
        self.rank = rank
        self.b_id = board.b_id
        
        if type is not None:
            self.place_piece()      #returns a file,rank tuple

        # self.piece_location = board.brd[file][rank]
    # def fetch_square(self):
        # return self.piece_location

    def set_square(self,file,rank):
        old_square = games[self.b_id].brd[self.file][self.rank]
        games[self.b_id].brd[file][rank] = self
        self.file = file
        self.rank = rank
        old_square.reset_square()       
        return (self.file,self.rank)
        
    def fetch_square(self):
        return games[self.b_id].brd[self.file][self.rank]

    def place_piece(self):
        if self.piece_type is None:
            self.fetch_square().piece = self
            return (self.file,self.rank)
        return False

    def move_piece(self, x,y):
        if self.piece_type is None:
            print("No piece to move.")
            return False
        elif self.islglmove(x,y):
            old = fetch.square()    # save square for reset
            #add move history here
            # move_history[self.get_board_id()].append([self.get_piece_type(),self.location,(x,y)])
            if self.get_board()[x][y].has_piece():
                print("Square is occupied.")
                return False
            else:
                self.set_square(x,y)
            # if DEBUG:
                # print("debug - Move " + str(len(move_history[self.get_board_id()])) + ":" + str(move_history[self.get_board_id()][-1]))
            # return True

    def islglmove(self,x,y):
        #logic for move by a queen along file or rank
        if self.file is x or self.rank is y:
            if self.get_board()[x][y].has_piece():
                return False
            return True
        #logic for move by queen along diag
        elif abs(x - self.file) is abs(y - self.rank):
            if self.get_board()[x][y].has_piece():
                return False
            return True
        else:
            return False

    def __str__(self):
        if self.piece_type is None:
            return ""
        return str(self.piece_type) + '@' + ''.join(map(str,(self.file,self.rank)))

def main():
    g = Game()

# #Testing# Boards #
    g.new_game(Board(4))
    g.new_game(Board(6))
    g.new_game(Board(8))
    g.new_game(Board(10))
    g.new_game(Board(12))

    for uuid in games:
        print(g.fetch_board(uuid))

# #Testing#  Queen Placement #

    for uuid in games:
        Board.setup_queens(games[uuid].brd)
        print(g.fetch_board(uuid).brd)
        

#  #Testing#  Solution Algorithms #
    # for game in games:
        # if MODE_GAME == 1:
            # if DEBUG:
                # print("Solving...")
            # Solutions.solveNQ(games[uuid])
            # print(g)

        # elif MODE_GAME == 2:
            # Board.setup_queens(games[uuid])
      


        #Print the empty boards
        # print(g.fetch_board(uuid))
        #test move a piece
        # g.fetch_board(uuid).brd[0][0].move_piece(1,1)

        #Solve them
        # Solutions.solveNQ(g.fetch_board(uuid).brd)

# 

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


