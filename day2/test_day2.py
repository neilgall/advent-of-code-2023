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
        )
    ],
)
def test_parse_game(input: str, expect: Game):
    assert parse_game(input) == expect

