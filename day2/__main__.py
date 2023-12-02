from dataclasses import dataclass
from enum import Enum
from parsy import decimal_digit, from_enum, seq, string, whitespace


class Colour(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


@dataclass
class Game:
    id: int
    turns: dict[Colour, int]


def parse_game(input: str) -> Game:
    integer = decimal_digit.at_least(1).map(lambda ds: int("".join(ds)))
    cubes = seq(integer << whitespace, from_enum(Colour)).map(lambda v: (v[1], v[0]))
    turn = cubes.sep_by(string(",") << whitespace).map(dict)
    game_id = (string("Game") >> whitespace) >> integer << (string(":") << whitespace)
    game = seq(game_id, turn.sep_by(string(";") << whitespace)).map(lambda v: Game(v[0], v[1]))
    return game.parse(input)


if __name__ == "__main__":
    with open("day2/input.txt", "rt") as f:
        input = [parse_game(l.strip()) for l in f.readlines()]

    print(f"Part 1: ")
