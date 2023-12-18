def parse_input(text):
    text = [line.replace('\n', '') for line in text] # strip \n
    records = []
    groups = []
    for line in text:
        r, g = line.split()
        records.append(r)
        groups.append(list(int(x) for x in g.split(',')))

    return records, groups

def next_state(r: list, qs: list):
    while True:
        for q in reversed(qs):
            if (r[q] == '.'):
                r[q] = '#'
                break
            else:
                r[q] = '.'
        else:
            break
        yield r

def validate(r, gs):
    r_gs = []
    cur = 0
    g_ind = 0
    for s in r:
        if s == '#':
            cur += 1
        elif cur > 0:
            if (g_ind >= len(gs) or cur != gs[g_ind]):
                return False
            r_gs.append(cur)
            cur = 0
            g_ind += 1
    if cur > 0:
        r_gs.append(cur)
    return r_gs == gs

def solve1(records, groups):
    # A shameful lazy brute-force
    arrs = 0
    for r, gs in zip(records, groups):
        qs = [i for i in range(len(r)) if r[i] == '?']
        r0 = list(r)
        for q in qs:
            r0[q] = '.'
        if (validate(r0, gs)):
            arrs += 1
        for state in next_state(r0, qs):
            if (validate(state, gs)):
                arrs += 1
    
    return arrs

def as_groups(r):
    sym_gs = []
    cur_grp = r[0]
    cur_sz = 1
    cur_st = 0
    for sym in r[1:]:
        if sym in cur_grp:
            cur_sz += 1
        elif cur_grp in "#?" and sym in "#?":
            cur_sz += 1
            cur_grp = "#?"
        else:
            sym_gs.append((cur_st, cur_sz, cur_grp))
            cur_st = cur_st + cur_sz
            cur_sz = 1
            cur_grp = sym
    sym_gs.append((cur_st, cur_sz, cur_grp))
    return sym_gs

# def soft_val(r, gs):
#     if not r:
#         return not bool(gs)
#     req_filled = sum(gs)
#     max_filled = len([x for x in r if x != '.'])
#     req_size = sum(gs) + len(gs) - 1
#     if max_filled < req_filled or len(r) < req_size:
#         return False

#     rgs = [x for x in as_groups(r) if x[-1] != '.']
#     rgs_idx = 0
#     cur_sum = 0
#     for idx, g in enumerate(gs):
#         st, sz, sym = rgs[rgs_idx]
#         if '?' in sym and sz - cur_sum < g and rgs_idx + 1 < len(rgs):
#             rgs_idx += 1
#             st, sz, sym = rgs[rgs_idx]
#             cur_sum = 0
#         # Test underflow
#         if '#' in sym and sz < g:
#             return False
#         # test overflow
#         if sym == '#':
#             if sz != g:
#                 return False
#             elif rgs_idx + 1 < len(rgs):
#                 rgs_idx += 1
        
#         # # test local overflow
#         # if sym == '#?':
#         #     # find # in a row
#         #     subr = r[st + cur_sum: st + sz]
#         #     if '#' in subr:
#         #         fill_st = subr.index('#')
#         #         if fill_st > g + 1:
#         #             return True # uncertainty is just too much at this point
#         #     else:
#         #         cur_sum += g
#         #         continue
#         #     cnt = 1
#         #     for i in range(st + cur_sum + fill_st + 1, st + sz):
#         #         if r[i] == '#':
#         #             cnt += 1
#         #         else:
#         #             break
#         #     if cnt > g:
#         #         return False
#         cur_sum += g + 1
        
#     return True

def soft_val(r, gs):
    if not r:
        return not gs
    req_filled = sum(gs)
    max_filled = len([x for x in r if x != '.'])
    req_size = sum(gs) + len(gs) - 1
    if max_filled < req_filled or len(r) < req_size:
        return False
    rs = [x for x in "".join(r).split('.') if x]
    if not rs:
        return not gs
    if '#' in rs[0] and (not gs or len(rs[0]) < gs[0]):
        return False
    if '?' not in rs[0] and len(rs[0]) > gs[0]:
        return False

    return True

    
cache = {}

def deduce(r, gs):
    if '?' not in r:
        return int(validate(r, gs))
    if ("".join(r), str(gs)) in cache:
        return cache[("".join(r), str(gs))]
    
    cand = r.index('?')
    res = 0
    # assume it '.'
    # Validate part before
    fills = r[:cand].count('#')
    test_gs = []
    iter_g = iter(gs)
    while fills > sum(test_gs):
        try:
            test_gs.append(next(iter_g))
        except StopIteration:
            return 0
    if validate(r[:cand], test_gs):
        new_gs = [x for x in iter_g]
        if soft_val(r[cand + 1:], new_gs):
            res += deduce(r[cand + 1:], new_gs)
    # now assume '#'
    r0 = list(r)
    r0[cand] = '#'
    res += deduce(r0, gs)
    cache[("".join(r), str(gs))] = res
    return res


def solve2(records, groups):
    arrs = 0
    multiplier = 5
    for r, gs in zip(records, groups):
        # Adapt the input
        r = '?'.join([r] * multiplier)
        gs = gs * multiplier

        cur_arr = deduce(r, gs)
        arrs += cur_arr

    return arrs

def pre_fill_cache():
    for i in range(1, 15):
        for j in range(1, i):
            s = '?' * i
            cache[(s, str([j]))] = i - j + 1


if __name__ == "__main__":
    path = "Day12.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    pre_fill_cache()
    print(solve2(*data))
    # print(solve1(*data))
    # records, groups = data
    # for r, g in zip(records, groups):
    #     r1 = solve1([r], [g])
    #     r2 = solve2([r], [g])
    #     if r1 != r2:
    #         print(r, ' ', g, f' {r1} != {r2}')