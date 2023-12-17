def strip_endings(text):
    return [x.replace("\n", "") for x in text]

def read_input(path):
    with open(path) as f:
        text = f.readlines()
        text = strip_endings(text)
    return text

def is_special(sym):
    return not (sym.isdigit() or sym == '.')

def in_bounds(var, left, right):
    return var >= left and var < right

def check_nearby_specials(text, x, y, check):
    for k in range (-1, 2):
        for l in range(-1, 2):
            if in_bounds(x+k, 0, len(text)) and in_bounds(y + l, 0, len(text[0]))  \
                and check(text[x + k][y + l]):
                return True
    return False

def solve1(text):
    current_num_str = ""
    current_special = False
    current_sum = 0
    for num, line in enumerate(text):
        for pos, sym in enumerate(line):
            if sym.isdigit():
                current_num_str += sym
                current_special = current_special or check_nearby_specials(text, num, pos, is_special)
            else:
                if current_special and current_num_str:
                    current_sum += int(current_num_str)
                current_num_str = ""
                current_special = False
    return current_sum

def find_connected_gears(gears, num, pos):
    connected_gears = []
    for index, gear in enumerate(gears):
        dist_x = abs(num - gear[0])
        dist_y = abs(pos - gear[1])
        if (dist_x <= 1 and dist_y <= 1):
            connected_gears.append(index)
    return connected_gears


def solve2(text):
    is_gear = lambda sym: sym == '*'
    all_gears = []
    for num, line in enumerate(text):
        for pos, sym in enumerate(line):
            if is_gear(sym):
                all_gears.append((num, pos))
    all_gears.sort()
    
    numbers_with_gears = []
    current_connected_gears = []
    current_num_str = ""
    for num, line in enumerate(text):
        for pos, sym in enumerate(line):
            if sym.isdigit():
                current_num_str += sym
                connected_gears = find_connected_gears(all_gears, num, pos)
                current_connected_gears.extend(connected_gears)
            else:
                if current_num_str:
                    for gear in current_connected_gears:
                        numbers_with_gears.append((int(current_num_str), gear))
                        
                current_num_str = ""
                current_connected_gears = []
    
    gear_numbers = [[] for _ in all_gears]
    for num, gear in numbers_with_gears:
        if num not in gear_numbers[gear]:
            gear_numbers[gear].append(num)
    
    result = 0
    for gn in gear_numbers:
        if len(gn) == 2:
            result += gn[0] * gn[1]
    
    return result

if __name__ == "__main__":
    path = "Day3.txt"
    text = read_input(path)
    print(solve2(text))
