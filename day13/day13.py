from functools import reduce
from typing import Iterable
import operator


Grid = list[str]


def transpose(grid: Grid) -> Grid:
    return [''.join(chars) for chars in zip(*grid)]


def parse_input(input: str) -> list[Grid]:
    def parse_grid(grid: str) -> Grid:
        return grid.strip().split("\n")

    return [parse_grid(g) for g in input.strip().split("\n\n")]


def find_reflections_in_row(row: str) -> Iterable[int]:
    for mid in range(2, len(row)-2):
        w = min(mid, len(row) - mid)
        left = row[mid - w : mid]
        right = row[mid: mid + w][::-1]
        if left == right:
            yield mid


def find_reflection_in_grid(grid: Grid):
    xs = [set(find_reflections_in_row(row)) for row in grid]
    mirror = reduce(operator.and_, xs)
    return next((x for x in mirror), 0)


def part1(input: str) -> int:
    grids = parse_input(input)
    xs = sum(find_reflection_in_grid(g) for g in grids)
    ys = sum(find_reflection_in_grid(transpose(g)) for g in grids)
    return xs + 100 * ys


def part2(input: str) -> int:
    return 0
