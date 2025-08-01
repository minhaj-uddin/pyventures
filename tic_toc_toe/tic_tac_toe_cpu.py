import random
from termcolor import colored

X = 'X'
O = 'O'

board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]


def cell(mark):
    color = 'red' if mark == X else 'green'
    return colored(mark, color)


def print_board(board):
    line = '---+---+---'
    print(line)
    for row in board:
        print(f' {cell(row[0])} | {cell(row[1])} | {cell(row[2])}')
        print(line)


def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return True

    # Check columns
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] != ' ':
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ' or \
       board[0][2] == board[1][1] == board[2][0] != ' ':
        return True

    return False


def is_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True


def get_position(prompt):
    while True:
        try:
            position = int(input(prompt))
            if position < 0 or position > 2:
                raise ValueError
            return position
        except ValueError:
            print('Invalid input!')


def player_move():
    print(f"Your move (X)")
    while True:
        row = get_position('Enter row (0-2): ')
        column = get_position('Enter column (0-2): ')

        if board[row][column] == ' ':
            board[row][column] = X
            break
        print('This spot is already taken')


def computer_move():
    print("Computer's move (O)")
    # Simple strategy: pick a random empty cell
    empty_cells = [(r, c) for r in range(3)
                   for c in range(3) if board[r][c] == ' ']
    if empty_cells:
        print(empty_cells)
        row, col = random.choice(empty_cells)
        board[row][col] = O


def main():
    print_board(board)

    while True:
        # Player move
        player_move()
        print_board(board)

        if check_winner(board):
            print('You win!')
            break
        if is_full(board):
            print('Draw!')
            break

        # Computer move
        computer_move()
        print_board(board)

        if check_winner(board):
            print('Computer wins!')
            break
        if is_full(board):
            print('Draw!')
            break


if __name__ == '__main__':
    main()
