from pathlib import Path
from typing import Iterator, List


def neighbors(rows: List[str], x: int, y: int) -> Iterator[str]:
    for iy in range(max(0, y - 1), min(y + 2, len(rows))):
        row = rows[iy]
        for ix in range(max(0, x - 1), min(x + 2, len(row))):
            if ix != x or iy != y:
                yield row[ix]


def part_one(rows: List[str]) -> int:
    accessible = 0
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c == "@":
                adjacent = len(list(filter(lambda x: x == "@", neighbors(rows, x, y))))
                if adjacent < 4:
                    accessible += 1
    return accessible


def part_two(rows: List[str]) -> int:
    return 0


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    assert part_one(data) == 13


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    # assert part_two(data) == 0


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = f.read().splitlines()

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
