import pytest
from .day7 import *


EXAMPLE = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def test_parser():
    hands = parse_input(EXAMPLE)
    assert hands == [
        Hand(["3", "2", "T", "3", "K"], 765),
        Hand(["T", "5", "5", "J", "5"], 684),
        Hand(["K", "K", "6", "7", "7"], 28),
        Hand(["K", "T", "J", "J", "T"], 220),
        Hand(["Q", "Q", "Q", "J", "A"], 483)
    ]


@pytest.mark.parametrize("hand,hand_type", [
    ("AAAAA", Type.FIVE_OF_A_KIND),
    ("8AAAA", Type.FOUR_OF_A_KIND),
    ("A8AAA", Type.FOUR_OF_A_KIND),
    ("AA8AA", Type.FOUR_OF_A_KIND),
    ("AAA8A", Type.FOUR_OF_A_KIND),
    ("AAAA8", Type.FOUR_OF_A_KIND),
    ("23332", Type.FULL_HOUSE),
    ("32332", Type.FULL_HOUSE),
    ("23323", Type.FULL_HOUSE),
    ("33232", Type.FULL_HOUSE),
    ("TTT98", Type.THREE_OF_A_KIND),
    ("TT9T8", Type.THREE_OF_A_KIND),
    ("T9T8T", Type.THREE_OF_A_KIND),
    ("98TTT", Type.THREE_OF_A_KIND),
    ("23432", Type.TWO_PAIR),
    ("23234", Type.TWO_PAIR),
    ("43232", Type.TWO_PAIR),
    ("A23A4", Type.ONE_PAIR),
    ("23AA4", Type.ONE_PAIR),
    ("23456", Type.HIGH_CARD)
])
def test_type(hand: str, hand_type: Type):
    assert Hand(list(hand), 0).type == hand_type


@pytest.mark.parametrize("hand1,hand2", [
    ("AA8AA", "AAAAA"),
    ("23332", "AA8AA"),
    ("TTT98", "23332"),
    ("23432", "TTT98"),
    ("A23A4", "23432"),
    ("23456", "A23A4")
])
def test_ordering(hand1: str, hand2: str):
    assert Hand(list(hand1), 0) < Hand(list(hand2), 0)
    assert Hand(list(hand2), 0) > Hand(list(hand1), 0)

def test_part1():
    assert part1(EXAMPLE) == 6440


def test_part2():
    assert part2(EXAMPLE) == 0
