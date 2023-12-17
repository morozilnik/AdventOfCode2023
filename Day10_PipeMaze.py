import numpy as np
from queue import Queue

def parse_input(text):
    text = [line.replace('\n', '') for line in text]
    return text


def solve1(maze):
    cons = {
       # Connections for symbols sym: [(dx, dy)]
       '|' : [(1, 0), (-1, 0)], # row-column order
       '-' : [(0, 1), (0, -1)],
       'L' : [(-1, 0), (0, 1)],
       'J' : [(-1, 0), (0, -1)],
       '7' : [(1, 0), (0, -1)],
       'F' : [(1, 0), (0, 1)],
       '.' : [],
       'S' : [(1, 0), (-1, 0), (0, 1), (0, -1)]
    }
    connectors = {}
    for sym, con_arr in cons.items():
        for con in con_arr:
            anticon = (-con[0], -con[1])
            if anticon in connectors:
                connectors[anticon].append(sym)
            else:
                connectors[anticon] = [sym]
    
    orig_maze = maze
    maze = [list(row) for row in orig_maze]
    s_row = next(i for i in range(len(maze)) if 'S' in maze[i])
    s_col = maze[s_row].index('S')

    steps = 0
    q = Queue()
    q.put((s_row, s_col, steps))
    while not q.empty():
        row, col, step = q.get()
        sym = maze[row][col]
        if sym == '*':
            continue
        for dx, dy in cons[sym]:
            cx = row + dx
            cy = col + dy
            if 0 <= cx < len(maze) and 0 <= cy < len(maze[0]):
                cand = maze[cx][cy]
                if cand in connectors[(dx, dy)]:
                    q.put((cx, cy, step + 1))
                    steps = step + 1
        maze[row][col] = '*'
    
    # return steps # part 1
    
    # Part 2: Raycast
    enclosed = 0
    vert_brakes = ['-', 'F', '7', 'L', 'J'] # Ignore L and J bc we can move a little bit and not include them
    opposites = {'L': '7', 'J': 'F', '7': 'L', 'F': 'J'}
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '*':
                continue
            
            changes = 0

            alternate = False
            starter = ''
            for k in range(0, i):
                if orig_maze[k][j] == 'S':
                    alternate = True
                    changes = 0
                    break
                elif maze[k][j] == '*':
                    cur = orig_maze[k][j]
                    if cur in vert_brakes:
                        if cur == '-':
                            changes += 1
                        elif starter:
                            if opposites[starter] == cur:
                                changes += 1
                            starter = ''
                        else:
                            starter = cur

                        
            if alternate:
                for k in range(i + 1, len(maze)):
                    if maze[k][j] == '*':
                        cur = orig_maze[k][j]
                        if cur in vert_brakes:
                            if cur == '-':
                                changes += 1
                            elif starter:
                                if opposites[starter] == cur:
                                    changes += 1
                                starter = ''
                            else:
                                starter = cur

            if changes % 2 == 1:
                enclosed += 1
                maze[i][j] = 'I'
                
    
    for line in maze:
        print(''.join(line))
    return enclosed


if __name__ == "__main__":
    path = "Day10.txt"
    with open(path) as f:
        text = f.readlines()
        
    data = parse_input(text)
    print(solve1(data))