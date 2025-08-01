from termcolor import colored

X = 'X'
O = 'O'


def cell(mark):
    color = 'red' if mark == X else 'green'
    return colored(mark, color)


def print_board(board):
    size = len(board)
    line = '+'.join(['---'] * size)
    print(line)
    for row in board:
        print(' | '.join(cell(mark) for mark in row))
        print(line)


def check_winner(board, win_length=3):
    size = len(board)

    def check_line(line):
        count = 1
        for i in range(1, len(line)):
            if line[i] == line[i - 1] and line[i] != ' ':
                count += 1
                if count == win_length:
                    return True
            else:
                count = 1
        return False

    # Rows
    for row in board:
        if check_line(row):
            return True

    # Columns
    for col in range(size):
        column = [board[row][col] for row in range(size)]
        for row in range(size):
            print(f"column: {row, col}")
        if check_line(column):
            return True

    # Diagonals (main and anti diagonals)
    print(size, win_length)
    for r in range(size - win_length + 1):
        for c in range(size - win_length + 1):
            # Main diagonal
            print(r, c, size - win_length + 1)
            diagonal = [board[r + i][c + i] for i in range(win_length)]
            for i in range(win_length):
                print(f"diagonal: {r + i, c + i}")
            if check_line(diagonal):
                return True

            # Anti diagonal
            anti_diagonal = [board[r + i][c + win_length - 1 - i]
                             for i in range(win_length)]
            for i in range(win_length):
                print(f"anti_diagonal: {r + i, c + win_length - 1 - i}")
            if check_line(anti_diagonal):
                return True

    return False


def is_full(board):
    return all(cell != ' ' for row in board for cell in row)


def get_position(prompt, size):
    while True:
        try:
            position = int(input(prompt))
            if position < 0 or position >= size:
                raise ValueError
            return position
        except ValueError:
            print(
                f'Invalid input! Please enter a number between 0 and {size - 1}.')


def get_move(current_player, board):
    size = len(board)
    print(f"Player {current_player}'s turn")
    while True:
        row = get_position('Enter row: ', size)
        column = get_position('Enter column: ', size)

        if board[row][column] == ' ':
            board[row][column] = current_player
            break

        print('This spot is already taken')


def create_board(size):
    return [[' ' for _ in range(size)] for _ in range(size)]


def main():
    size = 0
    while size < 3:
        try:
            size = int(input('Enter board size (minimum 3): '))
            if size < 3:
                print('Board size must be at least 3.')
        except ValueError:
            print('Invalid number!')

    board = create_board(size)
    win_length = 3 if size <= 3 else min(size, 4)

    print_board(board)

    current_player = X

    while True:
        get_move(current_player, board)

        print_board(board)

        if check_winner(board, win_length):
            print(f'Player {current_player} wins!')
            break

        if is_full(board):
            print('The board is full! It\'s a draw.')
            break

        current_player = O if current_player == X else X


if __name__ == '__main__':
    main()
