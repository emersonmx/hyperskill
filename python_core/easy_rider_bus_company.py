import re
from collections import defaultdict
from collections.abc import Container
import json


def input_data():
    data = input()
    return json.loads(data)


# def input_data():
#    with open("input") as f:
#        return json.load(f)


def required(v):
    if is_str(v):
        return v != ""
    return v is not None


def is_int(v):
    return isinstance(v, int)


def is_str(v):
    return isinstance(v, str)


def is_time(v):
    if not is_str(v):
        return False

    return bool(re.match(r"^[0-2]\d:[0-5]\d$", v))


def contains(values):
    def check(v):
        return isinstance(values, Container) and v in values

    return check


def pattern(regex):
    def check(v):
        return re.match(regex, v)

    return check


BUS_SCHEMA = {
    "bus_id": [is_int, required],
    "stop_id": [is_int, required],
    "stop_name": [
        pattern(r"^([A-Z][a-z]+ ?)+(Road|Avenue|Boulevard|Street)$"),
        required,
    ],
    "next_stop": [is_int, required],
    "stop_type": [contains(["S", "O", "F", ""])],
    "a_time": [is_time, required],
}


def validate(row, schema, fields=None):
    result = {}
    for field, checks in schema.items():
        if fields and field in fields:
            value = row[field]
            valid = all([check_func(value) for check_func in checks])
            result[field] = 0 if valid else 1
    return result


def main():
    data = input_data()

    # fields = ["stop_name", "stop_type", "a_time"]
    # errors_per_field = defaultdict(int)
    # total_errors = 0
    # for row in data:
    #    for f, e in validate(row, BUS_SCHEMA, fields).items():
    #        errors_per_field[f] += e
    #        total_errors += e

    # print(f"Format validation: {total_errors} errors")
    # for k, v in errors_per_field.items():
    #    print(f"{k}: {v}")
    lines = defaultdict(int)
    for line in data:
        lines[line["bus_id"]] += 1

    print("Line names and number of stops:")
    for bid, slen in lines.items():
        print(f"bus_id: {bid}, stops: {slen}")

    return 0


if __name__ == "__main__":
    main()
