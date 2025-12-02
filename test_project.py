from project import new_game, list_moves, best_ai_move

from board import collect_squares

from pieces import Rook, Pawn, King

def test_new_board_has_pawns_on_rank2():
    b = new_game()
    # if pawn hasn't moved, it can move to one/two squares ahead
    assert list_moves(b, "a2") == ["a3", "a4"]
    assert list_moves(b, "b2") == ["b3", "b4"]

def test_list_moves_pieces():
    b = new_game()
    # white knight's pseudo moves in the starting position
    assert set(list_moves(b, "b1")) == {"a3", "c3"}
    # other white knight's pseudo moves in the starting position
    assert set(list_moves(b, "g1")) == {"f3", "h3"}
    # black knigh't pseudo moves in the starting position
    assert set(list_moves(b, "b8")) == {"a6", "c6"}
    # other black knight's pseudo moves in the starting position
    assert set(list_moves(b, "g8")) == {"f6", "h6"}

def test_immediate_capture():
    b = new_game()
    # clean board
    for r, c in collect_squares(b, "w") + collect_squares(b, "b"):
        b.grid[r][c].piece = None
    # create a new position
    b.grid[7][0].piece = Rook("w")  # a1
    b.grid[6][0].piece = Pawn("b")  # a2
    # to avoid indexing issues
    b.grid[6][0].piece.has_moved = True
    b.grid[7][7].piece = King("w")  # h1
    b.grid[0][7].piece = King("b")  # h8
    # the most material greedy move
    move = best_ai_move(b, "w", 1)
    assert move == ("a1", "a2")