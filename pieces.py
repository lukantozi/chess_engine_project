from utils import index_to_square

# create a general piece class
class Piece:
    def __init__(self, color):
        self.color = color
    

# create a Pawn class as a Piece's child
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False
        self.value = 100

    def __repr__(self):
        return "♙" if self.color == "b" else "♟"
    
    def clone(self):
        p = Pawn(self.color)
        p.has_moved = self.has_moved
        p.value = self.value
        return p
    
    # outputting valid moves for pawns
    def valid_moves(self, r, c, board):
        squares = []
        dir = -1 if self.color == 'w' else +1
        if board.in_bounds(r+dir, c) and board.piece_at(r+dir, c) == None: # if the square ahead is empty, add
            squares.append(index_to_square(r+dir, c))

        if not self.has_moved and board.in_bounds(r + (2*dir), c) and (board.piece_at(r + (2*dir), c) == None) and (board.piece_at(r + dir, c) == None): # if the squares two ahead is empty, add
            squares.append(index_to_square((r+2*dir), c))

        if board.in_bounds(r+dir, c+1): # check if the square exists
            if board.piece_at(r+dir, c+1) is not None and board.piece_at(r+dir, c+1).color != self.color: # if there is an enemy piece diagonally, add
                squares.append(index_to_square(r+dir, c+1))

        if board.in_bounds(r+dir, c-1): # check if the square exists
            if board.piece_at(r+dir, c-1) is not None and board.piece_at(r+dir, c-1).color != self.color: # if there is an enemy piece diagonally, add
                squares.append(index_to_square(r+dir, c-1))

        return squares
    
# create a Rook subclass
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False
        self.value = 500
    
    def __repr__(self):
        return "♖" if self.color == "b" else "♜"
    
    def clone(self):
        r = Rook(self.color)
        r.has_moved = self.has_moved
        r.value = self.value
        return r
    
    def valid_moves(self, r, c, board): # outputting valid moves for a rook
        delta = [ # movement directions
            (-1, 0),
            (+1, 0),
            (0, +1),
            (0, -1),
        ]
        squares = []
        for dr, dc in delta:
            row, col = r + dr, c + dc # reset starting coords after finishing up ray
            while board.in_bounds(row, col): # check if in bounds
                if board.piece_at(row, col) is None: # check if empty square ahead, add
                    squares.append(index_to_square(row, col))
                    row += dr
                    col += dc
                    continue
                # check if enemy ahead, add, stop
                if board.piece_at(row, col) is not None and board.piece_at(row, col).color != self.color:
                    squares.append(index_to_square(row, col))
                    break
                # check if friend ahead, stop
                if board.piece_at(row, col) is not None and board.piece_at(row, col).color == self.color:
                    break
        return squares
        
# create a Bishop subclass
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False
        self.value = 320

    def __repr__(self):
        return "♗" if self.color == "b" else "♝"
    
    def valid_moves(self, r, c, board):
        delta = [ # movement directions
            (-1, -1),
            (-1, +1),
            (+1, -1),
            (+1, +1)
        ]
        squares = []
        for dr, dc in delta:
                row, col = r + dr, c + dc # reset starting coords after finishing up ray
                while board.in_bounds(row, col): # check if in bounds
                    if board.piece_at(row, col) is None: # check if empty square ahead, add
                        squares.append(index_to_square(row, col))
                        row += dr
                        col += dc
                        continue
                    # check if enemy ahead, add, stop
                    if board.piece_at(row, col) is not None and board.piece_at(row, col).color != self.color:
                        squares.append(index_to_square(row, col))
                        break
                    # check if friend ahead, stop
                    if board.piece_at(row, col) is not None and board.piece_at(row, col).color == self.color:
                        break
        return squares

# create a Queen subclass
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False
        self.value = 900

    def __repr__(self):
        return "♕" if self.color == "b" else "♛"
 
    # outputting valid moves for a queen
    def valid_moves(self, r, c, board):
        delta = [ # movement directions
            (-1, 0),
            (+1, 0),
            (0, +1),
            (0, -1),
            (-1, -1),
            (-1, +1),
            (+1, -1),
            (+1, +1)
        ]
        squares = []
        for dr, dc in delta:
                row, col = r + dr, c + dc # reset starting coords after finishing up ray
                while board.in_bounds(row, col): # check if in bounds
                    if board.piece_at(row, col) is None: # check if empty square ahead, add
                        squares.append(index_to_square(row, col))
                        row += dr
                        col += dc
                        continue
                    # check if enemy ahead, add, stop
                    if board.piece_at(row, col) is not None and board.piece_at(row, col).color != self.color:
                        squares.append(index_to_square(row, col))
                        break
                    # check if friend ahead, stop
                    if board.piece_at(row, col) is not None and board.piece_at(row, col).color == self.color:
                        break
        return squares
    
# create a Knight subclass
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False
        self.value = 310

    def __repr__(self):
        return "♘" if self.color == "b" else "♞"
        
    # outputting valid moves for a knight
    def valid_moves(self, r, c, board):
        delta = [ # movement directions
            (+1, +2),
            (+1, -2),
            (+2, +1),
            (+2, -1),
            (-1, +2),
            (-1, -2),
            (-2, +1),
            (-2, -1)
        ]
        squares = []
        for dr, dc in delta:
                row, col = r + dr, c + dc # reset starting coords after finishing up ray
                if board.in_bounds(row, col): # check if in bounds
                    if board.piece_at(row, col) is None: # check if empty square ahead, add
                        squares.append(index_to_square(row, col))
                        row += dr
                        col += dc
                        continue
                    # check if enemy ahead, add, stop
                    if board.piece_at(row, col) is not None and board.piece_at(row, col).color != self.color:
                        squares.append(index_to_square(row, col))
                        continue
                    # check if friend ahead, stop
                    if board.piece_at(row, col) is not None and board.piece_at(row, col).color == self.color:
                        continue
        return squares
    
    #def __repr__(self):
        #return f"{self.color[0].upper()}{self.__class__.__name__[1].upper()}"
    
# create a king subclass
class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False
        self.has_castled = False
        self.value = 9999999999

    def __repr__(self):
        return "♔" if self.color == "b" else "♚"

    def clone(self):
        k = King(self.color)
        k.has_moved = self.has_moved
        k.has_castled = self.has_castled
        k.value = self.value    
        return k

    # outputting valid moves for a king
    def valid_moves(self, r, c, board):
        delta = [ # movement directions
            (-1, 0),
            (+1, 0),
            (0, +1),
            (0, -1),
            (-1, -1),
            (-1, +1),
            (+1, -1),
            (+1, +1)
        ]
        squares = []
        for dr, dc in delta:
                row, col = r + dr, c + dc # reset starting coords after finishing up ray
                if board.in_bounds(row, col): # check if in bounds
                    if board.piece_at(row, col) is None: # check if empty square ahead, add
                        squares.append(index_to_square(row, col))
                        row += dr
                        col += dc
                        continue
                    # check if enemy ahead, add, stop
                    if board.piece_at(row, col) is not None and board.piece_at(row, col).color != self.color:
                        squares.append(index_to_square(row, col))
                        continue
                    # check if friend ahead, stop
                    if board.piece_at(row, col) is not None and board.piece_at(row, col).color == self.color:
                        continue
 
        return squares
    