from functools import reduce
from parsy import any_char, digit, peek, string
from typing import Callable, Iterable

Input = list[int]


def parse_line_part1(input: str) -> Input:
    return [int(c) for c in input if c.isdigit()]


def parse_line_part2(input: str) -> Input:
    words = [
        (string(w[:-1]) >> peek(string(w[-1]))).result(v)
        for w, v in {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }.items()
    ]
    word_parser = reduce(lambda p1, p2: p1 | p2, words)
    parser = (digit.map(int) | word_parser | any_char.result(None)).many()

    return [p for p in parser.parse(input) if p]


def calibration_value(input: Input) -> int:
    return input[0] * 10 + input[-1]


def calculate(input: Iterable[Input], parse: Callable[[str], Input]) -> int:
    return sum(calibration_value(parse(i)) for i in input)


if __name__ == "__main__":
    with open("day1/input.txt", "rt") as f:
        input = [l.strip() for l in f.readlines()]

    print(f"Part 1: {calculate(input, parse_line_part1)}")
    print(f"Part 2: {calculate(input, parse_line_part2)}")
