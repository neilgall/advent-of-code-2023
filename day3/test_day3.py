from .day3 import *

EXAMPLE = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def test_parser():
    schematic = parse_input(EXAMPLE)
    assert schematic == Schematic(
        part_numbers=[
            PartNumber(pos=Position(0, 0), value="467"),
            PartNumber(pos=Position(5, 0), value="114"),
            PartNumber(pos=Position(2, 2), value="35"),
            PartNumber(pos=Position(6, 2), value="633"),
            PartNumber(pos=Position(0, 4), value="617"),
            PartNumber(pos=Position(7, 5), value="58"),
            PartNumber(pos=Position(2, 6), value="592"),
            PartNumber(pos=Position(6, 7), value="755"),
            PartNumber(pos=Position(1, 9), value="664"),
            PartNumber(pos=Position(5, 9), value="598")
        ],
        symbols=[
            Symbol(pos=Position(3, 1), value="*"),
            Symbol(pos=Position(6, 3), value="#"),
            Symbol(pos=Position(3, 4), value="*"),
            Symbol(pos=Position(5, 5), value="+"),
            Symbol(pos=Position(3, 8), value="$"),
            Symbol(pos=Position(5, 8), value="*")
        ]
    )


def test_adjacents():
    part = PartNumber(pos=Position(2, 2), value="35")
    adjacents = list(part.adjacent())
    assert adjacents == [
        Position(1, 1),
        Position(2, 1),
        Position(3, 1),
        Position(4, 1),
        Position(1, 2),
        Position(4, 2),
        Position(1, 3),
        Position(2, 3),
        Position(3, 3),
        Position(4, 3)
    ]


def test_valid_part_numbers():
    schematic = parse_input(EXAMPLE)
    valid_parts = list(schematic.valid_part_numbers())
    assert valid_parts == [
        PartNumber(pos=Position(0, 0), value="467"),
        PartNumber(pos=Position(2, 2), value="35"),
        PartNumber(pos=Position(6, 2), value="633"),
        PartNumber(pos=Position(0, 4), value="617"),
        PartNumber(pos=Position(2, 6), value="592"),
        PartNumber(pos=Position(6, 7), value="755"),
        PartNumber(pos=Position(1, 9), value="664"),
        PartNumber(pos=Position(5, 9), value="598")
    ]


def test_part1():
    assert part1(EXAMPLE) == 4361
