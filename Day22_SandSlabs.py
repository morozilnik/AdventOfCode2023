import numpy as np

DEBUG = False

def parse_input(text):
    text = [line.strip() for line in text]
    bricks = []
    for line in text:
        start, end = line.split('~')
        st_coord = [int(x) for x in start.split(',')]
        end_coord = [int(x) for x in end.split(',')]
        bricks.append([st_coord, end_coord])

    return bricks

def is_occupied(brick, occupancy_grid):
    start, end = brick
    for z in range(start[2], end[2]+1):
        if z >= len(occupancy_grid):
            continue
        for x in range(start[0], end[0]+1):
            for y in range(start[1], end[1]+1):
                if occupancy_grid[z][x][y] != 0:
                    return True
    return False

def fill_grid(brick, occupancy_grid, value):
    og_xy_size = len(occupancy_grid[0]), len(occupancy_grid[0][0])
    for z in range(brick[0][2], brick[1][2]+1):
        while z >= len(occupancy_grid):
            occupancy_grid.append(np.zeros(og_xy_size).tolist())
        for x in range(brick[0][0], brick[1][0]+1):
            for y in range(brick[0][1], brick[1][1]+1):
                occupancy_grid[z][x][y] = value

def can_lower(brick, occupancy_grid):
    start, end = brick
    new_z = start[2] - 1
    test_brick = [start[:2] + [new_z], end[:2] + [new_z]]
    return new_z >= 0 and not is_occupied(test_brick, occupancy_grid)

def settle(bricks, occupancy_grid):
    for num, brick in enumerate(bricks):
        while can_lower(brick, occupancy_grid):
            brick[0][2] -= 1
            brick[1][2] -= 1
        fill_grid(brick, occupancy_grid, num + 1)


def find_parent_graph(bricks, occupancy_grid):
    # Find if the brick is standing on any other bricks
    parents = [set() for _ in range(len(bricks))]
    children = [set() for _ in range(len(bricks))]
    for num, brick in enumerate(bricks, 1):
        start, end = brick
        new_z = end[2] + 1
        if new_z >= len(occupancy_grid):
            continue
        above_indexes = set()
        for x in range(start[0], end[0]+1):
            for y in range(start[1], end[1]+1):
                if occupancy_grid[new_z][x][y] != 0:
                    above_indexes.add(occupancy_grid[new_z][x][y])
        children[num - 1] = above_indexes
        for child in above_indexes:
            parents[child - 1].add(num)
    return parents, children


def find_free_bricks(bricks, occupancy_grid):
    result = 0
    parents, children = find_parent_graph(bricks, occupancy_grid)
    for num, brick in enumerate(bricks):
        if len(children[num]) == 0:
            if DEBUG:
                print("Can remove brick number " + str(num + 1))
            result += 1
            continue
        for c in children[num]:
            if len(parents[c - 1]) == 1:
                break
        else:
            if DEBUG:
                print("Can remove brick number " + str(num + 1))
            result += 1
        
    return result


def find_chain_reaction(bricks, occupancy_grid):
    # So here for every supporting brick we need to find a chain reaction
    result = 0
    parents, children = find_parent_graph(bricks, occupancy_grid)
    for num, brick in enumerate(bricks):
        falls = set()
        falls.add(num + 1)
        cur_parents = parents[num]
        cur_children = children[num]
        
        checkset = cur_children.copy()
        while len(checkset) > 0:
            new_set = set()
            for c in checkset:
                if parents[c - 1] <= falls:
                    falls.add(c)
                    new_set.update(children[c - 1])
            checkset = new_set
        result += len(falls) - 1

    return result

def solve(bricks):
    # Bricks are lines of blocks with start and end coords
    # Sort by z
    bricks.sort(key=lambda x: x[0][2])
    # Lets find occupancy grid size in x-y dims
    x_max = max([x[1][0] for x in bricks])
    y_max = max([x[1][1] for x in bricks])
    occupancy_grid = [np.zeros((x_max+1, y_max+1)).tolist()] # will grow with size
    settle(bricks, occupancy_grid)
    
    # Now we need to figure which ones can be safely removed
    # Part 1
    # result = find_free_bricks(bricks, occupancy_grid)
    # Part 2
    result = find_chain_reaction(bricks, occupancy_grid)

    return result


if __name__ == "__main__":
    path = "Day22.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve(data))