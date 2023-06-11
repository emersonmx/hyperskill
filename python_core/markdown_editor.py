FORMATTERS = [
    "plain",
    "bold",
    "italic",
    "header",
    "link",
    "inline-code",
    "ordered-list",
    "unordered-list",
    "new-line",
]
COMMANDS = ["!help", "!done"]

running = True
document = []


def plain_action():
    text = input("Text: ")
    document.append(text)


def bold_action():
    text = input("Text: ")
    document.append(f"**{text}**")


def italic_action():
    text = input("Text: ")
    document.append(f"*{text}*")


def header_action():
    while True:
        try:
            level = int(input("Level: "))
        except ValueError:
            continue

        if 1 <= level <= 6:
            break
        else:
            print("The level should be within the range of 1 to 6")

    text = input("Text: ")
    document.append(f"{'#' * level} {text}\n")


def link_action():
    label = input("Label: ")
    url = input("URL: ")
    document.append(f"[{label}]({url})")


def inline_code_action():
    text = input("Text: ")
    document.append(f"`{text}`")


def _get_row_list():
    while True:
        try:
            rows = int(input("Number of rows: "))
        except ValueError:
            continue

        if rows > 0:
            break
        else:
            print("The number of rows should be greater than zero")

    result = []
    for i in range(1, rows + 1):
        row = input(f"Row #{i}: ")
        result.append(f"{row}")
    return result


def ordered_list_action():
    for i, row in enumerate(_get_row_list(), 1):
        document.append(f"{i}. {row}\n")


def unordered_list_action():
    for row in _get_row_list():
        document.append(f"* {row}\n")


def new_line_action():
    document.append("\n")


def help_action():
    print("Available formatters:", " ".join(FORMATTERS))
    print("Special commands:", " ".join(COMMANDS))


def done_action():
    global running
    running = False
    with open("output.md", "w+") as f:
        f.write("".join(document))


def show_document():
    print("".join(document))


def main():
    while running:
        action = input("Choose a formatter: ")
        if action in FORMATTERS:
            action_name = action.replace("-", "_") + "_action"
            f = globals().get(action_name)
            f()
            show_document()
        elif action in COMMANDS:
            action_name = action[1:] + "_action"
            f = globals().get(action_name)
            f()
        else:
            print("Unknown formatting type or command")


if __name__ == "__main__":
    main()
