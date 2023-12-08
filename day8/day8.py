from dataclasses import dataclass
from enum import Enum
from functools import reduce
from parsy import alt, decimal_digit, from_enum, letter, seq, string, whitespace
from sympy.ntheory.modular import solve_congruence
import operator


NodeId = str


class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"


@dataclass
class Document:
    directions: list[Direction]
    network: dict[NodeId, (NodeId, NodeId)]

    @classmethod
    def parse(cls, input: str) -> "Document":
        direction = from_enum(Direction)
        node_id = alt(letter, decimal_digit).at_least(1).map("".join)
        node = seq(
            node_id << whitespace << string("=") << whitespace,
            seq(
                string("(") >> node_id << string(",") << whitespace,
                node_id << string(")"),
            ).map(tuple),
        )
        document = seq(
            direction.at_least(1) << whitespace, node.sep_by(whitespace).map(dict)
        ).combine(Document)
        return document.parse(input.strip())

    def direction(self, pos: int) -> Direction:
        return self.directions[pos % len(self.directions)]

    def move(self, node: NodeId, pos: int) -> NodeId:
        dir = 0 if self.direction(pos) == Direction.LEFT else 1
        return self.network[node][dir]

    def start_nodes(self) -> list[NodeId]:
        return [id for id in self.network.keys() if id.endswith("A")]

    def count_steps(self, start_node: NodeId) -> tuple[int, int]:
        node = start_node
        pos = 0
        zs = 0
        initial_steps = 0
        while zs < 2:
            node = self.move(node, pos)
            pos += 1
            if node.endswith("Z"):
                if zs == 0:
                    initial_steps = pos
                zs += 1
        return initial_steps, pos - initial_steps


def part1(input: str) -> int:
    document = Document.parse(input)
    steps, loop = document.count_steps("AAA")
    return steps


def part2(input: str) -> int:
    document = Document.parse(input)
    solution = solve_congruence(
        *(document.count_steps(id) for id in document.start_nodes())
    )
    return solution[1]
