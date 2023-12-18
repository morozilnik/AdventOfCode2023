def parse_input(text):
    text = [list(line.replace('\n', '')) for line in text] # strip \n
    return text

def bring_down(data, o):
    row, col = o
    while row > 0:
        if data[row - 1][col] == '.':
            data[row][col] = '.'
            row -= 1
            data[row][col] = 'O'
        else:
            break

def get_sym(data, sym):
    return [(row, col) for row in range(len(data))
                       for col in range(len(data[row]))
                       if data[row][col] == sym]

def get_Os(data): return get_sym(data, 'O')
def get_Hs(data): return get_sym(data, '#')

def solve1(data):
    Os = get_Os(data)
    for o in Os:
        bring_down(data, o)
    Os = get_Os(data)
    res = 0
    for row, col in Os:
        res += len(data) - row
    return res

ROWS = 0
COLS = 0

def north(O_by_col, H_by_col, rows, cols):
    O_by_row = [[] for i in range(len(data))]
    for i in range(cols):
        Hs = H_by_col[i]
        next_H = Hs[0] if Hs else rows
        next_H_idx = 0
        last_o = -1
        for o in O_by_col[i]:
            while o > next_H:
                last_o = next_H
                if next_H_idx + 1 < len(Hs):
                    next_H_idx += 1
                    next_H = Hs[next_H_idx]
                else:
                    next_H = rows
            last_o += 1
            O_by_row[last_o].append(i)
    return O_by_row

def south(O_by_col, H_by_col, rows, cols):
    O_by_row = [[] for i in range(len(data))]
    for i in range(rows):
        Hs = list(reversed(H_by_col[i]))
        next_H = Hs[0] if Hs else rows
        next_H_idx = 0
        last_o = rows
        for o in reversed(O_by_col[i]):
            while o < next_H:
                last_o = next_H
                if next_H_idx + 1 < len(Hs):
                    next_H_idx += 1
                    next_H = Hs[next_H_idx]
                else:
                    next_H = -1
            last_o -= 1
            O_by_row[last_o].append(i)
    return O_by_row

def visualize_rows(O_by_row, H_by_row):
    arr = [['.'] * COLS for _ in range(ROWS)]
    for i, Os in enumerate(O_by_row):
        for o in Os:
            arr[i][o] = 'O'
    for i, Hs in enumerate(H_by_row):
        for o in Hs:
            arr[i][o] = '#'
    for line in arr:
        print("".join(line))
    print()

def visualize_cols(O_by_col, H_by_col):
    arr = [['.'] * COLS for _ in range(ROWS)]
    for i, Os in enumerate(O_by_col):
        for o in Os:
            arr[o][i] = 'O'
    for i, Hs in enumerate(H_by_col):
        for o in Hs:
            arr[o][i] = '#'
    for line in arr:
        print("".join(line))
    print()

def to_tuple(O_by_col):
    return tuple(tuple(x) for x in O_by_col)

def get_load(O_by_col):
    res = 0
    for Os in O_by_col:
        for o in Os:
            res += ROWS - o
    return res

def solve2(data):
    global ROWS, COLS
    ROWS = len(data)
    COLS = len(data[0])
    Os = get_Os(data)
    Hs = get_Hs(data)
    H_by_row = [sorted([x[1] for x in Hs if x[0] == i]) for i in range(len(data))]
    H_by_col = [sorted([x[0] for x in Hs if x[1] == i]) for i in range(len(data[0]))]
    O_by_col = [sorted([x[0] for x in Os if x[1] == i]) for i in range(len(data[0]))]

    visited_states = {}
    req_steps = 1000000000
    final_state = None
    for i in range(req_steps):
        O_by_row = north(O_by_col, H_by_col, ROWS, COLS)
        # visualize_rows(O_by_row, H_by_row)
        O_by_col = north(O_by_row, H_by_row, COLS, ROWS)
        # visualize_cols(O_by_col, H_by_col)
        O_by_row = south(O_by_col, H_by_col, ROWS, COLS)
        # visualize_rows(O_by_row, H_by_row)
        O_by_col = south(O_by_row, H_by_row, COLS, ROWS)
        state = to_tuple(O_by_col)
        if state in visited_states:
            start = visited_states[state]

            print("Found cycle with iter:", visited_states[state], i)
            cycle_length = i - start
            repeats = (req_steps - start) // cycle_length
            offset = req_steps - start - repeats * cycle_length
            if offset == 0:
                offset = cycle_length
            final_state = next(x for x in visited_states if visited_states[x] == start + offset - 1)
            break
        visited_states[state] = i
    # visualize_cols(final_state, H_by_col)
    return get_load(final_state)

if __name__ == "__main__":
    path = "Day14.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve2(data))