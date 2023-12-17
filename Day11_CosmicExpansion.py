import numpy as np

def parse_input(text):
    text = [line.replace('\n', '') for line in text]
    coordinates = []
    for num, line in enumerate(text):
        for i, sym in enumerate(line):
            if sym == '#':
                coordinates.append((num, i))
    return coordinates

def solve1(coordinates, old_galaxies = False):
    coords = np.array(coordinates)
    multiplier = 1 if not old_galaxies else 999999
    mentioned_rows = set(x[0] for x in coords)
    mentioned_cols = set(x[1] for x in coords)
    max_coord = np.max(coordinates, axis=0)
    empty_rows = set(range(max_coord[0])) - mentioned_rows
    empty_cols = set(range(max_coord[1])) - mentioned_cols
    
    total_dist = 0
    for i1, c1 in enumerate(coordinates):
        for i2, c2 in enumerate(coordinates[i1 + 1:], i1 + 1):
            x1, y1 = c1
            x2, y2 = c2
            bad_rows = empty_rows & set(range(min(x1, x2), max(x1, x2)))
            bad_cols = empty_cols & set(range(min(y1, y2), max(y1, y2)))
            dist_x = abs(x1 - x2) + multiplier * len(bad_rows)
            dist_y = abs(y1 - y2) + multiplier * len(bad_cols)
            total_dist += dist_x + dist_y
    return total_dist


if __name__ == "__main__":
    path = "Day11.txt"
    with open(path) as f:
        text = f.readlines()
        
    coordinates = parse_input(text)
    print(solve1(coordinates, True))