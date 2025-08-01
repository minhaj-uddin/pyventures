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


def check_winner(board, player):
    # Rows, columns and diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_full(board):
    return all(cell != ' ' for row in board for cell in row)


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
    print("Your move (X)")
    while True:
        row = get_position('Enter row (0-2): ')
        column = get_position('Enter column (0-2): ')

        if board[row][column] == ' ':
            board[row][column] = X
            break
        print('This spot is already taken')


def computer_move():
    print("Computer move (O)")
    best_score = -float('inf')
    move = None

    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                board[r][c] = O
                score = minimax(board, 0, False)
                board[r][c] = ' '
                if score > best_score:
                    best_score = score
                    move = (r, c)
                    print(f"best_score: {best_score}, score: {score}")
                    print(move)
                    print("-" * 30)

    if move:
        board[move[0]][move[1]] = O


def minimax(board, depth, is_maximizing):
    if check_winner(board, O):
        return 1
    if check_winner(board, X):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':
                    board[r][c] = O
                    score = minimax(board, depth + 1, False)
                    board[r][c] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':
                    board[r][c] = X
                    score = minimax(board, depth + 1, True)
                    board[r][c] = ' '
                    best_score = min(score, best_score)
        return best_score


def main():
    print_board(board)

    while True:
        player_move()
        print_board(board)
        if check_winner(board, X):
            print('You win!')
            break
        if is_full(board):
            print('Draw!')
            break

        computer_move()
        print_board(board)
        if check_winner(board, O):
            print('Computer wins!')
            break
        if is_full(board):
            print('Draw!')
            break


if __name__ == '__main__':
    main()
