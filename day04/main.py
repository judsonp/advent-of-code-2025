from pathlib import Path
from typing import Iterator, List, Tuple


def neighbors(rows: List[List[str]], x: int, y: int) -> Iterator[Tuple[int, int, str]]:
    for iy in range(max(0, y - 1), min(y + 2, len(rows))):
        row = rows[iy]
        for ix in range(max(0, x - 1), min(x + 2, len(row))):
            if ix != x or iy != y:
                yield ix, iy, row[ix]


def neighbor_values(rows: List[List[str]], x: int, y: int) -> Iterator[str]:
    for _, _, nval in neighbors(rows, x, y):
        yield nval


def is_roll(val: str) -> bool:
    return val == "@"


def is_accessible(rows: List[List[str]], x: int, y: int) -> bool:
    return len(list(filter(is_roll, neighbor_values(rows, x, y)))) < 4


def part_one(rows: List[List[str]]) -> int:
    accessible = 0
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if is_roll(c) and is_accessible(rows, x, y):
                accessible += 1
    return accessible


def remove_pass(rows: List[List[str]]) -> int:
    removed = 0
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if is_roll(c) and is_accessible(rows, x, y):
                removed += 1
                rows[y][x] = "."
    return removed


def part_two(rows: List[List[str]]) -> int:
    total_removed = 0
    while True:
        removed = remove_pass(rows)
        if removed == 0:
            return total_removed
        total_removed += removed


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = [list(line) for line in f.read().splitlines()]
    assert part_one(data) == 13


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = [list(line) for line in f.read().splitlines()]
    assert part_two(data) == 43


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = [list(line) for line in f.read().splitlines()]

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
