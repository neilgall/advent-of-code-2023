import pytest
from .day4 import *

EXAMPLE = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


@pytest.mark.parametrize(
    "input,expect",
    [
        (
            "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
            Card(
                id=1, winning=[41, 48, 83, 86, 17], mine=[83, 86, 6, 31, 17, 9, 48, 53]
            ),
        ),
        (
            "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
            Card(
                id=2,
                winning=[13, 32, 20, 16, 61],
                mine=[61, 30, 68, 82, 17, 32, 24, 19],
            ),
        ),
    ],
)
def test_parse(input: str, expect: Card):
    assert Card.parse(input) == expect


@pytest.mark.parametrize("input,expect", zip(EXAMPLE, [8, 2, 2, 1, 0, 0]))
def test_point_value(input, expect):
    card = Card.parse(input)
    assert card.point_value() == expect


def test_part1():
    assert part1("\n".join(EXAMPLE)) == 13


def test_card_set():
    card_set = CardSet([Card.parse(c) for c in EXAMPLE])
    assert card_set.counts == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}


def test_part2():
    assert part2("\n".join(EXAMPLE)) == 30
