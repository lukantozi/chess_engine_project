# to assign notations to chessboard squares
def index_to_square(row, col):
    column = chr(ord('a') + col)
    rank = str(8 - row)
    return column + rank

def square_to_index(notation):
    column = ord(notation[0].lower()) - ord('a')
    row = 8 - int(notation[1])
    return (row, column)