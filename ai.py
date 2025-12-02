from board import collect_squares, alter_color, collect_moves, king_square

from utils import square_to_index

from pieces import Pawn


def evaluation(board):
    #return material_eval(board, color) + material_eval(board, alter_color(color)) + king_safety(board, color) + mobility(board, color)
    w_mat = material_eval(board, "w")
    b_mat = material_eval(board, "b")
    w_safety = king_safety(board, "w")
    b_safety = king_safety(board, "b")
    w_cent = center_control(board, "w")
    b_cent = center_control(board, "b")
    w_mob = mobility(board, "w")
    b_mob = mobility(board, "b")
    net = (w_mat + w_safety + w_cent + w_mob) - (b_mat + b_safety + b_cent + b_mob)
    return net

def material_eval(board, color):
    pieces = collect_squares(board, color)
    eval = 0
    for r, c in pieces:
        eval += board.piece_at(r, c).value
    return eval


def minimax(board, color, depth, alpha=-float("inf"), beta=float("inf")):
    # depth zero or no moves
    moves = collect_moves(board, color)
    if depth == 0 or not moves:
        if not moves:
            if board.in_check:
                return (float("inf") if color == "w" else -float("inf")), None
            else:
                return 0, None
        return evaluation(board), None
        
    best_move = None
    
    if color == "w":
        max_eval = -float("inf")
        for (st, en) in moves:
            child = board.clone()
            stat = child.move_piece(square_to_index(st), square_to_index(en))
            # detect mate immediately
            if stat == 4:
                return float("inf"), (st, en)
            # skip illegal, walking in check moves
            if stat not in (None, 0):
                continue

            eval, _ = minimax(child, alter_color(color), depth-1, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = (st, en)
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval, best_move
        
    else:
        min_eval = float("inf")
        for (st, en) in moves:
            child = board.clone()
            stat = child.move_piece(square_to_index(st), square_to_index(en))
            # detect checkmate immediately
            if stat == 4:
                return -float("inf"), (st, en)
            
            if stat not in (None, 0):
                continue
            
            eval, _ = minimax(child, alter_color(color), depth-1, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = (st, en)
            beta = min(beta, min_eval)    
            if beta <= alpha:
                break
        return min_eval, best_move


def around_king_attacked(board, color):
    penalty = 0
    r, c = king_square(board, color)
    around_king = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, -1), (0, 0),]
    attacked_squares = all_attack_count(board, color)
    for dr, dc in around_king:
        if board.in_bounds(r+dr, c+dc):
            if (r+dr, c+dc) in attacked_squares:
                penalty -= 10
    return penalty

def pawn_shield(board, color):
    r, c = king_square(board, color)
    king = board.piece_at(r, c)
    penalty = 0

    attacked_squares = all_attack_count(board, color)
    if king.has_moved == False:
        files = [1, 0, -1]
        rank = 1 if color == "b" else -1
        for file in files:
            if board.in_bounds(r+rank, c+file):
                if isinstance(board.piece_at(r+rank, c+file), Pawn):
                    if board.piece_at(r+rank, c+file).has_moved and (r+rank, c+file) in attacked_squares:
                        penalty += 20
    return penalty

def castle_pen(board, color):
    r, c = king_square(board, color)
    king = board.piece_at(r, c)
    penalty = 0
    if king.has_castled:
        penalty += 40
    elif king.has_moved:
        penalty -= 10
    return penalty

def king_safety(board, color):
    return pawn_shield(board, color) + around_king_attacked(board, color) + castle_pen(board, color)

def center_control(board, color):
    center_score = 0
    center = {"d4", "e4", "d5", "e5"}
    moves = collect_moves(board, color)
    for _, en in moves:
        if en in center:
            center_score += 5
    return center_score

def all_attack_count(board, color): # returns e4, d4 etc.
    return [board.pseudo_moves_from(ps_r, ps_c) 
            for ps_r, ps_c in collect_squares(board, alter_color(color))]

def mobility(board, color):
    return len(collect_moves(board, color))