import numpy as np

def parse_input(text):
    text = [line.replace('\n', '') for line in text]
    histories = [[int(x) for x in line.split()] for line in text]
    return histories

def solve1(data):
    res = 0
    for history in data:
        his = np.array(history)
        diffs = [his.tolist()]
        while not np.all(his == 0):
            his = np.diff(his)
            diffs.append(his.tolist())
        diffs[-1].append(0)
        for i in range(len(diffs) - 1, 0, -1):
            diffs[i - 1].append(diffs[i - 1][-1] + diffs[i][-1])
        res += diffs[0][-1]
    
    return res
        
def solve2(data):
    res = 0
    for history in data:
        his = np.array(history)
        diffs = [his.tolist()]
        while not np.all(his == 0):
            his = np.diff(his)
            diffs.append(his.tolist())
        diffs[-1].append(0)
        diffs[-1] = [0] + diffs[-1]
        for i in range(len(diffs) - 1, 0, -1):
            diffs[i - 1] = [diffs[i - 1][0] - diffs[i][0]] + diffs[i - 1]
        res += diffs[0][0]
    
    return res

if __name__ == "__main__":
    path = "Day9.txt"
    with open(path) as f:
        text = f.readlines()
        
    data = parse_input(text)
    print(solve2(data))