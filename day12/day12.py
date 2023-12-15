from dataclasses import dataclass
from enum import Enum
from re import compile, Pattern


@dataclass
class SpringRow:
    springs: str
    groups: list[int]

    @classmethod
    def from_string(cls, input: str) -> "SpringRow":
        [springs, groups] = input.split()
        springs = springs.replace('\.', "O").replace(r'\?', "U").replace(r'#', "D")
        return SpringRow(springs, [int(g) for g in groups.split(",")])

    def groups_as_regex(self) -> Pattern:
        return compile(
            "\\.*?" + "[\\.\\?]".join(f"[#\\?]{g}" for g in self.groups)
        )

    def matches(self) -> int:
        regex = self.groups_as_regex()
        print(regex)
        return len(regex.findall(self.springs))


def parse_input(input: str) -> list[SpringRow]:
    return [SpringRow.from_string(s) for s in input.strip().split("\n")]
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
