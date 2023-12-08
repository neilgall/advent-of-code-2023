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
    hands = parse_input(EXAMPLE, PART1_CONFIG)
    assert hands == [
        Hand(PART1_CONFIG, ["3", "2", "T", "3", "K"], 765),
        Hand(PART1_CONFIG, ["T", "5", "5", "J", "5"], 684),
        Hand(PART1_CONFIG, ["K", "K", "6", "7", "7"], 28),
        Hand(PART1_CONFIG, ["K", "T", "J", "J", "T"], 220),
        Hand(PART1_CONFIG, ["Q", "Q", "Q", "J", "A"], 483),
    ]


@pytest.mark.parametrize(
    "hand,hand_type",
    [
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
        ("23456", Type.HIGH_CARD),
    ],
)
def test_type(hand: str, hand_type: Type):
    assert Hand(PART1_CONFIG, list(hand), 0).type == hand_type


@pytest.mark.parametrize(
    "hand,hand_type",
    [
        ("AAAAA", Type.FIVE_OF_A_KIND),
        ("JAAAA", Type.FIVE_OF_A_KIND),
        ("8AAAA", Type.FOUR_OF_A_KIND),
        ("A8AAA", Type.FOUR_OF_A_KIND),
        ("T55J5", Type.FOUR_OF_A_KIND),
        ("KTJJT", Type.FOUR_OF_A_KIND),
        ("QQQJA", Type.FOUR_OF_A_KIND),
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
        ("KK677", Type.TWO_PAIR),
        ("A23A4", Type.ONE_PAIR),
        ("23AA4", Type.ONE_PAIR),
        ("32T3K", Type.ONE_PAIR),
        ("23456", Type.HIGH_CARD),
    ],
)
def test_type_with_jokers(hand: str, hand_type: Type):
    assert Hand(PART2_CONFIG, list(hand), 0).type == hand_type


def test_tie_break():
    hand1 = Hand(PART2_CONFIG, list("JKKK2"), 0)
    hand2 = Hand(PART2_CONFIG, list("QQQQ2"), 0)
    assert hand1 < hand2


@pytest.mark.parametrize(
    "hand1,hand2",
    [
        ("AA8AA", "AAAAA"),
        ("23332", "AA8AA"),
        ("TTT98", "23332"),
        ("23432", "TTT98"),
        ("A23A4", "23432"),
        ("23456", "A23A4"),
    ],
)
def test_ordering(hand1: str, hand2: str):
    h1 = Hand(PART1_CONFIG, list(hand1), 0)
    h2 = Hand(PART1_CONFIG, list(hand2), 0)
    assert h1 < h2
    assert h2 > h1


def test_part1():
    assert part1(EXAMPLE) == 6440


def test_part2():
    assert part2(EXAMPLE) == 5905
