from dataclasses import dataclass
from enum import Enum
from parsy import decimal_digit, from_enum, seq, string, whitespace


class Spring(Enum):
    OPERATIONAL = "."
    DAMAGED = "#"
    UNKNOWN = "?"


@dataclass
class SpringRow:
    springs: list[Spring]
    groups: list[int]


def parse_input(input: str) -> list[SpringRow]:
    springs = from_enum(Spring).at_least(1)
    integer = decimal_digit.at_least(1).map(lambda ds: int("".join(ds)))
    groups = integer.sep_by(string(","))
    row = seq(springs << whitespace, groups).combine(SpringRow)
    rows = row.sep_by(string("\n"))
    return rows.parse(input.strip())


def part1(input: str) -> int:
    return 0


def part2(input: str) -> int:
    return 0
