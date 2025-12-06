from itertools import groupby
from pathlib import Path
from typing import List, Tuple

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


def part_two(ops: List[str], numbergrid: List[List[str]]) -> int:
    grand_total = 0
    transposed_grid = [list(row) for row in zip(*numbergrid)]
    raw_numbers_str = ["".join(x) for x in transposed_grid]
    raw_numbers_int = [int(x) if not x.isspace() else None for x in raw_numbers_str]
    number_groups = [list(group) for key, group in
                     groupby(raw_numbers_int, lambda x: x is None) if not key]
    assert(len(number_groups) == len(ops))
    for op, numbers in zip(ops, number_groups):
        problem = list(intersperse(op, [str(x) for x in numbers]))
        result = eval(" ".join(problem))  # noqa: S307
        grand_total += result
    return grand_total


def parse_one(data: str) -> List[List[str]]:
    return [line.split() for line in data.splitlines()]


def parse_two(data: str) -> Tuple[List[str], List[List[str]]]:
    lines = data.splitlines()
    ops = lines[-1].split()
    numbergrid = [list(line) for line in lines[:-1]]
    return ops, numbergrid


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = parse_one(f.read())
    assert part_one(data) == 4277556


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        ops, numbergrid = parse_two(f.read())
    assert part_two(ops, numbergrid) == 3263827


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = f.read()

    print(f"Part 1: {part_one(parse_one(data))}")
    print(f"Part 2: {part_two(*parse_two(data))}")
