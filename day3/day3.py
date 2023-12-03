from dataclasses import dataclass
from typing import Generator


@dataclass
class Position:
    x: int
    y: int

    def adjacent(self, width) -> Generator["Position", None, None]:
        def row(y: int) -> Generator["Position", None, None]:
            for x in range(self.x-1, self.x+1+width):
                yield Position(x, y)
        yield from row(self.y - 1)
        yield Position(self.x - 1, self.y)
        yield Position(self.x + width, self.y)
        yield from row(self.y + 1)


@dataclass
class PartNumber:
    pos: Position
    value: str

    def adjacent(self) -> Generator["Position", None, None]:
        return self.pos.adjacent(len(self.value))

    def is_adjacent_to(self, pos: Position) -> bool:
        positions = [Position(x, self.pos.y) for x in range(self.pos.x, self.pos.x+len(self.value))]
        return any(p in positions for p in pos.adjacent(width=1))


@dataclass
class Symbol:
    pos: Position
    value: str

    def adjacent(self) -> Generator[Position, None, None]:
        return self.pos.adjacent(1)
    

@dataclass
class Gear:
    part1: PartNumber
    part2: PartNumber

    def ratio(self) -> int:
        return int(self.part1.value) * int(self.part2.value)


@dataclass
class Schematic:
    part_numbers: list[PartNumber]
    symbols: list[Symbol]

    def valid_part_numbers(self) -> Generator[PartNumber, None, None]:
        for part in self.part_numbers:
            if any(symbol.pos == pos for pos in part.adjacent() for symbol in self.symbols):
                yield part

    def find_gears(self) -> Generator[Gear, None, None]:
        for symbol in self.symbols:
            if symbol.value == "*":
                adjacent_parts = [p for p in self.part_numbers if p.is_adjacent_to(symbol.pos)]
                if len(adjacent_parts) == 2:
                    yield Gear(part1=adjacent_parts[0], part2=adjacent_parts[1])


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
        if part:
            part_numbers.append(part)
            part = None

    return Schematic(part_numbers=part_numbers, symbols=symbols)


def part1(input: str) -> int:
    schematic = parse_input(input)
    return sum(int(pn.value) for pn in schematic.valid_part_numbers())


def part2(input: str) -> int:
    schematic = parse_input(input)
    return sum(g.ratio() for g in schematic.find_gears())
