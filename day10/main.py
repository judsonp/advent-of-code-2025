import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from bitarray import frozenbitarray
from scipy.optimize import Bounds, LinearConstraint, milp


@dataclass
class Machine:
    target_lights: frozenbitarray
    buttons: list[list[int]]
    joltage: list[int]


def parse_input(data: str) -> list[Machine]:
    machines = []

    for line in data.strip().splitlines():
        if not line.strip() or "[" not in line:
            continue

        diagram_match = re.search(r"\[([.#]+)\]", line)
        target_lights = frozenbitarray()
        if diagram_match:
            target_lights = frozenbitarray([char == "#"
                                            for char in diagram_match.group(1)])

        button_matches = re.findall(r"\(([\d,]+)\)", line)
        buttons = [[int(x) for x in match.split(",")] for match in button_matches]

        joltage_match = re.search(r"\{([\d,]+)\}", line)
        joltage = []
        if joltage_match:
            joltage = [int(x) for x in joltage_match.group(1).split(",")]

        machines.append(Machine(
            target_lights=target_lights,
            buttons=buttons,
            joltage=joltage,
        ))

    return machines


def press_button(lights: frozenbitarray, button: list[int]) -> frozenbitarray:
    return frozenbitarray([state != (index in button)
                           for index, state in enumerate(lights)])


def required_button_presses(machine: Machine) -> int:
    press_count = 0
    light_states = [frozenbitarray([False] * len(machine.target_lights))]
    visited_configurations = set(light_states)

    while True:
        press_count += 1
        new_light_states = []
        for light_state in light_states:
            for button in machine.buttons:
                new_state = press_button(light_state, button)
                if new_state == machine.target_lights:
                    return press_count
                if new_state not in visited_configurations:
                    new_light_states.append(new_state)
                    visited_configurations.add(new_state)
        light_states = new_light_states


def solve_min_sum_system(
    coefficients: list[list[int]],
    constants: list[int],
) -> int:
    # Convert inputs to numpy arrays
    a = np.array(coefficients, dtype=float)
    b = np.array(constants, dtype=float)

    # Objective: Minimize sum(x)
    # The cost vector c is all 1s -> minimize 1*x_1 + 1*x_2 + ...
    c = np.ones(a.shape[1])

    # Define Constraints: Ax = b
    # We set lower_bound == upper_bound == b to enforce equality
    constraints = LinearConstraint(a, lb=b, ub=b)

    # Define Bounds: Nonnegative Integers (x >= 0)
    # ub=np.inf means no upper limit
    positive_bounds = Bounds(lb=0.0, ub=np.inf)

    # Define Integrality: 1 forces the variable to be an integer
    integrality = np.ones(a.shape[1], dtype=int)

    # Solve
    res = milp(
        c=c,
        constraints=constraints,
        bounds=positive_bounds,
        integrality=integrality,
    )

    if res.success:
        return sum(np.round(res.x).astype(int).tolist())

    raise ValueError


def required_joltage_presses(machine: Machine) -> int:
    constants = machine.joltage
    coefficients = [
        [1 if j_idx in button else 0 for button in machine.buttons]
            for j_idx in range(len(constants))
    ]
    return solve_min_sum_system(coefficients, constants)


def part_one(machines: list[Machine]) -> int:
    return sum(required_button_presses(machine) for machine in machines)


def part_two(machines: list[Machine]) -> int:
    return sum(required_joltage_presses(machine) for machine in machines)


def test_press_buttons() -> None:
    assert press_button(frozenbitarray([True, True, False]), [0, 2]) == \
        frozenbitarray([False, True, True])


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = parse_input(f.read())
    assert part_one(data) == 7


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = parse_input(f.read())
    assert part_two(data) == 33


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = parse_input(f.read())

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
