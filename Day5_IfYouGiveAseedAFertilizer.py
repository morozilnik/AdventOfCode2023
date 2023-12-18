from dataclasses import dataclass

@dataclass
class Map:
    orig: str
    dest: str
    st_dest: int
    st_source: int
    size: int

    def __init__(self, orig, dest, st_dest, st_source, size):
        self.orig = orig
        self.dest = dest
        self.st_dest = st_dest
        self.st_source = st_source
        self.size = size

def parse_input(text):
    text = [line.replace('\n', '') for line in text] # strip \n
    seeds = [int(x) for x in text[0][text[0].index(':') + 1:].split()]
    maps = {}
    current_orig = ""
    current_dest = ""
    for line in text[1:]:
        if not line:
            parsing_map = False
        elif "map" in line:
            name = line[:line.index('map') - 1]
            current_orig, to, current_dest = name.split('-')
            maps[current_orig] = []
        else:
            params = [int(x) for x in line.split()]
            maps[current_orig].append(Map(current_orig, current_dest, *params))
    
    return seeds, maps


def solve1(data):
    seeds, maps = data
    locations = []
    for seed in seeds:
        current_map = "seed"
        current_val = seed
        while current_map != "location":
            for map in maps[current_map]:
                if map.st_source <= current_val < map.st_source + map.size:
                    current_val = map.st_dest + current_val - map.st_source
                    current_map = map.dest
                    break
            else:
                current_map = maps[current_map][0].dest
        locations.append(current_val)
    
    return min(locations)

def find_intersection(range1, range2):
    start1, size1 = range1
    start2, size2 = range2
    end1 = start1 + size1
    end2 = start2 + size2

    # Check for no intersection
    if end1 <= start2 or end2 <= start1:
        return None

    # Calculate intersection
    intersection_start = max(start1, start2)
    intersection_end = min(end1, end2)
    intersection_size = intersection_end - intersection_start

    return (intersection_start, intersection_size)

def range_diff(range_papa, range_spinogriz):
    r1, sz1 = range_papa
    r2, sz2 = range_spinogriz
    e1 = r1 + sz1
    e2 = r2 + sz2

    new_ranges = []
    if (r2 > r1):
        new_ranges.append((r1, r2 - r1))
    if (e1 > e2):
        new_ranges.append((e2, e1 - e2))
    
    return new_ranges

def remove_subranges(range_papa, subranges: list):
    results = [range_papa]
    for subrange in subranges:
        new_results = []
        for r in results:
            intersection = find_intersection(r, subrange)
            if intersection is not None:
                new_results.extend(range_diff(r, intersection))
        results = new_results[:]
    return results
        

def solve2(data):
    seeds, maps = data
    seed_ranges = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    current_map = "seed"
    while current_map != "location":
        new_seed_ranges = []
        for r in seed_ranges:
            orig_ranges_from_r = []
            new_ranges_from_r = []
            for map in maps[current_map]:
                intersection = find_intersection(r, (map.st_source, map.size))
                if intersection is not None:
                    orig_ranges_from_r.append(intersection)
                    new_ranges_from_r.append((map.st_dest + intersection[0] - map.st_source, intersection[1]))
            new_seed_ranges.extend(new_ranges_from_r)
            new_seed_ranges.extend(remove_subranges(r, orig_ranges_from_r))
        seed_ranges = new_seed_ranges[:]
        current_map = maps[current_map][0].dest
    return min([x[0] for x in seed_ranges])

if __name__ == "__main__":
    path = "Day5.txt"
    with open(path) as f:
        text = f.readlines()
    input_data = parse_input(text)
    print(solve2(input_data))