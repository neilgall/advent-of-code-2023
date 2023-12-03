import pytest
from .day2 import *


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


@pytest.mark.parametrize('input,expect', [
    ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", True),
    ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", True),
    ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", False),
    ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", False),
    ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", True)
])
def test_is_game_possible(input: str, expect: bool):
    game = parse_game(input)
    assert game.is_possible({ Colour.RED: 12, Colour.GREEN: 13, Colour.BLUE: 14 }) == expect


@pytest.mark.parametrize('input,expect', [
    ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", 48),
    ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", 12),
    ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", 1560),
    ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", 630),
    ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", 36)
])
def test_smallest_load_power(input: str, expect: bool):
    game = parse_game(input)
    assert game.smallest_load_power() == expect
