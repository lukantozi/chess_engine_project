# Python Chess

### Description

This is a fully-featured command-line chess game written from scratch in Python.
It supports all standard rules and includes an AI opponent powered by a minimax algorithm with alpha–beta pruning.
I built this to deepen my understanding of object-oriented design, recursion, and algorithmic thinking.

## Key Features

* **Full Chess Rules**
  Piece movement, castling (king- and queen-side), en passant, pawn promotion,
  and check/checkmate/stalemate detection.

* **Board Representation**
  An 8×8 grid of `Square` objects, each tracking piece presence and square color.

* **Piece Classes**
  `Pawn`, `Knight`, `Bishop`, `Rook`, `Queen`, and `King` subclasses
  with movement logic and state flags (`has_moved`, `has_castled`).

* **Game State Management**
  Turn tracking, half-move clock for the fifty-move rule, move counter,
  and JSON-based save/resume via `saved_game.json`.

* **AI Opponent**
  Customizable-depth minimax search with alpha–beta pruning, plus an evaluation that combines:

  1. Material balance (sum of piece values)
  2. King safety (pawn shield, attacked squares, castling status)
  3. Center control (d4, d5, e4, e5)
  4. Mobility (number of legal moves)

## Getting Started
1. Run the game:

   ```bash
   python project.py
   ```

2. Play:

   * Enter moves in algebraic notation, e.g., `e2e4`.
   * Enter `q` to save and quit; resume by confirming on next launch.

## Project Structures

```
project.py     # Main game loop and user interaction  
board.py       # Board and Square classes, core game rules  
pieces.py      # Piece class hierarchy and movement logic  
ai.py          # Minimax implementation and evaluation  
utils.py       # Helper functions (notation conversion)  
```

## Future Improvements

* Iterative deepening & smarter move ordering (killer moves, history heuristics)
* Graphical interface (e.g., Pygame or web front end)
* Enhanced evaluation with positional heuristics, pawn structure, and game phase awareness

---

I’m proud of what I’ve learned building this. Thanks for checking it out!
Feel free to reach out with any questions or suggestions.

*— Luka Mamrikishvili*
