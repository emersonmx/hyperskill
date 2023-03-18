def cleaned_input():
    return input().strip()


def main():
    rows = 8
    columns = 8
    board = []
    for _ in range(rows):
        board.append(["_"] * columns)

    print("Enter the knight's starting position:")
    try:
        x, y = [int(v) - 1 for v in cleaned_input().split()]
    except ValueError:
        print("Invalid dimensions!")
        return

    if x < 0 or x > columns or y < 0 or y > rows:
        print("Invalid dimensions!")
        return

    board[y][x] = "X"

    print(f" {'-' * 19}")
    for n, line in reversed(list(enumerate(board, start=1))):
        formatted_line = " ".join(line)
        print(f"{n}| {formatted_line} |")
    print(f" {'-' * 19}")
    numbers = [str(i + 1) for i in range(len(board))]
    print(f"   {' '.join(numbers)}")


if __name__ == "__main__":
    main()
