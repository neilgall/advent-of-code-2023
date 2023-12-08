from dataclasses import dataclass
from enum import Enum
from parsy import from_enum, letter, seq, string, whitespace


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
        node_id = letter.at_least(1).map("".join)
        node = seq(
            node_id << whitespace << string("=") << whitespace,
            seq(
                string("(") >> node_id << string(",") << whitespace,
                node_id << string(")")
            ).map(tuple)
        )
        document = seq(
            direction.at_least(1) << whitespace,
            node.sep_by(whitespace).map(dict)
        ).combine(Document)
        return document.parse(input.strip())

    def direction(self, pos: int) -> Direction:
        return self.directions[pos % len(self.directions)]

    def move(self, node: NodeId, pos: int) -> NodeId:
        dir = 0 if self.direction(pos) == Direction.LEFT else 1
        return self.network[node][dir]


def count_steps(doc: Document) -> int:
    node = "AAA"
    pos = 0
    while node != "ZZZ":
        node = doc.move(node, pos)
        pos += 1
    return pos


def part1(input: str) -> int:
    document = Document.parse(input)
    return count_steps(document)


def part2(input: str) -> int:
    return 0
