from dataclasses import dataclass
from typing import Generator


@dataclass
class Position:
    x: int
    y: int


@dataclass
class PartNumber:
    pos: Position
    value: str

    def adjacent(self) -> Generator[Position, None, None]:
        def row(y: int) -> Generator[Position, None, None]:
            for x in range(self.pos.x-1, self.pos.x+1+len(self.value)):
                yield Position(x, y)
        yield from row(self.pos.y - 1)
        yield Position(self.pos.x - 1, self.pos.y)
        yield Position(self.pos.x + len(self.value), self.pos.y)
        yield from row(self.pos.y + 1)


@dataclass
class Symbol:
    pos: Position
    value: str


@dataclass
class Schematic:
    part_numbers: list[PartNumber]
    symbols: list[Symbol]

    def valid_part_numbers(self) -> Generator[PartNumber, None, None]:
        for part in self.part_numbers:
            if any(symbol.pos == pos for pos in part.adjacent() for symbol in self.symbols):
                yield part


def parse_input(input: str) -> Schematic:
    part_numbers = []
    symbols = []

    for y, line in enumerate(input.strip().split("\n")):
        part = None
        for x, c in enumerate(line.strip()):
            if c.isdigit():
                if part is None:
                    part = PartNumber(pos=Position(x, y), value="")
                part.value += c
            else:
                if part:
                    part_numbers.append(part)
                    part = None
                if c != '.':
                    symbols.append(Symbol(pos=Position(x, y), value=c))

    return Schematic(part_numbers=part_numbers, symbols=symbols)


def part1(input: str) -> int:
    schematic = parse_input(input)
    print(list(schematic.part_numbers[0].adjacent()))
    return sum(int(pn.value) for pn in schematic.valid_part_numbers())


def part2(input: str) -> int:
    return 0
