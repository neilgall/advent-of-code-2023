from dataclasses import dataclass
from enum import Enum
from parsy import alt, decimal_digit, letter, seq, string


@dataclass
class RemoveInstruction:
    label: str


@dataclass
class ReplaceInstruction:
    label: str
    focal_length: int | None

Instruction = RemoveInstruction | ReplaceInstruction


@dataclass
class Lens:
    label: str
    focal_length: int

    def __repr__(self) -> str:
        return f"[{self.label} {self.focal_length}]"


@dataclass
class Box:
    id: int
    lens_slots: list[Lens]

    def __repr__(self) -> str:
        return f"Box {self.id}: {' '.join(repr(slot) for slot in self.lens_slots)}"

    def remove(self, label: str):
        self.lens_slots = [lens for lens in self.lens_slots if lens.label != label]

    def replace(self, label: str, focal_length: int):
        for lens in self.lens_slots:
            if lens.label == label:
                lens.focal_length = focal_length
                return
        self.lens_slots.append(Lens(label, focal_length))

    def focus_power(self) -> int:
        return sum((self.id + 1) * (n + 1) * lens.focal_length for n, lens in enumerate(self.lens_slots))


def hash(input: str) -> int:
    value = 0
    for c in input:
        value = ((value + ord(c)) * 17) % 256
    return value


def parse_instructions(input: str) -> list[Instruction]:
    label = letter.at_least(1).map("".join)
    remove_instruction = (label << string("-")).map(RemoveInstruction)
    replace_instruction = seq(label << string("="), decimal_digit.map(int)).combine(ReplaceInstruction)
    instructions = alt(remove_instruction, replace_instruction).sep_by(string(","))
    return instructions.parse(input.strip())


def run_instructions(instructions: list[Instruction]):
    boxes = [Box(n, []) for n in range(256)]
    for instruction in instructions:
        box_id = hash(instruction.label)
        if isinstance(instruction, RemoveInstruction):
            boxes[box_id].remove(instruction.label)
        else:
            boxes[box_id].replace(instruction.label, instruction.focal_length)
        # print(f"\nAfter {instruction}:")
        # for box in boxes:
        #     if box.lens_slots:
        #         print(box)
    return boxes


def part1(input: str) -> int:
    return sum(hash(part) for part in input.strip().split(","))


def part2(input: str) -> int:
    instructions = parse_instructions(input)
    boxes = run_instructions(instructions)
    return sum(box.focus_power() for box in boxes)
