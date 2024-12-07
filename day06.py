from copy import deepcopy
from itertools import product
from types import SimpleNamespace as namespace

# ---------------------------- parse ----------------------------
grid = []
starting_point = -1 -1j

for y, line in enumerate(open("day06.txt").read().splitlines()):
    grid.append(list(line))

    if (x := line.find("^")) and x != -1:
        starting_point = complex(x, y)

# ---------------------------- helpers ----------------------------
dimensions = range(len(grid)), range(len(grid[0]))

def x_of(c): return int(c.real)
def y_of(c): return int(c.imag)

# return the current viewport, from guard pos up until the next obstruction or end
def lookup    (point, grid): return [grid[y][x_of(point)] for y in range(y_of(point) -1, -1, -1)]
def lookdown  (point, grid): return [grid[y][x_of(point)] for y in range(y_of(point) +1, len(grid), 1)]
def lookleft  (point, grid): return [grid[y_of(point)][x] for x in range(x_of(point) -1, -1, -1)]
def lookright (point, grid): return [grid[y_of(point)][x] for x in range(x_of(point) +1, len(grid[x_of(point)]), 1)]


# scan the viewport
# return (items count until obstruction or end, is end)
def lookat(row_or_column):
    return next(
        ((c, False) for c, element in enumerate(row_or_column, 0) if element in "O#"),
        (len(row_or_column), True)
    )

def modified(grid, x, y):
    grid = deepcopy(grid)
    grid[y][x] = 'O'
    return grid

directions = {
    #             delta, turns to
    lookup    : (+0 -1j, lookright),
    lookright : (+1 +0j, lookdown),
    lookdown  : (+0 +1j, lookleft),
    lookleft  : (-1 +0j, lookup),
}

starting_position=namespace(
    point=starting_point,
    steps_taken=0,
    direction=lookup,
    reached_destination=False
)


# ---------------------------- walk the grid ----------------------------
def walk(grid, pos):
    visited = set()

    while not pos.reached_destination:
        steps, pos.reached_destination = lookat(pos.direction(pos.point, grid))
        delta, pos.direction = directions[pos.direction]
        pos.steps_taken += steps

        for _ in range(steps + pos.reached_destination):
            visited.add(pos.point)
            pos.point += delta

        if pos.steps_taken > 10_000:
            return namespace(loops=1, unique_positions=len(visited))

    return namespace(loops=0, unique_positions=len(visited))


# ---------------------------- part 1 ----------------------------
result = walk(grid, pos=deepcopy(starting_position))
print(result.unique_positions)


# ---------------------------- part 2 ----------------------------
def brute_force_obstacles(grid):
    return sum(
        walk(modified(grid, x, y), deepcopy(starting_position)).loops
        for x, y in product(*dimensions)
    )

possible_obstruction_count = brute_force_obstacles(deepcopy(grid))
print(possible_obstruction_count)
