from dataclasses import dataclass
from itertools import pairwise
from operator import sub


@dataclass
class History:
    values: list[int]

    @classmethod
    def from_string(cls, s: str) -> "History":
        return History(values=[int(n) for n in s.strip().split()])

    def diff(self) -> "History":
        return History([p[1] - p[0] for p in pairwise(self.values)])

    def predict(self) -> int:
        if all(n == 0 for n in self.values):
            return 0
        else:
            return self.values[-1] + self.diff().predict()


def part1(input: str) -> int:
    histories = [History.from_string(line) for line in input.split("\n")]
    return sum(h.predict() for h in histories)


def part2(input: str) -> int:
    return 0
