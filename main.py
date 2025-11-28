import curses
import random

# size of the board
SIZE = 4

def create_board():
    # make a 4x4 grid full of 0
    board = []
    for i in range(SIZE):
        row = [0] * SIZE
        board.append(row)
    return board

def add_new_number(board):
    # find empty spaces
    empty = []
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                empty.append((r, c))
    if empty:
        r, c = random.choice(empty)
        # 90% chance 2, 10% chance 4
        board[r][c] = 4 if random.random() < 0.1 else 2

def slide_left(row):
    # remove zeros
    new_row = [num for num in row if num != 0]

    # merge numbers
    i = 0
    while i < len(new_row) - 1:
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            new_row.pop(i + 1)
            new_row.append(0)
        i += 1

    # add zeros to the end to keep size 4
    while len(new_row) < SIZE:
        new_row.append(0)

    return new_row

def move_left(board):
    changed = False
    for r in range(SIZE):
        old_row = list(board[r])
        board[r] = slide_left(board[r])
        if board[r] != old_row:
            changed = True
    return changed

def move_right(board):
    changed = False
    for r in range(SIZE):
        old_row = list(board[r])
        reversed_row = list(reversed(board[r]))
        new_row = slide_left(reversed_row)
        new_row = list(reversed(new_row))
        board[r] = new_row
        if new_row != old_row:
            changed = True
    return changed

def move_up(board):
    changed = False
    for c in range(SIZE):
        col = [board[r][c] for r in range(SIZE)]
        old_col = list(col)
        new_col = slide_left(col)
        for r in range(SIZE):
            board[r][c] = new_col[r]
        if new_col != old_col:
            changed = True
    return changed

def move_down(board):
    changed = False
    for c in range(SIZE):
        col = [board[r][c] for r in range(SIZE)]
        old_col = list(col)
        col.reverse()
        new_col = slide_left(col)
        new_col.reverse()
        for r in range(SIZE):
            board[r][c] = new_col[r]
        if new_col != old_col:
            changed = True
    return changed
def draw_board(stdscr, board):
    stdscr.clear()
    stdscr.addstr(0, 0, "2048 Game (Arrows to move, Q to quit)")

    for r in range(SIZE):
        for c in range(SIZE):
            val = str(board[r][c]) if board[r][c] != 0 else "."
            stdscr.addstr(r + 2, c * 6, val.center(5))

    stdscr.refresh()

def can_move(board):
    # if there is a zero, player can move
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return True

    # check horizontal merge possible
    for r in range(SIZE):
        for c in range(SIZE - 1):
            if board[r][c] == board[r][c + 1]:
                return True
 # check vertical merge possible
    for r in range(SIZE - 1):
        for c in range(SIZE):
            if board[r][c] == board[r + 1][c]:
                return True

    return False

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    board = create_board()
    add_new_number(board)
    add_new_number(board)

    while True:
        draw_board(stdscr, board)

        if not can_move(board):
            stdscr.addstr(8, 0, "GAME OVER! Press any key to exit.")
            stdscr.getch()
            break

        key = stdscr.getch()

        moved = False
        if key == curses.KEY_LEFT:
            moved = move_left(board)
        elif key == curses.KEY_RIGHT:
            moved = move_right(board)
        elif key == curses.KEY_UP:
            moved = move_up(board)
        elif key == curses.KEY_DOWN:
            moved = move_down(board)
        elif key == ord('q') or key == ord('Q'):
            break

        if moved:
            add_new_number(board)

curses.wrapper(main)