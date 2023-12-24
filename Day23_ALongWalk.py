import string
from queue import Queue

def parse_input(text):
    text = [line.strip() for line in text]
    return text

DEBUG = False

SLOPES = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}
DIRECTIONS = {(0, 1), (1, 0), (0, -1), (-1, 0)}
CACHE = {} # (started): (max length, visited)

track_maze = []
usable_symbols = string.ascii_uppercase + string.ascii_lowercase
used_symbols = set()

def longest_route(maze, start, visited, tm_sym = 'A'):
    global CACHE, track_maze
    global usable_symbols, used_symbols
    # We go recursively, assuming there's not a lot of branches
    end = (len(maze) - 1, len(maze[0]) - 2)
    if start in CACHE and len(CACHE[start][1] & visited) == 0:
        return CACHE[start][0]
    length = 0
    options = [start]
    branch_visited = set()
    while len(options) == 1: # Follow the branch until intersection
        length += 1
        current = options[0]
        branch_visited.add(current)
        if DEBUG:
            track_maze[current[0]][current[1]] = tm_sym
        if current == end:
            CACHE[start] = (length, visited)
            return length
        options = []
        sym = maze[current[0]][current[1]]
        if sym in SLOPES:
            slope = SLOPES[sym]
            new_pos = (current[0] + slope[0], current[1] + slope[1])
            if new_pos in visited or new_pos in branch_visited:
                return 0 # A special case when we wrongly put direction back
            options.append(new_pos)
            continue

        for direction in DIRECTIONS:
            next_pos = (current[0] + direction[0], current[1] + direction[1])
            if next_pos[0] < 0 or next_pos[0] >= len(maze) or next_pos[1] < 0 or next_pos[1] >= len(maze[0]):
                continue
            if maze[next_pos[0]][next_pos[1]] == '#':
                continue
            if next_pos in visited or next_pos in branch_visited:
                continue
            options.append(next_pos)
    
    if DEBUG:
        with open('dbg.txt', 'w') as f:
            f.write('\n'.join(["".join(line) for line in track_maze]))
    

    if not options:
        return length if current == end else 0
    
    subbranch_results = []
    output_visited = branch_visited.copy()
    for option in options:
        if len(used_symbols) == len(usable_symbols):
            used_symbols = set()
        next_symbol = [symbol for symbol in usable_symbols if symbol not in used_symbols][0]
        used_symbols.add(next_symbol)
        subbranch_results.append(longest_route(maze, option, visited | branch_visited, next_symbol))
        if option in CACHE:
            output_visited |= CACHE[option][1]
    
    result = length + max(subbranch_results)
    CACHE[start] = (result, output_visited)
    
    return length + max(subbranch_results)


def solve1(maze):
    # we need to find a longest route through the maze
    start = (0, 1)
    result = longest_route(maze, start, set())
    return result - 1 # Don't count the start

def convert_to_graph(maze):
    start = (0, 1)
    end = (len(maze) - 1, len(maze[0]) - 2)
    nodes = [start, end]
    edges = []
    # Intersections are new nodes, paths are edges
    visited = set()
    visited.add(start)
    current = (1, 1)
    q = Queue()
    q.put((start, current))
    current_node = start
    while not q.empty():
        current_node, current = q.get()
        length = 1
        found_node = False
        while not found_node:
            visited.add(current)
            options = []
            for d in DIRECTIONS:
                next_pos = (current[0] + d[0], current[1] + d[1])
                if next_pos[0] < 0 or next_pos[0] >= len(maze) or next_pos[1] < 0 or next_pos[1] >= len(maze[0]):
                    continue
                if maze[next_pos[0]][next_pos[1]] == '#':
                    continue
                if next_pos in nodes and next_pos != current_node:
                    edges.append((current_node, next_pos, length + 1))
                    found_node = True
                    break
                if next_pos in visited:
                    continue
                options.append(next_pos)
            if not options:
                break
            if len(options) == 1:
                current = options[0]
                length += 1
                continue
            found_node = True
            nodes.append(current)
            edges.append((current_node, current, length))
            for option in options:
                q.put((current, option))
    
    # represent edges as a dict
    edges_dict = {}
    for edge in edges:
        if edge[0] not in edges_dict:
            edges_dict[edge[0]] = []
        if edge[1] not in edges_dict:
            edges_dict[edge[1]] = []
        edges_dict[edge[0]].append((edge[1], edge[2]))
        edges_dict[edge[1]].append((edge[0], edge[2]))
       
    return nodes, edges_dict

def bruteforce(nodes, edges, current, visited, length)->int:
    # Find longest route in a graph
    end = nodes[1]
    visited.add(current)
    results = []
    for edge in edges[current]:
        node, e_length = edge
        if node in visited:
            continue
        if node == end:
            visited.remove(current)
            return length + e_length
        result = bruteforce(nodes, edges, node, visited, length + e_length)
        results.append(result)
    visited.remove(current)
    return max(results) if results else 0


def solve2(maze):
    global track_maze
    # Just try to adapt the data to substitute slopes for usual tile ('.')
    translation_table = str.maketrans({symbol: '.' for symbol in SLOPES})
    maze = [line.translate(translation_table) for line in maze]
    # track_maze = [list(line) for line in maze]
    nodes, edges = convert_to_graph(maze)
    start = (0, 1)
    # result = longest_route(maze, (0, 1), set())
    result = bruteforce(nodes, edges, start, set(), 0)
    return result

if __name__ == "__main__":
    path = "Day23.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve2(data))
