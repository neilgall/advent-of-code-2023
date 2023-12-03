from day1 import calculate, parse_line_part1, parse_line_part2

if __name__ == "__main__":
    with open("day1/input.txt", "rt") as f:
        input = [l.strip() for l in f.readlines()]

    print(f"Part 1: {calculate(input, parse_line_part1)}")
    print(f"Part 2: {calculate(input, parse_line_part2)}")
