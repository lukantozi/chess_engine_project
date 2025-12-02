from pieces import Pawn, Rook, Bishop, Queen, Knight, King

from utils import index_to_square, square_to_index

# Create a class for each square with colors, notations and pieces.
class Square:
    def __init__(self, color, notation):
        self.color = color  
        self.notation = notation
        self.piece = None # will add values
    
    def __repr__(self):
        if self.piece == None:
            return "-"
        else:
            return f"{self.piece}"

class Board:
    def __init__(self):
        # assign color and notation to each square
        self.grid = [[Square(alternator(r, c), index_to_square(r, c))
                      for c in range(8)] for r in range(8)]
        self._place_starting_pieces()
        self.turn = "w"
        self.in_check = False
        self.en_passant = False
        self.passant_move = []
        self.taken = None
        self.fifty = 50
        self.move_count = 0

    def clone(self): 
        new = Board.__new__(Board)
        new.turn = self.turn
        new.in_check = self.in_check
        new.en_passant = self.en_passant
        new.passant_move = self.passant_move
        new.taken = self.taken
        new.fifty = self.fifty
        new.move_count = self.move_count
        new.grid = [
            [Square(sq.color, sq.notation) for sq in row ]
            for row in self.grid
        ]
        for r in range(8):
            for c in range(8):
                piece = self.piece_at(r, c)
                if piece:
                    try:
                        new.grid[r][c].piece = piece.clone()
                    except AttributeError:
                        new.grid[r][c].piece = piece
        return new

    def __str__(self):
        r = ""
        for row in self.grid:
            for square in row:
                r = r + str(square) + " "
            r = r.rstrip() + "\n"
        return r[:-1]

    def _place_starting_pieces(self):
        back_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i in range(8):
            self.grid[6][i].piece = Pawn('w')
            self.grid[1][i].piece = Pawn('b')
            self.grid[0][i].piece = back_row[i]('b')
            self.grid[7][i].piece = back_row[i]('w')
    
    def in_bounds(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8
    
    def piece_at(self, r, c):
        return self.grid[r][c].piece
    
    def pseudo_moves_from(self, r, c): # generate pseudo moves for the piece at r, c
        piece = self.piece_at(r, c)
        if piece is None:
            return []
        moves = piece.valid_moves(r, c, self)
        
        if isinstance(piece, King) and not piece.has_moved:
            for rook_file in [0, 7]:
                rook = self.piece_at(r, rook_file)
                if isinstance(rook, Rook) and not rook.has_moved:
                    dir = 1 if rook_file > c else -1
                    enemy = collect_squares(self, alter_color(self.turn)) # all enemy piece indices
                    attacked = set()
                    for e_r, e_c in enemy:
                        for move in self.piece_at(e_r, e_c).valid_moves(e_r, e_c, self):
                            attacked.add(move)
                    path = [(r, sq_c) for sq_c in range(c+dir, rook_file, dir)]
                    if all(self.piece_at(rr, cc) is None for rr, cc in path):
                        king_way = [index_to_square(r, c), index_to_square(r, c+dir), index_to_square(r, c+2*dir)]
                        if not any(sq in attacked for sq in king_way):
                            moves = [index_to_square(r, rook_file)] + moves

        return moves
    
        
    
    def move_piece(self, start, end): # move the piece
        s_r, s_c = start # 0, 0 = (0, 0)
        e_r, e_c = end
        
        if self.piece_at(s_r, s_c) is None: # if empty square
            return 1
        if isinstance(self.piece_at(e_r, e_c), King):
            return False
        piece_50 = self.grid[s_r][s_c].piece
        piece2_50 = self.grid[e_r][e_c].piece
        piece = self.grid[s_r][s_c].piece
        destination = self.grid[e_r][e_c].piece
        if piece.color != self.turn:
            return 2
        else:
            if index_to_square(e_r, e_c) in (piece.valid_moves(s_r, s_c, self) + self.passant_move): # if the piece can go to the square
                if isinstance(piece, Pawn) and self.en_passant == True and index_to_square(e_r, e_c) in self.pseudo_moves_from(s_r, s_c) + self.passant_move:
                    self.en_passant = piece.valid_moves(s_r, s_c, self).pop()
                    dir = dir_from_color(self.turn)
                    self.taken = self.grid[e_r+dir][e_c].piece
                    self.grid[e_r+dir][e_c].piece = None
                    self.en_passant = False
                elif isinstance(piece, Pawn) and self.en_passant == True and index_to_square(e_r, e_c) not in self.pseudo_moves_from(s_r, s_c) + self.passant_move: # if en_passant not used
                    self.passant_move = piece.valid_moves(s_r, s_c, self).pop()
                    self.en_passant = False

                self.grid[s_r][s_c].piece = None # swap
                destination = self.grid[e_r][e_c].piece
                self.grid[e_r][e_c].piece = piece # pieces
                
                if isinstance(piece, Pawn): # promotion to queen for now
                    if e_r == 0:
                        self.grid[e_r][e_c].piece = Queen(self.turn)
                    elif e_r == 7:
                        self.grid[e_r][e_c].piece = Queen(self.turn)

                # en_passant
                if isinstance(piece, Pawn) and abs(e_r - s_r) == 2:
                    dir = dir_from_color(self.turn)
                    for col_dir in [-1, 1]:
                        if not self.in_bounds(e_r, e_c + col_dir):
                            continue
                        if isinstance(self.piece_at(e_r, e_c + col_dir), Pawn) and self.piece_at(e_r, e_c + col_dir).color == alter_color(self.turn):
                            self.en_passant = True
                            self.passant_move.append(index_to_square((e_r+dir), (e_c)))


                self.turn = alter_color(self.turn) # update the turn
                self.in_check = king_in_check(self, self.turn) # check and save if the opponent's king in check
            elif (isinstance(self.piece_at(s_r, s_c), King) and self.piece_at(s_r, s_c).has_moved == False) and (isinstance(self.piece_at(e_r, e_c), Rook) and self.piece_at(e_r, e_c).has_moved == False):
                self.piece_at(s_r, s_c).has_castled = True
                result = castle(self, s_c, e_c, self.turn)
                if result == 3:
                    self.piece_at(s_r, s_c).has_castled = False
                    return 3 # to indicate that the king is in check if castled
                
                return # to avoid undoing after castling successfully
            else:
                return False

            if king_in_check(self, alter_color(self.turn)): # check if after the move the mover's king is still in check
                self.grid[s_r][s_c].piece = piece # undo
                self.grid[e_r][e_c].piece = destination # move
                self.turn = alter_color(self.turn) # set back the turn
                if self.passant_move:
                    piece.valid_moves(s_r, s_c, self).append(self.passant_move)
                    self.en_passant = True
                    
                return 3
            
            if piece.has_moved == False:
                    piece.has_moved = True # update whether the piece has moved or not

            if piece_50 != None and piece2_50 != None:
                self.fifty = 50
            else:
                self.fifty -= 1
            
            if self.fifty == 0:
                return 5
            
            self.move_count += 1

            # detect checkmate/stalemate
            squares = collect_squares(self, self.turn) # find all pieces for the side that is in check
            not_check = False
            for r, c in squares:
                piece = self.grid[r][c].piece # get the single piece
                moves = self.pseudo_moves_from(r, c) # find it's valid moves
                for move in moves:
                    self.grid[r][c].piece = None # swap
                    ps_r, ps_c = square_to_index(move) 
                    piece_2 = self.grid[ps_r][ps_c].piece # save for later
                    self.grid[ps_r][ps_c].piece = piece # swap
                    if king_in_check(self, self.turn):
                        # undo the move
                        self.grid[r][c].piece = piece
                        self.grid[ps_r][ps_c].piece = piece_2
                        continue
                    # undo the move
                    self.grid[r][c].piece = piece
                    self.grid[ps_r][ps_c].piece = piece_2
                    not_check = True
            if not not_check:
                if self.in_check:
                    return 4 # checkmate
                else:
                    return 5 # stalemate


def king_square(self, color):
    for r in range(8):
        for c in range(8):
            p = self.piece_at(r, c)
            if isinstance(p, King) and p.color == color:
                return r, c


# check if there is empty space between the king and the rook and if the path is check-safe
def king_to_rook(self, rc, color):
    kr, kc = king_square(self, color)
    king = self.grid[kr][kc].piece
    if kc > rc:
        for c in range(kc - 1, rc, -1):
            if not self.grid[kr][c].piece == None:
                return False # there is a piece between them
            self.grid[kr][kc].piece = None
            self.grid[kr][c].piece = king
            # check if the king steps into the check by castling
            if c - rc >= 2: # only check columns king will travel on
                if king_in_check(self, color):
                    self.grid[kr][kc].piece = king
                    self.grid[kr][c].piece = None
                    return False
            self.grid[kr][kc].piece = king
            self.grid[kr][c].piece = None
    elif kc < rc:
        for c in range(kc + 1, rc, +1):
            if not self.grid[kr][c].piece == None:
                return False # there is a piece between them
            self.grid[kr][kc].piece = None
            self.grid[kr][c].piece = king
            # check if the king steps into the check by castling
            if rc - c >= 2: # only check columns king will travel on
                if king_in_check(self, color):
                    self.grid[kr][kc].piece = king
                    self.grid[kr][c].piece = None
                    return False
            self.grid[kr][kc].piece = king
            self.grid[kr][c].piece = None
    return True


def castle(self, kc, rc, color):
    if color == 'w':
        kr = 7
    else:
        kr = 0
    king = self.grid[kr][kc].piece
    if king_to_rook(self, rc, color):
        rook = self.grid[kr][rc].piece
        if kc < rc:
            king.has_moved = True
            rook.has_moved = True
            self.grid[kr][kc + 2].piece = king 
            self.grid[kr][kc + 1].piece = rook
            self.grid[kr][kc].piece = None
            self.grid[kr][rc].piece = None
            self.turn = alter_color(color)
        else:
            king.has_moved = True
            rook.has_moved = True
            self.grid[kr][kc - 2].piece = king
            self.grid[kr][kc - 1].piece = rook
            self.grid[kr][kc].piece = None
            self.grid[kr][rc].piece = None
            self.turn = alter_color(color)
    else:
        return 3


def king_in_check(self, color):
    king = king_square(self, color)
    if king:
        kr, kc = king_square(self, color) # find where the king is
        for r, c in collect_squares(self, alter_color(color)): # collect all the squares where the enemy pieces are
            if index_to_square(kr, kc) in self.pseudo_moves_from(r, c): # check if the enemy pieces can "take" the king
                return True # check!
    return False


# to alternate colors when assigning them b
def alternator(r, c):
    if (r + c) % 2 == 0:
        return 'w'
    else:
        return 'b'

# swap colors
def alter_color(c):
    return "b" if c == "w" else "w"

def dir_from_color(c):
    return 1 if c == 'w' else -1

# find one color piece squares
def collect_squares(self, color):
    squares = []
    for r in range(8):
        for c in range(8):
            p = self.piece_at(r, c)
            if p is not None and p.color == color:
                squares.append((r, c))
    return squares

def collect_moves(self, color):
    pieces = collect_squares(self, color)
    moves = []
    for piece in pieces:
        r, c = piece
        pseudo_moves = self.pseudo_moves_from(r, c)
        if pseudo_moves:
            for move in pseudo_moves:
                moves.append((index_to_square(r, c), move))
    return moves
