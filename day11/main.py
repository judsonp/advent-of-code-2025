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


def create_reverse_graph(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    reverse_graph: dict[str, list[str]] = {}
    for in_node, out_nodes in graph.items():
        for out_node in out_nodes:
            if out_node not in reverse_graph:
                reverse_graph[out_node] = []
            reverse_graph[out_node].append(in_node)
    return reverse_graph


def compute_reachability(start_name: str, end_name: str, reverse_graph: dict[str, list[str]]) -> set[str]:
    nodes_to_visit = [end_name]
    reachable = {end_name}
    while len(nodes_to_visit) > 0:
        visit = nodes_to_visit.pop()
        if visit in reverse_graph and visit != start_name:
            connections = reverse_graph[visit]
            for connection in connections:
                if connection not in reachable:
                    reachable.add(connection)
                    nodes_to_visit.append(connection)
    return reachable



def paths_between(start_name: str, end_name: str, graph: dict[str, list[str]], reverse_graph: dict[str, list[str]]) -> set[GraphPath]:
    start = GraphPath([start_name])
    paths_to_process = [start]
    paths_reaching_end = set()
    paths_visited = set()
    can_reach_end = compute_reachability(start_name, end_name, reverse_graph)

    while len(paths_to_process) > 0:
        path = paths_to_process.pop()
        if path.end() in graph:
            connections = graph[path.end()]
            for connection in connections:
                if connection not in path.path and connection in can_reach_end:
                    new_path = path.and_then(connection)
                    if new_path not in paths_visited:
                        paths_visited.add(new_path)
                        paths_to_process.append(new_path)
                        if connection == end_name:
                            paths_reaching_end.add(new_path)

    return paths_reaching_end


def part_one(graph: dict[str, list[str]]) -> int:
    reverse_graph = create_reverse_graph(graph)
    return len(paths_between("you", "out", graph, reverse_graph))


def part_two(graph: dict[str, list[str]]) -> int:
    reverse_graph = create_reverse_graph(graph)
    a = paths_between("svr", "fft", graph, reverse_graph)
    print("a")
    b = paths_between("fft", "dac", graph, reverse_graph)
    print("b")
    c = paths_between("dac", "out", graph, reverse_graph)
    print("c")
    d = paths_between("svr", "dac", graph, reverse_graph)
    print("d")
    e = paths_between("dac", "fft", graph, reverse_graph)
    print("e")
    f = paths_between("fft", "out", graph, reverse_graph)
    print("f")
    return len(a) * len(b) * len(c) + len(d) * len(e) * len(f)


def test_parse_input() -> None:
    with Path("example.txt").open() as f:
        data = parse_input(f.read())
    assert data["you"] == ["bbb", "ccc"]


def test_part_one() -> None:
    with Path("example.txt").open() as f:
        data = parse_input(f.read())
    assert part_one(data) == 5


def test_part_two() -> None:
    with Path("example2.txt").open() as f:
        data = parse_input(f.read())
    assert part_two(data) == 2


if __name__ == "__main__":
    with Path("input.txt").open() as f:
        data = parse_input(f.read())

    print(f"Part 1: {part_one(data)}")
    print(f"Part 2: {part_two(data)}")
