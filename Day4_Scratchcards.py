def calc_wins(win, mine):
    return len([x for x in mine if x in win])


def solve1(data):
    res = 0
    for win, mine in data:
        wins = calc_wins(win, mine)
        if not wins:
            continue
        res += pow(2,  wins - 1)       

    return res

def solve2(data):
    res = 0
    amount_of_cards = [1 for _ in range(len(data))]
    for i in range(len(data)):
        win, mine = data[i]
        wins = calc_wins(win, mine)
        for j in range(wins):
            amount_of_cards[i + j + 1] += amount_of_cards[i]
    
    return sum(amount_of_cards)


def to_arr(line):
    return [int(x) for x in line]

def parse_input(text_input):
    text_input = [x.replace("\n", "") for x in text_input]
    output = []
    for line in text_input:
        line = line[line.index(':') + 1:] # trim Card N:
        win, mine = line.split("|")
        output.append((to_arr(win.split()), to_arr(mine.split())))
    return output
        

if __name__ == "__main__":
    path = "Day4.txt"
    with open(path) as f:
        text_input = f.readlines()
    data = parse_input(text_input)
    print(solve2(data))
