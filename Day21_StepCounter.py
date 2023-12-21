from queue import Queue, PriorityQueue
import numpy as np

def parse_input(text):
    text = [list(line.strip()) for line in text]
    return text

def solve1(garden_map):
    total_steps = 15
    S_pos = [(row, col) for row in range(len(garden_map))
                        for col in range(len(garden_map[0]))
                        if garden_map[row][col] == "S"][0]
    q = Queue()
    q.put((S_pos, 0))
    visited = {S_pos: 0}
    directions = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]
    # we do bfs and take the ones of same oddity 
    while not q.empty():
        pos, steps = q.get()
        if steps == total_steps:
            continue
        for d in directions:
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            if new_pos[0] < 0 or new_pos[0] >= len(garden_map) or new_pos[1] < 0 or new_pos[1] >= len(garden_map[0]):
                continue
            if new_pos in visited:
                continue
            if garden_map[new_pos[0]][new_pos[1]] == "#":
                continue
            if garden_map[new_pos[0]][new_pos[1]] == ".":
                q.put((new_pos, steps + 1))
                visited[new_pos] = steps + 1
    
    # Debug print maze:
    for pos, steps in visited.items():
        if steps % 2 == total_steps % 2:
            garden_map[pos[0]][pos[1]] = "O"
    for row in garden_map:
        print("".join(row))
    
    result =  len([v for v in visited.values() if v % 2 == total_steps % 2])
    return result

# I leave it here as evidence a reminder of all of my struggles to find a solution while writing code
# def solve2(data):
#     # This is more tricky since map duplicates infinitely in all directions
#     # The outer line is always empty so along it we have entries.
#     # Also assume map is square
    
#     # entries would contain an array that lists the amount of reachable nodes in I steps
#     total_steps = 10
#     entries = {}
#     top_row = len(data) - 1
#     for x in range(top_row + 1):
#         entries[(x, 0)] = [[1], [0]]
#         entries[(x, top_row)] = [[1], [0]]
#         entries[(0, x)] = [[1], [0]]
#         entries[(top_row, x)] = [[1], [0]]
    
#     # exits would be how long it takes to exit on a different side
#     # here exit would be other side's entry
    
#     # starters = entries.keys()[:]
#     S_pos = [(row, col) for row in range(len(data))
#                         for col in range(len(data[0]))
#                         if data[row][col] == "S"][0]
#     starters = [(S_pos[0], 0), (S_pos[0], top_row), (0, S_pos[1]), (top_row, S_pos[1])]
#     starters.append(S_pos)
#     entries[S_pos] = [[1], [0]]
#     exits = {entry:[] for entry in starters}
#     directions = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]
#     for S in starters:
#         # bfs all inputs
#         visited = {S: 0}
#         q = Queue()
#         q.put((S, 0))
#         visited = {S: 0}
#         filled_sides = [None] * 4 # left, top, right, bottom
#         while not q.empty():
#             pos, steps = q.get()
#             for dir in directions:
#                 new_pos = (pos[0] + dir[0], pos[1] + dir[1])
#                 if new_pos[0] < 0:
#                     if filled_sides[0] is None:
#                         filled_sides[0] = ((top_row, new_pos[1], dir), steps + 1)
#                     continue
#                 if new_pos[0] >= top_row:
#                     if filled_sides[2] is None:
#                         filled_sides[2] = ((0, new_pos[1], dir), steps + 1)
#                     continue
#                 if new_pos[1] < 0:
#                     if filled_sides[1] is None:
#                         filled_sides[1] = ((new_pos[0], top_row, dir), steps + 1)
#                     continue
#                 if new_pos[1] >= top_row:
#                     if filled_sides[3] is None:
#                         filled_sides[3] = ((new_pos[0], 0, dir), steps + 1)
#                     continue
#                 if new_pos in visited:
#                     continue
#                 if data[new_pos[0]][new_pos[1]] == "#":
#                     continue
#                 if data[new_pos[0]][new_pos[1]] == ".":
#                     q.put((new_pos, steps + 1))
#                     visited[new_pos] = steps + 1
#                 if data[new_pos[0]][new_pos[1]] == "S":
#                     q.put((new_pos, steps + 1))
#                     visited[new_pos] = steps + 1
#                     exits[new_pos].append((S, steps + 1))
        
#         # Fill exits
#         for i in range(4):
#             if filled_sides[i] is not None:
#                 exits[S].append(filled_sides[i][1])
        
#         # Fill entries
#         max_steps = max(visited.values())
#         entries[S][0] = [len([x for x in visited.values() if x <= steps and x % 2 == 0]) for steps in range(max_steps + 1)]
#         entries[S][1] = [len([x for x in visited.values() if x <= steps and x % 2 == 1]) for steps in range(max_steps + 1)]
    
#     # Now we have entries and exits
#     actions = PriorityQueue()
#     actions.put((0, S_pos))
#     result = 0
#     current_steps = 0
#     entered = {(0, 0)}
#     while not actions.empty():
#         steps, pos = actions.get()
#         entry = entries[pos]
#         steps_to_fill = steps + len(entry)
#         if steps_to_fill < total_steps:
#             result += entry[(total_steps - steps_to_fill) % 2][-1]
#             for ex_pos, ex_steps, ex_dir in exits[pos]:

#                 if steps + ex_steps > total_steps:
#                     continue
#                 actions.put((steps + ex_steps, ex_pos))
#         else:
#             steps_left = total_steps - steps
#             result += entry[steps_left % 2][steps_left]
#             for ex_pos, ex_steps in exits[pos]:
#                 if steps + ex_steps > steps_left:
#                     continue
#                 actions.put((steps + ex_steps, ex_pos))



#             continue
#         if steps > total_steps:
#             break


def walk_with_overlap(garden_map, requests: list):
    sz = len(garden_map)
    S_pos = [(row, col) for row in range(len(garden_map))
                        for col in range(len(garden_map[0]))
                        if garden_map[row][col] == "S"][0]


    visited = set([S_pos])
    results = []
    directions = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]
    # we do bfs and take the ones of same oddity 
    for i in range(1, max(requests) + 1):
        new_visited = visited
        visited = set()
        for v in new_visited:
            for d in directions:
                new_pos = (v[0] + d[0], v[1] + d[1])
                if garden_map[new_pos[0] % sz][new_pos[1] % sz] == "#":
                    continue
                visited.add(new_pos)
        if i in requests:
            results.append(len(visited))
    return results
        


def solve2(garden_map):
    # So. this is one of those where the input is crazy important
    # important properties of the input:
    # A whole border of empty space
    # A whole empty line between two neighbouring pairs of s
    # The whole thing hence grows quadratically.
    N = len(garden_map) # 131
    total_steps = 26501365 # My input
    repeats = total_steps // N
    offset = total_steps % N

    sample_points = [offset, offset + N, offset + 2*N]
    walk_values = walk_with_overlap(garden_map, sample_points)
    # walk_values = [3734, 33285, 92268]
    poly = np.polyfit([0, 1, 2], walk_values, 2)

    result = np.polyval(poly, repeats)

    return int(np.round(result))


if __name__ == "__main__":
    path = "Day21.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve2(data))
