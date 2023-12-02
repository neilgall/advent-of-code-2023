import pytest
from .__main__ import *


@pytest.mark.parametrize(
    "input,expect",
    [
        (
            "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
            Game(id=1, turns=[
                { Colour.BLUE: 3, Colour.RED: 4 },
                { Colour.RED: 1, Colour.GREEN: 2, Colour.BLUE: 6 },
                { Colour.GREEN: 2}
            ])
        ),
        (
            "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
            Game(id=2, turns=[
                { Colour.BLUE: 1, Colour.GREEN: 2 },
                { Colour.BLUE: 4, Colour.GREEN: 3, Colour.RED: 1 },
                { Colour.BLUE: 1, Colour.GREEN: 1 }
            ])
        ),
        (
            "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
            Game(id=3, turns=[
                { Colour.GREEN: 8, Colour.BLUE: 6, Colour.RED: 20 },
                { Colour.GREEN: 13, Colour.BLUE: 5, Colour.RED: 4 },
                { Colour.GREEN: 5, Colour.RED: 1 }
            ])
        )
    ],
)
def test_parse_game(input: str, expect: Game):
    assert parse_game(input) == expect

