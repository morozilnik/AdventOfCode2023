import math
import numpy as np

def parse_input(text):
    text = [line.replace('\n', '') for line in text]
    instructions = [0 if x == "L" else 1 for x in text[0]]
    graph = {}

    for line in text[2:]:
        parent, children = line.split(' = ')
        children = children.replace("(", '').replace(')', '')
        left, right = children.split(', ')
        graph[parent] = (left, right)
    
    return instructions, graph

def solve1(instructions, graph):
    res = 0
    current = "AAA"
    while current != "ZZZ":
        for let in instructions:
            current = graph[current][let]
            res += 1
            if current == "ZZZ":
                break
    
    return res

def lcm(a, b):
    lcd = int(np.gcd(a, b))
    return a * b // lcd

def solve2(instructions, graph):
    res = 0
    all_zs = set(x for x in graph if x[-1] == 'Z') # ending positions
    all_as = [x for x in graph if x[-1] == 'A'] # starting positions

    current = all_as[:]
    task_id = 0
    cycles = []
    # For each of starting positions we iterate until we find a cycle.
    # For each cycle we should store start iteration, length and winning positions
    for starter in all_as:
        it = 0
        ind = 0
        visited = {}
        current = (starter, ind)
        while current not in visited:
            visited[current] = it
            it += 1
            inst = instructions[ind]
            ind += 1
            if (ind >= len(instructions)):
                ind = 0
            current = (graph[current[0]][inst], ind)
        cycle_start = visited[current]
        cycle_len = it - cycle_start
        cycle_wins = [visited[x] - cycle_start   for x in visited if x[0][-1] == "Z" and visited[x] >= cycle_start]
        cycles.append((cycle_start, cycle_len, cycle_wins[:]))
        print(starter, len(cycle_wins))
        
    
    print("AAA")
    iters = [cycle[0] + cycle[2][0] for cycle in cycles] # first win 
        
    return math.lcm(*iters)

    
    # Naive implementation just to test that it wouldn't work
    # while not set(current).issubset(all_zs):
    #     index = instructions[task_id]
    #     res += 1
    #     task_id += 1
    #     if task_id >= len(instructions):
    #         task_id = 0
        
    #     for i in range(len(current)):
    #         current[i] = graph[current[i]][index]
    
    # return res

if __name__ == "__main__":
    path = "Day8.txt"
    with open(path) as f:
        text = f.readlines()
        
    data = parse_input(text)
    print(solve2(*data))