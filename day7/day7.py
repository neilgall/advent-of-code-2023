from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from parsy import char_from, decimal_digit, seq, whitespace


Card = str
CARDS = "23456789TJQKA"


class Type(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __lt__(self, other):
        return self.value < other.value


@total_ordering
@dataclass
class Hand:
    cards: list[Card]
    bid: int

    def __post__init(self):
        assert all(c in CARDS for c in self.cards)


    @property
    def type(self) -> Type:
        counts: list[int] = Counter(self.cards).values()
        if 5 in counts:
            return Type.FIVE_OF_A_KIND
        elif 4 in counts:
            return Type.FOUR_OF_A_KIND
        elif 3 in counts:
            return Type.FULL_HOUSE if 2 in counts else Type.THREE_OF_A_KIND
        elif sum(1 for c in counts if c == 2) == 2:
            return Type.TWO_PAIR
        elif 2 in counts:
            return Type.ONE_PAIR
        else:
            return Type.HIGH_CARD
        
    def __lt__(self, other: "Hand") -> int:
        d = self.type.value - other.type.value
        if d < 0: return True
        if d > 0: return False
        for c1, c2 in zip(self.cards, other.cards):
            d = CARDS.index(c1) - CARDS.index(c2)
            if d < 0: return True
            if d > 0: return False
        return False


def parse_input(input: str) -> list[Hand]:
    card = char_from(CARDS)
    cards = card.times(5)
    bid = decimal_digit.at_least(1).map(lambda ds: int("".join(ds)))
    hand = seq(cards << whitespace, bid).combine(Hand)
    return hand.sep_by(whitespace).parse(input.strip())


def part1(input: str) -> int:
    hands = parse_input(input)
    hands = sorted(hands)
    scores = [hand.bid * (rank+1) for rank, hand in enumerate(hands)]
    return sum(scores)


def part2(input: str) -> int:
    return 0
