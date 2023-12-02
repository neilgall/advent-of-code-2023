from typing import Iterable

Input = list[int]


def parse_line(input: str) -> Input:
    return [int(c) for c in input if c.isdigit()]


def calibration_value(input: Input) -> int:
    return input[0] * 10 + input[-1]


def part1(input: Iterable[Input]) -> int:
    return sum(calibration_value(parse_line(i)) for i in input)


if __name__ == "__main__":
    with open("input.txt", "rt") as f:
        input = f.readlines()

    print(f"Part 1: {part1(input)}")