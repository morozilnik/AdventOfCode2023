from queue import Queue

def parse_input(text):
    text = [line.replace('\n', '') for line in text]
    return text

def traverse(maze, origin) -> int:
    q = Queue()
    q.put(origin) # x(row), y(col), dx, dy
    visited = {} # coords
    while not q.empty():
        cx, cy, cdx, cdy = q.get()
        if (cx, cy, cdx, cdy) in visited:
            continue
        if cx < 0 or cx >= len(maze):
            continue
        if cy < 0 or cy >= len(maze[0]):
            continue
        visited[(cx, cy, cdx, cdy)] = True
    
        maze_symbol = maze[cx][cy]

        if maze_symbol == ".":
            q.put((cx + cdx, cy + cdy, cdx, cdy))
            continue
        if maze_symbol == "/":
            q.put((cx - cdy, cy - cdx, -cdy, -cdx))
            continue
        if maze_symbol == "\\":
            q.put((cx + cdy, cy + cdx, cdy, cdx))
            continue

        if maze_symbol == "-": # horizontal splitter
            if (cdx != 0):
                q.put((cx, cy - 1, 0, -1))
                q.put((cx, cy + 1, 0, 1))
            else:
                q.put((cx + cdx, cy + cdy, cdx, cdy))
            continue

        if maze_symbol == "|": # vertical splitter
            if (cdy != 0):
                q.put((cx - 1, cy, -1, 0))
                q.put((cx + 1, cy, 1, 0))
            else:
                q.put((cx + cdx, cy + cdy, cdx, cdy))
            continue
         
    unique_coords = set(key[:2] for key in visited.keys())
    # new_maze = [['.' for _ in range(len(maze[0]))] for _ in range(len(maze))]
    # for coord in unique_coords:
    #     new_maze[coord[0]][coord[1]] = '#'
    # print('\n'.join([''.join(row) for row in new_maze]))
    return len(unique_coords)

def solve1(maze) -> int:
    return traverse(maze, (0, 0, 0, 1))

def solve2(maze) -> int:
    max_res = 0
    total_rows = len(maze)
    total_cols = len(maze[0])
    for i in range(total_rows):
        res = traverse(maze, (i, 0, 0, 1))
        res1 = traverse(maze, (i, total_cols - 1, 0, -1))
        if res > max_res:
            max_res = res
        if res1 > max_res:
            max_res = res1
    for j in range(total_cols):
        res = traverse(maze, (0, j, 1, 0))
        res1 = traverse(maze, (total_rows - 1, j, -1, 0))
        if res > max_res:
            max_res = res
        if res1 > max_res:
            max_res = res1
    return max_res


if __name__ == "__main__":
    path = "Day16.txt"
    with open(path) as f:
        text = f.readlines()
        
    maze = parse_input(text)
    print(solve2(maze))