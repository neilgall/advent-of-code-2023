from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass
class Size:
    width: int
    height: int


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def path_distance_to(self, other: "Pos") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass(frozen=True)
class Galaxy:
    id: int
    x: int
    y: int

    @property
    def pos(self) -> Pos:
        return Pos(self.x, self.y)


@dataclass
class Universe:
    galaxies: set[Galaxy]
    extent: Size

    @classmethod
    def parse(cls, input: str) -> "Universe":
        galaxies = set()
        maxx = 0
        maxy = 0
        for y, line in enumerate(input.strip().split("\n")):
            maxy = max(y, maxy)
            for x, c in enumerate(line.strip()):
                maxx = max(x, maxx)
                if c == "#":
                    galaxies.add(Galaxy(id=len(galaxies), x=x, y=y))
        return Universe(galaxies, Size(maxx, maxy))

    def expand(self, amount: int):
        x = 0
        while x < self.extent.width:
            if not next(self.find_galaxies(lambda g: g.x == x), None):
                self.expand_x(x, amount)
                x += amount + 1
            else:
                x += 1

        y = 0
        while y < self.extent.height:
            if not next(self.find_galaxies(lambda g: g.y == y), None):
                self.expand_y(y, amount)
                y += amount + 1
            else:
                y += 1

    def find_galaxies(self, predicate: Callable[[Galaxy], bool]) -> Iterable[Galaxy]:
        return (g for g in self.galaxies if predicate(g))

    def expand_x(self, x: int, amount: int):
        self.extent.width += amount
        for g in list(self.find_galaxies(lambda g: g.x > x)):
            self.galaxies.remove(g)
            self.galaxies.add(Galaxy(g.id, g.x + amount, g.y))

    def expand_y(self, y: int, amount: int):
        self.extent.height += amount
        for g in list(self.find_galaxies(lambda g: g.y > y)):
            self.galaxies.remove(g)
            self.galaxies.add(Galaxy(g.id, g.x, g.y + amount))

    def shortest_paths(self) -> Iterable[int]:
        starts = self.galaxies.copy()
        while starts:
            start = starts.pop()
            for end in starts.copy():
                yield start.pos.path_distance_to(end.pos)


def part1(input: str) -> int:
    universe = Universe.parse(input)
    universe.expand(1)
    return sum(d for d in universe.shortest_paths())


def part2(input: str, expand=1_000_000) -> int:
    universe = Universe.parse(input)
    universe.expand(expand - 1)
    return sum(d for d in universe.shortest_paths())
