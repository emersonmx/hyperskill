board = []


def make_board(data):
    return list(list(data[i : i + 3]) for i in [0, 3, 6])


def input_move():
    while True:
        move = input()
        try:
            i, j = map(int, move.split(" "))
        except ValueError:
            print("You should enter numbers!")
            continue

        if (i < 1 or i > 3) or (j < 1 or j > 3):
            print("Coordinates should be from 1 to 3!")
            continue

        i, j = i - 1, j - 1
        if board[i][j] == "_":
            return i, j
        else:
            print("This cell is occupied! Choose another one!")


def show_board():
    print("---------")
    for row in board:
        print("| " + " ".join(row) + " |")
    print("---------")


def is_player_won(player):
    global board
    columns = list(zip(*board))
    diagonals = list(zip(*[[board[i][i], board[i][2 - i]] for i in range(3)]))
    cell_checks = board + columns + diagonals
    checks = [a == b == c for a, b, c in cell_checks if player == a]
    if any(checks):
        return True
    return False


def has_empty_cell():
    global board
    return "_" in sum(board, [])


def is_impossible():
    if is_player_won("X") and is_player_won("O"):
        return True
    xc = sum([1 if c == "X" else 0 for c in sum(board, [])])
    oc = sum([1 if c == "O" else 0 for c in sum(board, [])])
    return abs(xc - oc) > 1


def main():
    global board

    board = make_board("_________")

    player = "X"
    show_board()
    while True:
        i, j = input_move()
        board[i][j] = player
        player = "O" if player == "X" else "X"

        show_board()
        if is_impossible():
            print("Impossible")
            break
        elif is_player_won("X"):
            print("X wins")
            break
        elif is_player_won("O"):
            print("O wins")
            break
        elif has_empty_cell():
            continue
        else:
            print("Draw")
            break


if __name__ == "__main__":
    main()
