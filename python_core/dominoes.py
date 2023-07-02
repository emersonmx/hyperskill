import random


context = {}


def make_context():
    dominoes = [[i, j] for i in range(7) for j in range(i, 7)]
    stock_pieces = []
    computer_pieces = []
    player_pieces = []
    snake = []
    status = ""
    while status == "":
        random.shuffle(dominoes)
        stock_pieces = dominoes[:14]
        computer_pieces = dominoes[14:21]
        player_pieces = dominoes[21:]
        for i in range(6, 0, -1):
            piece = [i, i]
            if piece in computer_pieces:
                status = "player"
                computer_pieces.remove(piece)
                snake.append(piece)
                break
            if piece in player_pieces:
                status = "computer"
                player_pieces.remove(piece)
                snake.append(piece)
                break
    return {
        "stock_pieces": stock_pieces,
        "computer_pieces": computer_pieces,
        "player_pieces": player_pieces,
        "snake": snake,
        "status": status,
        "winner": "",
    }


def process_input():
    global context

    if context["status"] == "player":
        player, move = input_player_move()
    else:
        input()
        player, move = input_computer_move()

    if move == 0:
        if context["stock_pieces"]:
            piece = random.choice(context["stock_pieces"])
            context["stock_pieces"].remove(piece)
            context[player].append(piece)
    else:
        index = abs(move)
        piece = context[player][index - 1]
        context[player].remove(piece)
        snake = context["snake"]
        if move < 0:
            piece = piece if piece[1] == snake[0][0] else piece[::-1]
            context["snake"].insert(0, piece)
        else:
            piece = piece if piece[0] == snake[-1][1] else piece[::-1]
            context["snake"].append(piece)


def valid_move(player, move):
    global context

    if move == 0:
        return True

    pieces = context[player]
    index = abs(move)
    piece = pieces[index - 1]
    snake = context["snake"]
    left, right = snake[0][0], snake[-1][1]
    if left in piece and move < 0:
        return True
    if right in piece and move > 0:
        return True
    return False


def input_player_move():
    global context
    max_move = abs(len(context["player_pieces"]))
    min_move = -max_move
    while True:
        try:
            move = int(input())
            if move < min_move or move > max_move:
                raise ValueError("Invalid range")
        except ValueError:
            print("Invalid input. Please try again.")
            continue

        if valid_move("player_pieces", move):
            return "player_pieces", move
        else:
            print("Illegal move. Please try again.")


def input_computer_move():
    global context

    pieces = context["computer_pieces"]
    snake = context["snake"]
    move_counter = {}
    for i in range(7):
        move_counter[i] = sum([p.count(i) for p in pieces])
        move_counter[i] += sum([p.count(i) for p in snake])

    scores = []
    for piece in pieces:
        left, right = piece
        score = move_counter[left] + move_counter[right]
        scores.append([piece, score])
    scores.sort(key=lambda e: e[1], reverse=True)

    for piece, _ in scores:
        move = pieces.index(piece) + 1
        if valid_move("computer_pieces", -move):
            return "computer_pieces", -move
        if valid_move("computer_pieces", move):
            return "computer_pieces", move

    return "computer_pieces", 0


def show_header():
    global context

    stock_pieces = context["stock_pieces"]
    computer_pieces = context["computer_pieces"]
    print("=" * 70)
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer_pieces)}")


def show_player_pieces():
    global context

    player_pieces = context["player_pieces"]
    print("Your pieces:")
    for i, piece in enumerate(player_pieces, start=1):
        print(f"{i}: {piece}")


def show_status():
    global context

    print()
    if context["status"] == "player":
        print("Status: It's your turn to make a move. Enter your command.")
    else:
        print("Status: Computer is about to make a move. Press Enter to continue...")


def show_snake():
    global context

    snake = [str(p) for p in context["snake"]]
    formatted_snake = "".join(snake)
    if len(snake) > 6:
        begin = snake[:3]
        end = snake[-3:]
        formatted_snake = "".join(begin + ["..."] + end)

    print()
    print(formatted_snake)
    print()


def has_winner():
    global context

    player_pieces = len(context["player_pieces"])
    computer_pieces = len(context["computer_pieces"])

    player_has_moves = False
    for p in context["player_pieces"]:
        move = context["player_pieces"].index(p) + 1
        if valid_move("player_pieces", move):
            player_has_moves = True
            break

    computer_has_moves = False
    for p in context["computer_pieces"]:
        move = context["computer_pieces"].index(p) + 1
        if valid_move("computer_pieces", move):
            computer_has_moves = True
            break

    if player_pieces == 0:
        context["winner"] = "player"
        return True
    elif computer_pieces == 0:
        context["winner"] = "computer"
        return True
    elif not player_has_moves and not computer_has_moves:
        context["winner"] = "draw"
        return True
    else:
        return False


def next_player():
    global context

    status = context["status"]
    if status == "computer":
        context["status"] = "player"
    else:
        context["status"] = "computer"


def show_gameover():
    global context

    print()
    winner = context["winner"]
    if winner == "draw":
        print("Status: The game is over. It's a draw!")
    elif winner == "player":
        print("Status: The game is over. You won!")
    elif winner == "computer":
        print("Status: The game is over. The computer won!")


def main():
    global context

    context = make_context()

    while True:
        show_header()
        show_snake()
        show_player_pieces()
        if has_winner():
            show_gameover()
            break
        show_status()
        process_input()
        next_player()


if __name__ == "__main__":
    main()
