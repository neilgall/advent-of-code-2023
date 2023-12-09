from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import partial, total_ordering
from parsy import decimal_digit, seq, string_from, whitespace


Card = str


@dataclass
class Config:
    ranks: list[Card]
    jokers: bool

    def rank(self, card: Card):
        return self.ranks.index(card)


PART1_CONFIG = Config(list("23456789TJQKA"), False)
PART2_CONFIG = Config(list("J23456789TQKA"), True)


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
    config: Config
    cards: list[Card]
    bid: int

    def __post_init__(self):
        assert len(self.cards) == 5
        assert all(c in self.config.ranks for c in self.cards)

    @property
    def type(self) -> Type:
        counter = Counter(self.cards)
        if self.config.jokers:
            jokers = counter["J"]
            del counter["J"]
        else:
            jokers = 0
        counts = counter.values()

        if jokers == 5 or 5 in counts:
            return Type.FIVE_OF_A_KIND

        elif 4 in counts:
            match jokers:
                case 1:
                    return Type.FIVE_OF_A_KIND
                case 0:
                    return Type.FOUR_OF_A_KIND

        elif 3 in counts:
            match jokers:
                case 2:
                    return Type.FIVE_OF_A_KIND
                case 1:
                    return Type.FOUR_OF_A_KIND
                case 0:
                    return Type.FULL_HOUSE if 2 in counts else Type.THREE_OF_A_KIND

        elif sum(1 for n in counts if n == 2) == 2:
            match jokers:
                case 1:
                    return Type.FULL_HOUSE
                case 0:
                    return Type.TWO_PAIR

        elif 2 in counts:
            match jokers:
                case 3:
                    return Type.FIVE_OF_A_KIND
                case 2:
                    return Type.FOUR_OF_A_KIND
                case 1:
                    return Type.THREE_OF_A_KIND
                case 0:
                    return Type.ONE_PAIR
        else:
            match jokers:
                case 4:
                    return Type.FIVE_OF_A_KIND
                case 3:
                    return Type.FOUR_OF_A_KIND
                case 2:
                    return Type.THREE_OF_A_KIND
                case 1:
                    return Type.ONE_PAIR
                case 0:
                    return Type.HIGH_CARD

    def __lt__(self, other: "Hand") -> int:
        d = self.type.value - other.type.value
        if d < 0:
            return True
        if d > 0:
            return False

        for c1, c2 in zip(self.cards, other.cards):
            d = self.config.rank(c1) - self.config.rank(c2)
            if d < 0:
                return True
            if d > 0:
                return False
        return False


def parse_input(input: str, config: Config) -> list[Hand]:
    cards = string_from(*config.ranks).times(5)
    bid = decimal_digit.at_least(1).map(lambda ds: int("".join(ds)))
    hand = seq(cards << whitespace, bid).combine(lambda h, b: Hand(config, h, b))
    return hand.sep_by(whitespace).parse(input.strip())


def rank_and_score(hands: list[Hand]) -> int:
    hands = sorted(hands)
    scores = [hand.bid * (rank + 1) for rank, hand in enumerate(hands)]
    return sum(scores)


def part1(input: str) -> int:
    hands = parse_input(input, PART1_CONFIG)
    return rank_and_score(hands)


def part2(input: str) -> int:
    hands = parse_input(input, PART2_CONFIG)
    return rank_and_score(hands)
