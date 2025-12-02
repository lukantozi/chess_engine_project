import sys
import os
import json
import re

from board import Board
from utils import square_to_index
from ai import minimax



# functions to test
def new_game():
    # start a fresh chess baord
    return Board()

def list_moves(board, square):
    # return pseudo-legal moves
    r, c = square_to_index(square)
    return board.pseudo_moves_from(r, c)

def best_ai_move(Board, color, depth):
    # return the best move (tu, ple)
    return minimax(Board, color, depth)[1]

def main():
    board = new_game()
    save_moves = []
    if os.path.exists("saved_game.json"):
        while True:
            q = input("Would you like to continue the previous game? y/n: ")
            if q.lower() in ["y", "yes"]:
                game = open("saved_game.json",)
                moves = json.load(game)
                for move in moves:
                    board.move_piece(square_to_index(move[0]), square_to_index(move[1]))
                break
            elif q.lower() in ["n", "no"]:
                os.remove("saved_game.json")
                break
            else:
                continue
    
    print(board)
    while True:
        # user's move
        while True:
            fr, to = user_move("Enter the move (eg. e2e4) or q to quit: ", save_moves)
            x = board.move_piece(square_to_index(fr), square_to_index(to))
            save_moves.append((fr, to))
            state = board_status(x)
            check_stale = stalemate_checkmate(state)

            if check_stale:
                break
            if state == 1:
                print("King in check")
            if state == 0:
                break
        

        if state == "checkmate":
            print(board)
            print("Checkmate!")
            if os.path.exists("saved_game.json"):
                os.remove("saved_game.json")
            break
        elif state == "stalemate":
            print(board)
            print("Stalemate!")
            if os.path.exists("saved_game.json"):
                os.remove("saved_game.json")
            break

        print(board)
        print("-" * 16)
        print("thinkning.......")


        # ai's move       
        while True:
            _, best_move = minimax(board, board.turn, 2)
            st, en = best_move
            x = board.move_piece(square_to_index(st), square_to_index(en))
            save_moves.append((st, en))
            state = board_status(x)
            check_stale = stalemate_checkmate(state)
            if check_stale:
                break
            elif state == 0:
                break
        
        if state == "checkmate":
            print(board)
            print("Checkmate!")
            if os.path.exists("saved_game.json"):
                os.remove("saved_game.json")
            break
        elif state == "stalemate":
            print(board)
            print("Stalemate!")
            if os.path.exists("saved_game.json"):
                os.remove("saved_game.json")
            break
        
            
        print(board)

def user_move(inp, moves):
    while True:
        notation = input(f"{inp}").replace(" ","").lower()
        if nota := re.search(r"^([a-h][1-8])([a-h][1-8])$", notation):
            return (nota.group(1), nota.group(2))
        elif notation == "q":
            if moves:
                with open("saved_game.json", "w") as outfile:
                    json.dump(moves, outfile)
            sys.exit("You quit the game")
        print("Wrong annotation")

def board_status(x):
    match x:
        case 1:
            print("grabbing an empty square")
        case 2:
            print("not this color's move")
        case False:
            print("invalid move")
        case 3:
            return 1
        case 4:
            return "checkmate"
        case 5:
            return "stalemate"
        case _:
            return 0

def stalemate_checkmate(state):
    if state == "checkmate":
        return True
    elif state == "stalemate":
        return True
    return False

if __name__ == "__main__":
    main()