from pathlib import Path
from typing import List

from more_itertools import intersperse


def part_one(data: List[List[str]]) -> int:
    grand_total = 0
    ops = data[-1]
    values = data[:-1]
    for col in range(len(ops)):
        problem_values = [v[col] for v in values]
        problem = list(intersperse(ops[col], problem_values))
        result = eval(" ".join(problem))  # noqa: S307
        grand_total += result
    return grand_total


def part_two(data: List[List[str]]) -> int:
    return 0


def parse(data: str) -> List[List[str]]:
    return [line.split() for line in data.splitlines()]


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = parse(f.read())
    assert part_one(data) == 4277556


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = parse(f.read())
    # assert part_two(data) == 0


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = parse(f.read())

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
