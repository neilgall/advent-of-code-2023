from dataclasses import dataclass
from functools import reduce
from parsy import decimal_digit, seq, string, whitespace
import operator


@dataclass
class Race:
    time: int
    distance: int

    def ways_to_win(self) -> int:
        return sum(1 for hold in range(1, self.time) if self.wins_if_hold_for(hold))

    def wins_if_hold_for(self, hold: int) -> bool:
        travelled = (self.time - hold) * hold
        return travelled > self.distance


def parse_input(input: str) -> list[Race]:
    integer = decimal_digit.at_least(1).map(lambda ds: int("".join(ds)))
    integer_list = integer.sep_by(whitespace)
    times = string("Time:") >> whitespace >> integer_list
    distances = string("Distance:") >> whitespace >> integer_list
    document = seq(times << whitespace, distances)
    [times, distances] = document.parse(input.strip())
    return [Race(t, d) for t, d in zip(times, distances)]


def part1(input: str) -> int:
    races = parse_input(input)
    return reduce(operator.mul, (race.ways_to_win() for race in races))


def part2(input: str) -> int:
    return 0
