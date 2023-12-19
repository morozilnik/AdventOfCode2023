import numpy as np
import re
from functools import reduce
import operator

class Rule:
    less = None
    out = None
    key = None
    val = None

    def __init__(self, rule_str):
        # Example Rule
        if ':' not in rule_str:
            self.out = rule_str
            return

        check, self.out = rule_str.split(':')
        self.less = '<' in check
        if self.less:
            self.key, val = check.split('<')
        else:
            self.key, val = check.split('>')
        self.val = int(val)

    def check(self, var):
        if self.less is None:
            return True

        val = var[self.key]
        if self.less:
            return val < self.val
        else:
            return val > self.val
    
    def accept(self):
        return self.out
    
    def __repr__(self) -> str:
        if self.less is None:
            return f"{self.out}"
        return f"{self.key} {'<' if self.less else '>'} {self.val} -> {self.out}"

def parse_input(text):
    text = [line.strip() for line in text]
    empty_id = text.index("")
    workflows = {}
    for line in text[:empty_id]:
        inst_idx = line.index('{')
        name = line[:inst_idx]
        rules = [Rule(rule) for rule in line[inst_idx + 1:-1].split(',')]
        workflows[name] = rules

    variables = []
    for line in text[empty_id + 1:]:
        # example line: "{x=787,m=2655,a=1222,s=2876}"
        matches = re.findall(r'(\w+)=(\d+)', line)
        variables.append({k: int(v) for k, v in matches})


    return workflows, variables

def solve1(workflows, variables):
    result = 0
    for var in variables:
        wf = workflows["in"]
        is_end = False
        while not is_end:
            for rule in wf:
                if rule.check(var):
                    wf_key = rule.accept()
                    if wf_key == 'A':
                        result += sum(var.values())
                        is_end = True
                    elif wf_key == 'R':
                        is_end = True
                    else:
                        wf = workflows[wf_key]
                    break
        
    return result

def follow(workflows, intervals, cur_wf, cur_rule_idx):
    if cur_wf == "A":
        return reduce(operator.mul, [b - a + 1 for a, b in intervals.values()], 1)
    elif cur_wf == "R":
        return 0

    result = 0
    wf = workflows[cur_wf]
    rule = wf[cur_rule_idx]
    if rule.less is None:
        return follow(workflows, intervals, rule.accept(), 0)
    key = rule.key
    val = rule.val
    interval = intervals[key]
    new_interval = intervals.copy()
    if (val < interval[0] and not rule.less) or (val > interval[1] and rule.less):
        result += follow(workflows, intervals, rule.accept(), 0)
    elif interval[0] < val <= interval[1] and rule.less:
        new_interval[key] = [interval[0], val - 1] # pass
        result += follow(workflows, new_interval, rule.accept(), 0)
        new_interval[key] = [val, interval[1]]     # fail
        result += follow(workflows, new_interval, cur_wf, cur_rule_idx + 1)
    elif interval[0] <= val < interval[1] and not rule.less:
        new_interval[key] = [interval[0], val]  # fail
        result += follow(workflows, new_interval, cur_wf, cur_rule_idx + 1)
        new_interval[key] = [val + 1, interval[1]] # pass
        result += follow(workflows, new_interval, rule.accept(), 0)

    return result

def solve2(workflows, variables):
    default_intervals = {x:[1, 4000] for x in "xmas"}
    result = follow(workflows, default_intervals, "in", 0)

    return result

if __name__ == "__main__":
    path = "Day19.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve2(*data))