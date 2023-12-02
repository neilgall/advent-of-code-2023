from dataclasses import dataclass
from enum import Enum
from parsy import decimal_digit, from_enum, seq, string, whitespace
from typing import Iterable


class Colour(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

Turn = dict[Colour, int]


DEFAULT_LOAD = {
    Colour.RED: 12,
    Colour.GREEN: 13,
    Colour.BLUE: 14,
}


@dataclass
class Game:
    id: int
    turns: list(Turn)

    def is_possible(self, load: Turn):
        def turn_is_possible(t: Turn) -> bool:
            return all(t[c] <= load[c] for c in t.keys())

        return all(turn_is_possible(t) for t in self.turns)


    def smallest_load_power(self) -> int:
        red, blue, green = 0, 0, 0
        for turn in self.turns:
            red = max(red, turn.get(Colour.RED, 0))
            blue = max(blue, turn.get(Colour.BLUE, 0))
            green = max(green, turn.get(Colour.GREEN, 0))
        
        return red * blue * green
            

def parse_game(input: str) -> Game:
    integer = decimal_digit.at_least(1).map(lambda ds: int("".join(ds)))
    cubes = seq(integer << whitespace, from_enum(Colour)).map(lambda v: (v[1], v[0]))
    turn = cubes.sep_by(string(",") << whitespace).map(dict)
    game_id = (string("Game") >> whitespace) >> integer << (string(":") << whitespace)
    game = seq(game_id, turn.sep_by(string(";") << whitespace)).map(lambda v: Game(v[0], v[1]))
    return game.parse(input)


def part1(input: Iterable[Game]) -> int:
    return sum(game.id for game in input if game.is_possible(DEFAULT_LOAD))


def part2(input: Iterable[Game]) -> int:
    return sum(game.smallest_load_power() for game in input)


if __name__ == "__main__":
    with open("day2/input.txt", "rt") as f:
        input = [parse_game(l.strip()) for l in f.readlines()]

    print(f"Part 1: {part1(input)}")
    print(f"Part 2: {part2(input)}")
