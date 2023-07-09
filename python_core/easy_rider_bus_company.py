from collections import defaultdict
import re
from collections.abc import Container
import json


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


BUS_LINE_SCHEMA = {
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


def input_bus_lines():
    data = input()
    return json.loads(data)


def _input_bus_lines():
    with open("input") as f:
        return json.load(f)


def show_checking_the_data_type(bus_lines):
    errors_per_field = defaultdict(int)
    total_errors = 0
    for row in bus_lines:
        for f, e in validate(row, BUS_LINE_SCHEMA).items():
            errors_per_field[f] += e
            total_errors += e

    print(f"Type and required field validation: {total_errors} errors")
    for k, v in errors_per_field.items():
        print(f"{k}: {v}")


def show_correct_syntax(bus_lines):
    fields = ["stop_name", "stop_type", "a_time"]
    errors_per_field = defaultdict(int)
    total_errors = 0
    for row in bus_lines:
        for f, e in validate(row, BUS_LINE_SCHEMA, fields).items():
            errors_per_field[f] += e
            total_errors += e

    print(f"Format validation: {total_errors} errors")
    for k, v in errors_per_field.items():
        print(f"{k}: {v}")


def show_bus_line_info(bus_lines):
    lines = defaultdict(int)
    for line in bus_lines:
        lines[line["bus_id"]] += 1

    print("Line names and number of stops:")
    for bid, slen in lines.items():
        print(f"bus_id: {bid}, stops: {slen}")


def show_special_stops(bus_lines):
    bus_stops = defaultdict(lambda: defaultdict(int))
    stop_counter = defaultdict(int)
    stop_index = {}

    for bus in bus_lines:
        bus_id = bus["bus_id"]
        stop_id = bus["stop_id"]
        stop_name = bus["stop_name"]
        next_stop = bus["next_stop"]
        stop_type = bus["stop_type"]
        bus_stops[bus_id][stop_type] += 1
        stop_counter[next_stop] += 1
        stop_index[stop_id] = stop_name

    for line, stops in bus_stops.items():
        if stops["S"] == stops["F"] == 1:
            continue
        print(f"There is no start or end stop for the line: {line}.")
        return

    start_stops = {bus["stop_name"] for bus in bus_lines if bus["stop_type"] == "S"}
    finish_stops = {bus["stop_name"] for bus in bus_lines if bus["stop_type"] == "F"}
    transfer_stops = {
        stop_index[k] for k, v in stop_counter.items() if k != 0 and v > 1
    }
    print("Start stops:", len(start_stops), sorted(start_stops))
    print("Transfer stops:", len(transfer_stops), sorted(transfer_stops))
    print("Finish stops:", len(finish_stops), sorted(finish_stops))


def show_unlost_in_time(bus_lines):
    bus_index = defaultdict(dict)
    for line in bus_lines:
        bus_id = line["bus_id"]
        stop_id = line["stop_id"]
        bus_index[bus_id][stop_id] = line

    print("Arrival time test:")
    invalid_time = set()
    for line in bus_lines:
        next_stop = line["next_stop"]
        if next_stop == 0:
            continue

        bus_id = line["bus_id"]
        if bus_id in invalid_time:
            continue
        next_line = bus_index[bus_id][next_stop]
        a_time = line["a_time"]
        next_a_time = next_line["a_time"]
        next_stop_name = next_line["stop_name"]
        if next_a_time < a_time:
            print(f"bus_id line {bus_id}: wrong time on station {next_stop_name}")
            invalid_time.add(bus_id)

    if not invalid_time:
        print("OK")


def show_on_demand(bus_lines):
    stop_counter = defaultdict(int)
    stop_index = {}
    for bus in bus_lines:
        stop_id = bus["stop_id"]
        stop_name = bus["stop_name"]
        next_stop = bus["next_stop"]
        stop_index[stop_id] = stop_name
        stop_counter[next_stop] += 1

    transfer_stops = {k for k, v in stop_counter.items() if k != 0 and v > 1}
    wrong_stops = set()
    for bus in bus_lines:
        stop_id = bus["stop_id"]
        stop_type = bus["stop_type"]
        if stop_type != "O":
            continue
        if stop_id in transfer_stops:
            wrong_stops.add(stop_index[stop_id])

    print("On demand stops test:")
    if wrong_stops:
        print("Wrong stop type:", sorted(wrong_stops))
    else:
        print("OK")


def main():
    bus_lines = input_bus_lines()
    # show_checking_the_data_type(bus_lines)
    # show_correct_syntax(bus_lines)
    # show_bus_line_info(bus_lines)
    # show_special_stops(bus_lines)
    # show_unlost_in_time(bus_lines)
    show_on_demand(bus_lines)


if __name__ == "__main__":
    main()
