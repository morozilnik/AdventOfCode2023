
def solve1(text_array):
    res = 0
    for line in text_array:
        digits = [x for x in line if x.isdigit()]
        num = int(digits[0] + digits[-1])
        res += num
    return res

def solve2(text_array):
    letters = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    let_map = list(enumerate(letters, 1))
    res = 0
    for line in text_array:
        for num, lets in let_map:
            line = line.replace(lets, lets + str(num) + lets)
        digits = [x for x in line if x.isdigit()]
        num = int(digits[0] + digits[-1])
        res += num
    return res


if __name__ == "__main__":
    path = "Day1.txt"
    with open(path) as f:
        coordinates = f.readlines()
    
    print(solve2(coordinates))