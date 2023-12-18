import numpy as np

def parse_input(text):
    text = [line.replace('\n', '') for line in text] # strip \n
    dirs, lens, cols = [], [], []
    for line in text:
        direction, length, color = line.split(' ')
        dirs.append(direction)
        lens.append(int(length))
        cols.append(color)
    return dirs, lens, cols

def area(points):
    # Shoelace formula
    total_area = 0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        total_area += (int(x1) * int(y2) - int(x2) * int(y1))
    return abs(total_area) / 2


def solve1(dirs, lens, cols):
    cur_coord = np.array((0,0))
    digsite = [cur_coord]
    directions = {'R': np.array((0, 1)), 'L': np.array((0, -1)), 'U': np.array((-1, 0)), 'D': np.array((1, 0))}
    total_len = 0
    for d, l in zip(dirs, lens):
        total_len += l
        cur_coord += directions[d] * l
        digsite.append(np.copy(cur_coord))
    digsite = np.array(digsite)
    total_area = area(digsite)
    additional_area = (total_len / 2) + 1

    return int(total_area + additional_area)


def solve2(dirs, lens, cols):
    # Oh no, someone has switched colors and directions columns!
    new_dirs = []
    new_lens = []
    dirs = ['R', 'D', 'L', 'U']
    for color in cols:
        hex = color[2:-2]
        dir = color[-2]
        new_dirs.append(dirs[int(dir)])
        new_lens.append(int(hex, base=16))

    return solve1(new_dirs, new_lens, cols)

if __name__ == "__main__":
    path = "Day18.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve2(*data))