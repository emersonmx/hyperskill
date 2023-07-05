context = {}


def input_size():
    while True:
        try:
            size = input("Enter your board dimensions: ")
            x, y = [int(v) for v in size.split(" ")]

            if x < 1 or y < 1:
                raise ValueError("Invalid range")
            return x, y
        except ValueError:
            print("Invalid dimensions!")


def make_board(width, height, fill):
    return [[fill for _ in range(width)] for _ in range(height)]


def move_in_range(x, y, width, height):
    return (0 <= x < width) and (0 <= y < height)


def empty_cell(board, x, y):
    return board[y][x] == "_"


def valid_move(x, y):
    global context
    width, height = context["size"]
    if not move_in_range(x, y, width, height):
        return False
    return empty_cell(context["board"], x, y)


def input_position_with_prompt(prompt):
    while True:
        try:
            position = input(prompt)
            x, y = [int(v) - 1 for v in position.split(" ")]
            if not valid_move(x, y):
                raise ValueError("Invalid range")
            return x, y
        except ValueError:
            print("Invalid move!", end=" ")


def get_moves_from(x, y, width, height):
    offsets = [
        [-1, -2],
        [1, -2],
        [-2, -1],
        [2, -1],
        [-2, 1],
        [2, 1],
        [-1, 2],
        [1, 2],
    ]
    for ox, oy in offsets:
        nx = x + ox
        ny = y + oy
        if move_in_range(nx, ny, width, height):
            yield nx, ny


def get_valid_moves(x, y):
    global context
    width, height = context["size"]
    result = []
    for nx, ny in get_moves_from(x, y, width, height):
        if valid_move(nx, ny):
            result.append([nx, ny])

    return result


def cell_size():
    global context
    w, h = context["size"]
    return len(str(w * h))


def mark(board, x, y, cell):
    board[y][x] = cell[-cell_size() :]


def make_preview_board():
    global context
    sx, sy = context["select_position"]
    board = [r.copy() for r in context["board"].copy()]
    for x, y in get_valid_moves(sx, sy):
        count = len(get_valid_moves(x, y)) - 1
        mark(board, x, y, str(count))

    if valid_move(sx, sy):
        mark(board, sx, sy, "x")
    return board


def left_padding():
    global context
    width, _ = context["size"]
    return len(str(width))


def show_ruler():
    global context
    width, _ = context["size"]
    count = width * (cell_size() + 1) + 3
    left_spaces = " " * left_padding()
    bar = "-" * count
    print(left_spaces + bar)


def format_cell(cell):
    padding_size = cell_size()
    placeholder = "_" if cell == "_" else " "
    template = placeholder * padding_size
    return (template + cell)[-padding_size:]


def show_board(board):
    print("Here are the possible moves:")
    show_ruler()

    row_length = len(board)
    reverse_rows = board[::-1]
    for i in range(row_length):
        py = row_length - i
        row = [format_cell(c) for c in reverse_rows[i]]
        left_spaces = " " * left_padding()
        row_number = (left_spaces + str(py))[-left_padding() :]
        print(" ".join([f"{row_number}|"] + row + ["|"]))

    show_ruler()
    left_spaces = " " * (left_padding() + 1)
    row = [format_cell(str(i + 1)) for i in range(len(board[0]))]
    print(" ".join([left_spaces] + row))


def update_board(x, y):
    global context
    context["select_position"] = [x, y]
    preview_board = make_preview_board()
    show_board(preview_board)
    mark(context["board"], x, y, "*")
    context["visited"] += 1


def setup():
    global context
    context = {
        "size": [0, 0],
        "board": [],
        "select_position": [0, 0],
        "visited": 0,
    }

    width, height = input_size()
    context["size"] = width, height
    context["board"] = make_board(width, height, "_")
    x, y = input_position_with_prompt("Enter the knight's starting position: ")
    context["select_position"] = [x, y]
    update_board(x, y)


def is_running():
    global context
    x, y = context["select_position"]
    moves = len(get_valid_moves(x, y))
    return moves > 0


def input_position():
    global context
    while True:
        try:
            x, y = input_position_with_prompt("Enter your next move: ")
            sx, sy = context["select_position"]
            if [x, y] in get_valid_moves(sx, sy):
                return x, y
            else:
                raise ValueError("Invalid move")
        except ValueError:
            print("Invalid move!", end=" ")


def update():
    x, y = input_position()
    update_board(x, y)


def show_game_over():
    global context
    board = context["board"]
    visited = context["visited"]
    complete = all([c == "*" for c in sum(board, [])])
    if complete:
        print("What a great tour! Congratulations!")
    else:
        print("No more possible moves!")
        print(f"Your knight visited {visited} squares!")


def main():
    setup()
    while is_running():
        update()
    show_game_over()


if __name__ == "__main__":
    main()
