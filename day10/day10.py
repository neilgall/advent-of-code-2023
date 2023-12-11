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

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    def __mul__(self, n: int) -> "Pos":
        return Pos(self.x * n, self.y * n)

    def __lt__(self, other: "Pos") -> bool:
        if self.y < other.y:
            return True
        if self.y == other.y and self.x < other.x:
            return True
        return False

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
    extent: Pos

    def __post_init__(self):
        if self.start:
            self.tiles[self.start] = self.infer_tile(self.start)

    @classmethod
    def parse(cls, input: str) -> "Field":
        tiles = {}
        start = None
        maxx = 0
        maxy = 0
        for y, line in enumerate(input.strip().split("\n")):
            maxy = max(y, maxy)
            for x, char in enumerate(line.strip()):
                maxx = max(x, maxx)
                tile = Tile.from_symbol(char)
                if tile:
                    tiles[Pos(x, y)] = tile
                elif char == "S":
                    start = Pos(x, y)

        return Field(tiles, start or Pos(0, 0), Pos(maxx, maxy))

    def __str__(self) -> str:
        out = ""
        for y in range(0, self.extent.y + 1):
            for x in range(0, self.extent.x + 1):
                d = self.connections(Pos(x, y))
                out += "X" if d else "."
            out += "\n"
        return out

    def positions(self) -> Generator[Pos, None, None]:
        for y in range(1, self.extent.y):
            for x in range(1, self.extent.x):
                yield Pos(x, y)

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

    def connected_neighbours(self, pos: Pos) -> Generator[Pos, None, None]:
        connections = self.connections(pos)
        for dir in ALL_DIRECTIONS:
            if dir in connections:
                yield pos.go(dir)

    def open_neighbours(self, pos: Pos) -> Generator[Pos, None, None]:
        for dir in ALL_DIRECTIONS:
            n = pos.go(dir)
            if n not in self.tiles:
                yield n

    def find_distances_from_start(self) -> dict[Pos, int]:
        remaining = [self.start]
        distances = {self.start: 0}
        while remaining:
            pos = remaining.pop(0)
            distance = distances[pos]
            for n in self.connected_neighbours(pos):
                if n in distances:
                    distances[n] = min(distance + 1, distances[n])
                else:
                    distances[n] = distance + 1
                    remaining.append(n)
        return distances

    def find_furthest_tile_from_start(self) -> tuple[Pos, int]:
        distances = self.find_distances_from_start()
        return max(distances.items(), key=lambda i: i[1])

    def zoom(self) -> "Field":
        def tiles() -> Generator[tuple[Pos, Tile], None, None]:
            for pos, tile in self.tiles.items():
                new_pos = pos * 2
                yield new_pos, tile
                if Directions.EAST in tile.connected:
                    yield new_pos.go(Directions.EAST), Tile(
                        connected=Directions.EAST | Directions.WEST
                    )
                if Directions.SOUTH in tile.connected:
                    yield new_pos.go(Directions.SOUTH), Tile(
                        connected=Directions.NORTH | Directions.SOUTH
                    )

        return Field(
            tiles=dict(tiles()),
            start=self.start * 2,
            extent=Pos(self.extent.x * 2 + 1, self.extent.y * 2 + 1),
        )

    def find_loop(self) -> list[Pos]:
        distances = self.find_distances_from_start()
        end, _ = max(distances.items(), key=lambda i: i[1])

        def find_paths_from(
            pos: Pos, path_to_pos: []
        ) -> Generator[list[Pos], None, None]:
            if pos == end:
                yield [*path_to_pos, pos]
            else:
                for n in self.connected_neighbours(pos):
                    if distances[n] == distances[pos] + 1:
                        yield from find_paths_from(n, [*path_to_pos, pos])

        paths = find_paths_from(self.start, [])
        return sorted(set(pos for path in paths for pos in path))

    def is_inside_loop(self, pos: Pos) -> tuple[bool, set[Pos]]:
        def debug(pos: Pos, checked: set[Pos], unchecked: set[Pos]):
            out = ""
            for y in range(0, self.extent.y + 1):
                for x in range(0, self.extent.x + 1):
                    p = Pos(x, y)
                    if p == pos:
                        out += "X"
                    elif p in checked:
                        out += "@"
                    elif p in unchecked:
                        out += "?"
                    else:
                        d = self.connections(p)
                        out += "*" if d else "."
                out += "\n"
            return out

        if pos in self.tiles:
            return False, set()

        unchecked = set([pos])
        checked = set()
        while len(unchecked) > 0:
            next = unchecked.pop()
            assert next not in checked
            assert next not in self.tiles
            if (
                next.x == 0
                or next.y == 0
                or next.x == self.extent.x
                or next.y == self.extent.y
            ):
                # print(f"outside {len(checked)}\n{debug(next, checked, unchecked)}")
                return False, checked | unchecked
            else:
                checked.add(next)
                neighbours = set(
                    n
                    for n in self.open_neighbours(next)
                    if n not in checked and not n in self.tiles
                )
                unchecked |= neighbours
        # print(f"inside {len(checked)}\n{debug(next, checked, unchecked)}")
        return True, checked

    def positions_enclosed_by_loop(self) -> Generator[Pos, None, None]:
        determined = set()
        for pos in self.positions():
            if pos not in determined:
                inside, checked = self.is_inside_loop(pos)
                determined |= checked
                if inside:
                    yield from checked

    def positions_enclosed_by_loop_with_squeezing(self) -> Generator[Pos, None, None]:
        field = self.zoom()
        determined = set()
        for pos in field.positions():
            if pos not in determined:
                inside, checked = field.is_inside_loop(pos)
                determined |= checked
                if inside:
                    yield from (c for c in checked if c.x % 2 == 0 and c.y % 2 == 0)


def part1(input: str) -> int:
    field = Field.parse(input)
    pos, distance = field.find_furthest_tile_from_start()
    return distance


def part2(input: str) -> int:
    print("part2", input)
    field = Field.parse(input)
    inside = list(field.positions_enclosed_by_loop_with_squeezing())
    print("result ", len(inside))
    return len(inside)
