import sys
import ast
import re
from pathlib import Path
from collections import defaultdict
from functools import cache


def check_s001(lines, errors):
    for number, line in enumerate(lines, start=1):
        is_too_long = len(line) > 79
        if is_too_long:
            errors[number].append("S001 Too long")


def check_s002(lines, errors):
    for number, line in enumerate(lines, start=1):
        spaces_match = re.match(r"^( *)", line)
        if not spaces_match:
            continue
        if len(spaces_match.group(1)) % 4 != 0:
            errors[number].append("S002 Indentation is not a multiple of four")


def check_s003(lines, errors):
    for number, line in enumerate(lines, start=1):
        has_semicolon = re.search(r";", line)
        if not has_semicolon:
            continue
        t = re.sub("#.*", "", line).strip()
        if t.endswith(";"):
            errors[number].append("S003 Unnecessary semicolon")


def check_s004(lines, errors):
    for number, line in enumerate(lines, start=1):
        spaces_match = re.search(r".+?( *)#", line)
        if not spaces_match:
            continue
        if len(spaces_match.group(1)) < 2:
            errors[number].append(
                "S004 At least two spaces required before inline comments"
            )


def check_s005(lines, errors):
    for number, line in enumerate(lines, start=1):
        if re.search(r"#\s*todo", line, re.IGNORECASE):
            errors[number].append("S005 TODO found")


def check_s006(lines, errors):
    for line_index in range(len(lines)):
        number = line_index + 1
        line = lines[line_index].strip()
        if line == "":
            continue

        count = 0
        for line in lines[line_index - 3 : line_index]:
            count += 1 if line.strip() == "" else 0
        if count > 2:
            errors[number].append(
                "S006 More than two blank lines used before this line"
            )


def check_s007(lines, errors):
    for number, line in enumerate(lines, start=1):
        match = re.match(r"^ *(def|class) {2,}", line)
        if not match:
            continue
        name = match.groups()
        errors[number].append(f"S007 Too many spaces after '{name}'")


def check_s008(lines, errors):
    for number, line in enumerate(lines, start=1):
        match = re.match(r"^class (\w+):$", line)
        if not match:
            continue
        name = match.group(1)
        if not re.match(r"^[A-Z][a-zA-Z]+", name):
            errors[number].append(f"S008  Class name '{name}' should use CamelCase")


def check_s009(lines, errors):
    for number, line in enumerate(lines, start=1):
        match = re.match(r"^ *def (\w+)\(.*\):$", line)
        if not match:
            continue
        name = match.group(1)
        if not re.match(r"[a-z_][a-z0-9_]", name):
            errors[number].append(f"S009 Function name '{name}' should use snake_case")


@cache
def make_source_ast(lines):
    try:
        return ast.parse("\n".join(lines))
    except (SyntaxError, ValueError):
        return None


def check_s010(lines, errors):
    source_ast = make_source_ast(tuple(lines))
    pattern = re.compile(r"^[a-z_]+$")
    for node in ast.walk(source_ast):
        if not isinstance(node, ast.FunctionDef):
            continue
        for number, name in map(lambda a: (a.end_lineno, a.arg), node.args.args):
            if pattern.match(name):
                continue
            errors[number].append(f"S010 Argument name '{name}' should be snake_case")


def check_s011(lines, errors):
    source_ast = make_source_ast(tuple(lines))
    pattern = re.compile(r"^[a-z_]+$")
    for node in ast.walk(source_ast):
        if not isinstance(node, ast.FunctionDef):
            continue
        for function_node in node.body:
            if not isinstance(function_node, ast.Assign):
                continue
            for target in function_node.targets:
                name_node = target
                if isinstance(target, ast.Attribute):
                    name_node = target.value
                number = name_node.end_lineno
                name = name_node.id
                if pattern.match(name):
                    continue
                errors[number].append(
                    f"S011 Variable '{name}' in function should be snake_case"
                )


def check_s012(lines, errors):
    source_ast = make_source_ast(tuple(lines))
    for node in ast.walk(source_ast):
        if not isinstance(node, ast.FunctionDef):
            continue
        for d in node.args.defaults:
            if not isinstance(d, ast.List):
                continue
            errors[d.end_lineno].append("S012 Default argument value is mutable")


def get_rules():
    names = globals()
    for name in names:
        if re.match(r"^check_s\d{3}$", name):
            yield names[name]


def get_lines(filepath):
    with filepath.open() as f:
        data = f.read()
    return data.splitlines()


def get_errors(lines):
    errors = defaultdict(list)
    for check_rule in get_rules():
        check_rule(lines, errors)
    return errors


def show_errors(filepath, errors):
    sorted_errors = sorted(errors.items(), key=lambda e: e[0])
    for line_number, messages in sorted_errors:
        for message in messages:
            print(f"{filepath}: Line {line_number}: {message}")


def check_rules(filepath):
    lines = get_lines(filepath)
    errors = get_errors(lines)
    show_errors(filepath, errors)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory-or-file>")
        return

    path = Path(sys.argv[1])
    if path.is_dir():
        for filepath in path.glob("**/*.py"):
            check_rules(filepath)
    else:
        check_rules(path)


if __name__ == "__main__":
    main()
