def parse_input(text):
    text = [line.replace('\n', '') for line in text] # strip \n
    patterns = []
    cur_pattern = []
    for line in text:
        if not line:
            patterns.append(cur_pattern)
            cur_pattern = []
        else:
            cur_pattern.append(line)
    if cur_pattern:
        patterns.append(cur_pattern)
    return patterns

def convert_to_ints(pattern):
    bin_pattern = [line.replace('.', '0').replace('#', '1') for line in pattern]
    horizontal = [int(line, 2) for line in bin_pattern]
    vertical_lines = list(map("".join, zip(*bin_pattern))) # transpose the pattern
    vertical = [int(line, 2) for line in vertical_lines]
    return horizontal, vertical

def find_int_mirrors(arr):
    res = 0
    for i in range(len(arr) - 1):
        for j in range(min(len(arr) - i - 1, i + 1)):
            if arr[i + j + 1] != arr[i - j]:
                break
        else:
            res += (i + 1)
    return res

def count_set_bits(number):
    count = 0
    while number:
        count += number & 1
        number >>= 1
    return count

def find_smudged_mirrors(arr):
    res = 0
    for i in range(len(arr) - 1):
        val = 0
        for j in range(min(len(arr) - i - 1, i + 1)):
            diff = arr[i + j + 1] ^ arr[i - j]
            val += count_set_bits(diff)
        if val == 1:
            return i + 1
    return 0


def find_mirrors(pattern):
    hor, vert = convert_to_ints(pattern)

    # part 1
    # hm = find_int_mirrors(hor) 
    # vm = find_int_mirrors(vert)
    # part 2
    hm = find_smudged_mirrors(hor)
    vm = find_smudged_mirrors(vert)
    return hm * 100 + vm

def solve1(patterns):
    res = 0
    for pattern in patterns:

        res += find_mirrors(pattern)
    return res

if __name__ == "__main__":
    path = "Day13.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve1(data))