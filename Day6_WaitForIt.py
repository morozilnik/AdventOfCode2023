

def parse_input(text):
    text = [line.replace('\n', '') for line in text] # strip \n
    times = [int(x) for x in text[0][text[0].index(':') + 1:].split()]
    records = [int(x) for x in text[1][text[1].index(':') + 1:].split()]
    return times, records

def solve1(times, records):
    res = 1
    for time, record in zip(times, records):
        wins = 0
        for k in range(time):
            dist = (time - k) * k
            if (dist > record):
                wins += 1
        res *= wins
    return res

def is_increasing(time, k):
    dist_k = (time - k) * k
    dist_k1 = (time - k - 1) * (k + 1)
    return dist_k1 > dist_k

def solve2(times, records):
    time = int(''.join([str(x) for x in times]))
    record = int(''.join([str(x) for x in records]))
    # assume triangle function
    lb = 0
    hb = time // 2

    # find first win
    while (lb != hb):
        k = (lb + hb) // 2
        dist = (time - k) * k
        if (dist <= record):
            lb = k + 1
        else:
            hb = k
    min_win = k

    # find last win
    lb = time // 2
    hb = time - 2
    while (lb != hb):
        k = (lb + hb) // 2
        dist = (time - k) * k
        if (dist <= record):
            hb = k - 1
        else:
            lb = k
    
    max_win = k
    return max_win - min_win


if __name__ == "__main__":
    path = "Day6.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve2(*data))