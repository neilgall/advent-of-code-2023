from dataclasses import dataclass
from enum import auto, Flag
from typing import Generator


class Directions(Flag):
    NONE = 0
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

    def invert(self) -> "Directions":
        dirs = Directions.NONE
        if Directions.NORTH in self:
            dirs |= Directions.SOUTH
        if Directions.SOUTH in self:
            dirs |= Directions.NORTH
        if Directions.EAST in self:
            dirs |= Directions.WEST
        if Directions.WEST in self:
            dirs |= Directions.EAST
        return dirs


ALL_DIRECTIONS = Directions.NORTH | Directions.SOUTH | Directions.EAST | Directions.WEST


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def go(self, dir: Directions) -> "Pos":
        x = self.x
        y = self.y
        if Directions.NORTH in dir:
            y -= 1
        if Directions.SOUTH in dir:
            y += 1
        if Directions.EAST in dir:
            x += 1
        if Directions.WEST in dir:
            x -= 1
        return Pos(x, y)


@dataclass(frozen=True)
class Tile:
    connected: Directions

    @classmethod
    def from_symbol(cls, symbol: str) -> "Tile" or None:
        match symbol:
            case "|":
                directions = Directions.NORTH | Directions.SOUTH
            case "-":
                directions = Directions.EAST | Directions.WEST
            case "L":
                directions = Directions.NORTH | Directions.EAST
            case "J":
                directions = Directions.NORTH | Directions.WEST
            case "7":
                directions = Directions.SOUTH | Directions.WEST
            case "F":
                directions = Directions.SOUTH | Directions.EAST
            case _:
                return None
        return Tile(connected=directions)


@dataclass
class Field:
    tiles: dict[Pos, Tile]
    start: Pos

    def __post_init__(self):
        if self.start:
            self.tiles[self.start] = self.infer_tile(self.start)

    @classmethod
    def parse(cls, input: str) -> "Field":
        tiles = {}
        start = None
        for y, line in enumerate(input.strip().split("\n")):
            for x, char in enumerate(line.strip()):
                tile = Tile.from_symbol(char)
                if tile:
                    tiles[Pos(x, y)] = tile
                elif char == "S":
                    start = Pos(x, y)

        return Field(tiles, start or Pos(0, 0))

    def connected(self, pos: Pos, direction: Directions) -> bool:
        tile = self.tiles.get(pos)
        return (direction in tile.connected) if tile else False

    def connections(self, pos: Pos) -> Directions:
        tile = self.tiles.get(pos)
        return tile.connected if tile else Directions.NONE

    def infer_tile(self, pos: Pos) -> Tile:
        directions = Directions.NONE
        for dir in ALL_DIRECTIONS:
            if self.connected(pos.go(dir), dir.invert()):
                directions |= dir
        return Tile(connected=directions)

    def find_furthest_tile_from_start(self) -> tuple[Pos, int]:
        def connected_neighbours(pos: Pos) -> Generator[Pos, None, None]:
            connections = self.connections(pos)
            for dir in ALL_DIRECTIONS:
                if dir in connections:
                    yield pos.go(dir)

        remaining = [self.start]
        distances = {self.start: 0}
        while remaining:
            pos = remaining.pop(0)
            distance = distances[pos]
            for n in connected_neighbours(pos):
                if n in distances:
                    distances[n] = min(distance + 1, distances[n])
                else:
                    distances[n] = distance + 1
                    remaining.append(n)

        return max(distances.items(), key=lambda i: i[1])


def part1(input: str) -> int:
    field = Field.parse(input)
    pos, distance = field.find_furthest_tile_from_start()
    return distance


def part2(input: str) -> int:
    return 0
