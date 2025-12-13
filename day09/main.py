from dataclasses import dataclass
from itertools import chain, combinations, pairwise, product
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def rectangle_area(self, other: "Point") -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


type Line = tuple[Point, Point]


def line_intersects_rectangle(a: Point, b: Point, line: Line) -> bool:
    # This input happens to have only horizontal or vertical lines,
    # and we assume that property (so we check it here).
    if line[0].x != line[1].x and line[0].y != line[1].y:
        raise ValueError

    if line[0].x == line[1].x:
        # vertical line
        # line is within the x extent of the rectangle
        if min(a.x, b.x) < line[0].x < max(a.x, b.x):
            # line is not entirely on one side or the other on the y axis
            return not (max(line[0].y, line[1].y) <= min(a.y, b.y) or
                        min(line[0].y, line[1].y) >= max(a.y, b.y))
        return False
    if line[0].y == line[1].y:
        # horizontal line
        # line is within the y extent of the rectangle
        if min(a.y, b.y) < line[0].y < max(a.y, b.y):
            # line is not entirely on one side or the other on the x axis
            return not (max(line[0].x, line[1].x) <= min(a.x, b.x) or
                        min(line[0].x, line[1].x) >= max(a.x, b.x))
        return False

    # already guaranteed this
    raise ValueError


def is_valid_rectangle(a: Point, b: Point, lines: list[Line]) -> bool:
    return not any(line_intersects_rectangle(a, b, line) for line in lines)


def part_one(data: list[str]) -> int:
    points = [Point(*[int(x) for x in line.split(",")]) for line in data]
    return max(a.rectangle_area(b) for a, b in product(points, repeat = 2))


def part_two(data: list[str]) -> int:
    points = [Point(*[int(x) for x in line.split(",")]) for line in data]
    lines = list(pairwise(chain(points, [points[0]])))

    candidates = sorted(
        ((a.rectangle_area(b), a, b) for a, b in combinations(points, 2)),
        key=lambda x: x[0],
        reverse=True,
    )

    for area, a, b in candidates:
        if is_valid_rectangle(a, b, lines):
            return area

    return 0


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    assert part_one(data) == 50


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    assert part_two(data) == 24


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = f.read().splitlines()

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
