import math
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import List, Optional, Set, Tuple


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def distance(self, other: "Point") -> float:
        return math.sqrt((self.x - other.x) ** 2 +
                  (self.y - other.y) ** 2 +
                  (self.z - other.z) ** 2)


def find_and_remove(circuits: List[Set[int]], box: int) -> Optional[Set[int]]:
    for i in range(len(circuits)):
        if box in circuits[i]:
            to_return = circuits[i]
            circuits.pop(i)
            return to_return
    return None


def add_circuit(circuits: List[Set[int]], distances: List[Tuple[float, int, int]]) \
        -> Tuple[int, int]:
    _, left, right = distances.pop()
    new_circuit = {left, right}
    left_set = find_and_remove(circuits, left)
    if left_set:
        new_circuit = new_circuit.union(left_set)
    right_set = find_and_remove(circuits, right)
    if right_set:
        new_circuit = new_circuit.union(right_set)
    circuits.append(new_circuit)
    return left, right


def part_one(data: List[str], num_connections: int, num_solution_circuits: int) -> int:
    junction_boxes = [Point(*[int(x) for x in line.split(",")]) for line in data]
    distances = {(left, right): junction_boxes[left].distance(junction_boxes[right])
                 for (left, right)
                 in product(range(len(junction_boxes)), repeat = 2)
                 if left < right}

    sorted_distances = sorted([(distance, left, right)
                               for (left, right), distance
                               in distances.items()],
                               key = lambda x: x[0], reverse = True)
    circuits: List[Set[int]] = []
    for _ in range(num_connections):
        _ = add_circuit(circuits, sorted_distances)

    sorted_circuits = sorted(circuits, key = lambda x: len(x), reverse = True)

    return math.prod(len(x) for x in sorted_circuits[:num_solution_circuits])


def part_two(data: List[str]) -> int:
    junction_boxes = [Point(*[int(x) for x in line.split(",")]) for line in data]
    distances = {(left, right): junction_boxes[left].distance(junction_boxes[right])
                 for (left, right)
                 in product(range(len(junction_boxes)), repeat = 2)
                 if left < right}

    sorted_distances = sorted([(distance, left, right)
                               for (left, right), distance
                               in distances.items()],
                               key = lambda x: x[0], reverse = True)
    circuits: List[Set[int]] = []
    while True:
        left, right = add_circuit(circuits, sorted_distances)
        if len(circuits) == 1 and len(circuits[0]) == len(junction_boxes):
            return junction_boxes[left].x * junction_boxes[right].x


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    assert part_one(data, 10, 3) == 40


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = f.read().splitlines()
    assert part_two(data) == 25272


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = f.read().splitlines()

    print(f"Part 1: {part_one(data, 1000, 3)}")
    print(f"Part 2: {part_two(data)}")
