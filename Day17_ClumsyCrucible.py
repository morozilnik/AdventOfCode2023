from queue import Queue, PriorityQueue

def parse_input(text):
    text = [[int(x) for x in line.replace('\n', '')] for line in text]
    return text

def solve1(maze):
    dyn_table = [[[-1 for _ in range(12)] for _ in range(len(maze[0]))] for _ in range(len(maze))]
    start = (0, 0)
    directions = 4
    right, down, left, up = range(4)
    dir_adders = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    max_straight = 3
    for i in range(directions):
        for j in range(max_straight):
            dyn_table[start[0]][start[1]][i * max_straight + j] = 0
    q = Queue()
    q.put(((0, 1), right * max_straight)) # 0 corresponds to 1 step in that direction, so offset 1
    q.put(((1, 0), down * max_straight))
    dyn_table[0][1][right * max_straight] = maze[0][1]
    dyn_table[1][0][down * max_straight] = maze[1][0]
    while not q.empty():
        coord, cdir = q.get()
        x, y = coord
        dr = cdir // max_straight
        for i in range(-1, 2): # turn left, straight or right
            next_steps = 0 if i != 0 else (cdir % max_straight) + 1
            if next_steps >= max_straight:
                continue
            next_dir = (dr + i) % directions
            adder = dir_adders[next_dir]
            next_coord = (x + adder[0], y + adder[1])
            if next_coord[0] < 0 or next_coord[0] >= len(maze) or next_coord[1] < 0 or next_coord[1] >= len(maze[0]):
                continue
            new_val = dyn_table[x][y][cdir] + maze[next_coord[0]][next_coord[1]]

            for i in range(min(max_straight, next_steps + 1)):
                dt_val = dyn_table[next_coord[0]][next_coord[1]][next_dir * 3 + i]
                if dt_val != -1 and dt_val <= new_val:
                    break
            else:
                dyn_table[next_coord[0]][next_coord[1]][next_dir * 3 + next_steps] = new_val
                q.put((next_coord, next_dir * 3 + next_steps))
    final_coord_table = [dyn_table[-1][-1][i] for i in range(12) if dyn_table[-1][-1][i] != -1]
    print(dyn_table[-1][-1])
    return min(final_coord_table)

def dist(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def solve2(maze): 
    # There is a mistake somewhere here and it takes too long.
    # So rather than fix it i rewrote it completely using more correct A* algorithm
    directions = 4
    min_straight = 4
    max_straight = 10
    dyn_table = [[[10000 for _ in range(directions * max_straight)] for _ in range(len(maze[0]))] for _ in range(len(maze))]
    start = (0, 0)
    right, down, left, up = range(4)
    dir_adders = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i in range(directions):
        for j in range(max_straight):
            dyn_table[start[0]][start[1]][i * max_straight + j] = 0
    q = Queue()
    q.put(((0, min_straight), right * max_straight + min_straight - 1)) # 0 corresponds to 1 step in that direction, so offset 1
    q.put(((min_straight, 0), down * max_straight + min_straight - 1))
    dyn_table[0][min_straight][right * max_straight + min_straight - 1] = sum(maze[0][1:min_straight + 1])
    dyn_table[min_straight][0][down * max_straight + min_straight - 1] = sum([maze[i][0] for i in range(1, min_straight + 1)])
    while not q.empty():
        coord, cdir = q.get()
        x, y = coord
        dr = cdir // max_straight
        cur_steps = cdir % max_straight
        for i in range(-1, 2): # turn left, straight or right
            next_steps = min_straight if i != 0 else cur_steps + 1
            if next_steps >= max_straight:
                continue
            next_dir = (dr + i) % directions
            adder = dir_adders[next_dir]
            mult = 1 if i == 0 else next_steps
            next_coord = (x + adder[0] * mult, y + adder[1] * mult)
            if next_coord[0] < 0 or next_coord[0] >= len(maze) or next_coord[1] < 0 or next_coord[1] >= len(maze[0]):
                continue
            new_val = dyn_table[x][y][cdir]
            tmp_coord = coord
            while tmp_coord[0] != next_coord[0] or tmp_coord[1] != next_coord[1]:
                tmp_coord = (tmp_coord[0] + adder[0], tmp_coord[1] + adder[1])
                new_val += maze[tmp_coord[0]][tmp_coord[1]]

            for i in range(min_straight, min(max_straight, next_steps + 1)):
                dt_val = dyn_table[next_coord[0]][next_coord[1]][next_dir * max_straight + i]
                if dt_val != -1 and dt_val <= new_val:
                    break
            else:
                dyn_table[next_coord[0]][next_coord[1]][next_dir * max_straight + next_steps] = new_val
                q.put((next_coord, next_dir * max_straight + next_steps))
    final_coord_table = [dyn_table[-1][-1][i] for i in range(len(dyn_table[-1][-1])) if dyn_table[-1][-1][i] != -1]
    # min_table = [[min(dyn_table[i][j]) for j in range(len(dyn_table[0]))] for i in range(len(dyn_table))]
    # print(min_table)
    print(dyn_table[-1][-1])
    return min(final_coord_table)

def solve2_astar(maze):
    directions = 4
    min_straight = 4
    max_straight = 10
    start = (0, 0)
    right, down, left, up = range(4)
    dir_adders = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    br = (len(maze) - 1, len(maze[0]) - 1)
    q = PriorityQueue()
    q.put((dist(start, br), (start, up, 0, 0)))
    q.put((dist(start, br), (start, left, 0, 0)))
    cur = q.get()
    steps_done = 0
    visited = {}
    while cur[1][0] != br:
        steps_done += 1
        qval, val = cur
        coord, direction, steps, price = val
        last_visit = visited.get((coord, direction, steps))
        if last_visit is not None and last_visit <= price:
            cur = q.get()
            continue
        else:
            visited[(coord, direction, steps)] = price
        for i in range(-1, 2):
            next_dir = (direction + i) % directions
            adder = dir_adders[next_dir]
            if next_dir == direction:
                if steps == max_straight:
                    continue
                next_coord = (coord[0] + adder[0], coord[1] + adder[1])
                if next_coord[0] < 0 or next_coord[0] >= len(maze) or next_coord[1] < 0 or next_coord[1] >= len(maze[0]):
                    continue
                new_price = price + maze[next_coord[0]][next_coord[1]]
                new_val = new_price + dist(next_coord, br)
                q.put((new_val, (next_coord, next_dir, steps + 1, new_price)))
            else:
                next_coord = (coord[0] + min_straight * adder[0], coord[1] + min_straight * adder[1])
                if next_coord[0] < 0 or next_coord[0] >= len(maze) or next_coord[1] < 0 or next_coord[1] >= len(maze[0]):
                    continue
                new_price = price
                for i in range(1, min_straight + 1):
                    tmp_coord = (coord[0] + i * adder[0], coord[1] + i * adder[1])
                    new_price += maze[tmp_coord[0]][tmp_coord[1]]
                new_val = new_price + dist(next_coord, br)
                q.put((new_val, (next_coord, next_dir, min_straight, new_price)))
        cur = q.get()

    print(f"Done {steps_done} steps")
    return cur[0]

if __name__ == "__main__":
    path = "Day17.txt"
    with open(path) as f:
        text = f.readlines()
        
    maze = parse_input(text)
    print(solve2_astar(maze))