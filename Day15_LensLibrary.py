
def parse_input(text):
    text = [line.replace('\n', '') for line in text] # strip \n
    return "".join(text).split(',')

def myHash(s):
    cur = 0
    for sym in s:
        cur += ord(sym)
        cur *= 17
        cur %= 256
    return cur


def solve1(data):
    res = 0
    for s in data:
        res += myHash(s)
    return res

class Lens:
    def __init__(self, name, val):
        self.name = name
        self.val = val
        self.next = None
        self.prev = None
    
class LinkedList:
    def __init__(self):
        self.head = None
        self.lookup = {}
    
    def add(self, name, val):
        new_node = Lens(name, val)
        if name in self.lookup:
            self.lookup[name].val = val
            return
        if self.head:
            new_node.next = self.head
            self.head.prev = new_node
        self.head = new_node
        self.lookup[name] = new_node
    
    def delete(self, name):
        if name not in self.lookup:
            return
        node = self.lookup[name]
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.head:
            self.head = node.next
        del self.lookup[name]
    
    def focus_power(self):
        res = 0
        node = self.head
        idx = len(self.lookup)
        while node is not None:
            res += idx * node.val
            idx -= 1
            node = node.next
        return res
    
    def __repr__(self):
        s = "LL["
        node = self.head
        node_vals = []
        while node is not None:
            node_vals.append(f"{node.name}({node.val})")
            node = node.next
        s = s + "->".join(node_vals) + "]"
        return s


def solve2(data):
    boxes = [LinkedList() for _ in range(256)]
    for s in data:
        if '-' in s:
            # Dash command - remove lens
            lens = s.replace('-', '')
            boxnum = myHash(lens)
            box = boxes[boxnum]
            box.delete(lens)
        elif '=' in s:
            name, val = s.split('=')
            boxnum = myHash(name)
            box = boxes[boxnum]
            box.add(name, int(val))
    res = 0
    for i, box in enumerate(boxes, 1):
        res += i * box.focus_power()
    return res


if __name__ == "__main__":
    path = "Day15.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve2(data))