from dataclasses import dataclass
from parsy import decimal_digit, seq, string, whitespace


@dataclass
class Card:
    id: int
    winning: list[int]
    mine: list[int]

    @classmethod
    def parse(self, input: str) -> "Card":
        integer = decimal_digit.at_least(1).map(lambda ds: int("".join(ds)))
        integer_list = integer.sep_by(whitespace)
        card_id = string("Card") >> whitespace >> integer << string(":") << whitespace
        separator = whitespace >> string("|") >> whitespace
        card = seq(card_id, integer_list, separator >> integer_list).combine(Card)
        return card.parse(input)

    def count_matching(self):
        return sum(1 for n in self.mine if n in self.winning)

    def point_value(self):
        matches = self.count_matching()
        return 0 if matches == 0 else 2 ** (matches - 1)


@dataclass
class CardSet:
    cards: list[Card]
    counts: dict[int, int]

    def __init__(self, cards: list[Card]):
        self.cards = cards
        self.counts = {(card.id): 1 for card in cards}

    def total(self) -> int:
        for card in self.cards:
            for n in range(0, card.count_matching()):
                if card.id + 1 + n in self.counts:
                    self.counts[card.id + 1 + n] += self.counts[card.id]
        return sum(self.counts.values())


def part1(input: str) -> int:
    cards = [Card.parse(line) for line in input.strip().split("\n")]
    return sum(card.point_value() for card in cards)


def part2(input: str) -> int:
    cards = [Card.parse(line) for line in input.strip().split("\n")]
    return CardSet(cards).total()
