from functools import cmp_to_key

def parse_input(text):
    text = [line.replace('\n', '') for line in text]
    hands = [line.split()[0] for line in text]
    bids = [int(line.split()[1]) for line in text]
    return hands, bids

def rank(hand):
    count_dict = {k: hand.count(k) for k in hand}
    count_arr = sorted(count_dict.values(), reverse=True)
    ## Following block is for part 2
    jval = count_dict['J'] if 'J' in count_dict else 0
    if jval:
        count_arr.remove(jval)

    if (not count_arr) and (jval == 5):
        count_arr = [5]
        print("AAAAAA")
    else:
        count_arr[0] += jval
    ## End part 2
    ranks = [[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1,1]]
    return ranks.index(count_arr)

def is_better_card(a, b):
    # order = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'] # For part 1
    order = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'] # For part 2
    return order.index(a) < order.index(b)
    
def is_better_hand(a, b):
    if rank(a) < rank(b):
        return 1
    elif rank(b) < rank(a):
        return -1
    else:
        for a1, b1 in zip(a,b):
            if is_better_card(a1, b1):
                return 1
            elif is_better_card(b1, a1):
                return -1
                
    print("Error. By now the cards are the same")
    return 0

def solve1(hands, bids):
    ranked_hands = sorted(zip(hands, bids), key=cmp_to_key(lambda x, y: is_better_hand(x[0], y[0])))
    res = 0
    idx = 1
    for _, bid in ranked_hands:
        res += bid * idx
        idx += 1
    
    return res

if __name__ == "__main__":
    path = "Day7.txt"
    with open(path) as f:
        text = f.readlines()
        
    data = parse_input(text)
    print(solve1(*data))