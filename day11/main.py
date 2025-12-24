from pathlib import Path


class GraphPath:
    path: list[str]
    path_str: str

    def __init__(self, path: list[str]) -> None:
        self.path = path
        self.path_str = " ".join(path)

    def __hash__(self) -> int:
        return self.path_str.__hash__()

    def end(self) -> str:
        return self.path[-1]

    def and_then(self, connection: str) -> "GraphPath":
        return GraphPath([*self.path, connection])


def parse_input(data: str) -> dict[str, list[str]]:
    machines = {}
    for line in data.splitlines():
        m_in, m_out_str = line.split(":", 1)
        m_out_list = m_out_str.split()
        machines[m_in] = m_out_list
    return machines


def part_one(graph: dict[str, list[str]]) -> int:
    start = GraphPath(["you"])
    paths_to_process = [start]
    paths_reaching_end = set()
    paths_visited = set()

    while len(paths_to_process) > 0:
        path = paths_to_process.pop()
        if path.end() in graph:
            connections = graph[path.end()]
            for connection in connections:
                new_path = path.and_then(connection)
                if new_path not in paths_visited:
                    paths_visited.add(new_path)
                    paths_to_process.append(new_path)
                    if connection == "out":
                        paths_reaching_end.add(new_path)

    return len(paths_reaching_end)


def part_two(data: dict[str, list[str]]) -> int:
    return 0


def test_parse_input() -> None:
    with Path("example.txt").open() as f:
        data = parse_input(f.read())
    assert data["you"] == ["bbb", "ccc"]


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = parse_input(f.read())
    assert part_one(data) == 5


def test_part_two() -> None:
    with Path("example.txt").open() as f:
        data = parse_input(f.read())
    # assert part_two(data) == 0


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = parse_input(f.read())

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
