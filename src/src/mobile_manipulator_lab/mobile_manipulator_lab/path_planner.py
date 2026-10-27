import heapq
import math


GRID = [
    "..........",
    ".##.......",
    "...#......",
    "...#..##..",
    "......#...",
    ".##.......",
    "..........",
    "..........",
]

START = (0, 0)
WORK_LOCATIONS = {
    "A": (9, 3),
    "B": (9, 7),
}

ROWS = len(GRID)
COLS = len(GRID[0])


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def is_free(pos):
    x, y = pos
    return (
        0 <= x < COLS
        and 0 <= y < ROWS
        and GRID[y][x] != "#"
    )


def astar(start, goal):
    queue = [(0, start)]
    came_from = {}
    cost = {start: 0}

    while queue:
        _, current = heapq.heappop(queue)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        x, y = current
        for nxt in [
            (x + 1, y), (x - 1, y),
            (x, y + 1), (x, y - 1)
        ]:
            if not is_free(nxt):
                continue

            new_cost = cost[current] + 1
            if nxt not in cost or new_cost < cost[nxt]:
                cost[nxt] = new_cost
                came_from[nxt] = current
                priority = new_cost + heuristic(nxt, goal)
                heapq.heappush(queue, (priority, nxt))

    return None


def display_map(path, start, goal):
    cells = [list(row) for row in GRID]

    for x, y in path or []:
        cells[y][x] = "*"

    sx, sy = start
    gx, gy = goal
    cells[sy][sx] = "S"
    cells[gy][gx] = "G"

    for row in cells:
        print(" ".join(row))


def run_trial(route_name, goal, trial):
    path = astar(START, goal)

    print(f"\n{route_name} - Trial {trial}")

    if path is None:
        print("Status: FAIL - no safe path found")
        print("Collisions: 0")
        print("Path distance: 0")
        return

    # Simulated planned path: obstacles are excluded by A*.
    collisions = sum(not is_free(p) for p in path)
    distance = sum(
        math.dist(path[i], path[i + 1])
        for i in range(len(path) - 1)
    )

    print("Status: SUCCESS - goal reached")
    print(f"Collisions: {collisions}")
    print(f"Path distance: {distance:.2f} grid units")
    display_map(path, START, goal)


def main():
    print("MOBILE MANIPULATOR - A* PATH PLANNING")
    print("S = Start, G = Goal, * = Planned path, # = Obstacle")

    for name, goal in WORK_LOCATIONS.items():
        for trial in range(1, 4):
            run_trial(f"Work Location {name}", goal, trial)


if __name__ == "__main__":
    main()