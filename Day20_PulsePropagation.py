import math
from queue import Queue
DEBUG = False

class Module:
    _connectionMap = {}
    _workflowQueue = Queue()

    @property
    def connectionMap(self):
        return self._connectionMap
    
    @property
    def workflowQueue(self):
        return self._workflowQueue

    def __init__(self, name, type, connections):
        self.total_signals = [0, 0]
        self.name = name
        self.type = type
        self.state = "low"
        self.connections = connections
        self.parents = []
        Module._connectionMap[name] = self

    def broadcast(self):
        smap = ["low", "high"]
        out = []
        for con in self.connections:
            # Module._connectionMap[con].receive(self.name, self.state)
            self.total_signals[smap.index(self.state)] += 1
            out.append((Module._connectionMap[con], self.state, self.name))
            # Module._workflowQueue.put(con)
            if DEBUG:
                print(f"{self.name} -{self.state}-> {con}")
        return out

    def receive(self, parent, state: str):
        self.state = state

    def __repr__(self):
        return f"{self.name}({self.type}) -> {','.join(self.connections)}"

class BroadcastModule(Module):
    def __init__(self, name, connections):
        super().__init__(name, "broadcast", connections)

class FlipFlopModule(Module):
    def __init__(self, name, connections):
        self.got_low = False
        super().__init__(name, "FlipFlop", connections)    
    
    def receive(self, parent, state):
        self.got_low = state == "low"
        if self.got_low:
            self.state = "low" if self.state == "high" else "high"
    
    def broadcast(self):
        if self.got_low:
            return super().broadcast()
        return []

class ConjunctionModule(Module):
    def __init__(self, name, connections):
        super().__init__(name, "conjunction", connections)
        self.state = True
        self.memory = {}
    
    def set_inputs(self, inputs):
        self.memory = {con: "low" for con in inputs}
    
    def receive(self, parent, state: str):
        self.memory[parent] = state
        self.state = "low" if all([x == "high" for x in self.memory.values()]) else "high"

def createNewModule(string):
    cur, connections = string.split(" -> ")
    connections = connections.split(", ")
    name = "".join(x for x in cur if x.isalpha())
    if name == "broadcaster":
        return BroadcastModule(name, connections)
    elif cur[0] == "%":
        return FlipFlopModule(name, connections)
    elif cur[0] == "&":
        return ConjunctionModule(name, connections)
    else:
        return Module(name, None, connections)


def parse_input(text):
    text = [line.strip() for line in text]
    modules = [createNewModule(line) for line in text]
    conj = [x for x in modules if x.type == "conjunction"]
    for c in conj:
        c.set_inputs([x.name for x in modules if c.name in x.connections])

    all_outputs = set(x for a in modules for x in a.connections)
    all_inputs = set(x.name for x in modules)
    for out in all_outputs - all_inputs:
        modules.append(Module(out, None, []))
    
    # Fill parents
    for x in modules:
        for con in x.connections:
            Module._connectionMap[con].parents.append(x)
    return modules

def solve1(modules):
    first = Module("in", None, ["broadcaster"])
    repeats = 1000
    conjunction_cycles = {c.name: 1 for c in modules if c.type == "conjunction"}

    for i in range(repeats):
        next_tact = first.broadcast()
        while next_tact:
            curerent_tact = next_tact
            next_tact = []
            for c, state, parent in curerent_tact:
                c.receive(parent, state)
                if c.type == "conjunction" and c.state == "low" and i > 0:
                    if conjunction_cycles[c.name] == 1:
                        conjunction_cycles[c.name] = i
                    else:
                        val = conjunction_cycles[c.name]
                        if val == i - val:
                            print(f"Cycle {c.name} confirmed: {val}")
                        else:
                            print(f"Cycle {c.name} not confirmed: {i-val} instead of {val}")

                next_tact.extend(c.broadcast())
                
        if DEBUG:
            print('----------------')
    
    print("Part 2 result:", math.lcm(*conjunction_cycles.values()))

    low_signals = sum([x.total_signals[0] for x in modules]) + repeats
    high_signals = sum([x.total_signals[1] for x in modules])
    return low_signals * high_signals



def solve2(modules):
    # I suspected that it has to do something with cycle caching
    # But I haven't realized that the input is carefully constructed
    rx = Module._connectionMap["rx"]
    # rx parent is a single conjunction module
    # And rx grandparents are conjunction modules that activate with the same cycle
    rx_grandparents = rx.parents[0].parents

    first = Module("in", None, ["broadcaster"])
    # repeats = 10000
    conjunction_cycles = {c.name: 0 for c in rx_grandparents}

    i = 0
    # for i in range(repeats):
    while not all(conjunction_cycles.values()):
        i += 1
        next_tact = first.broadcast()
        while next_tact:
            curerent_tact = next_tact
            next_tact = []
            for c, state, parent in curerent_tact:
                c.receive(parent, state)
                if c.name in conjunction_cycles and c.state == "high" and i > 0:
                    if conjunction_cycles[c.name] == 0:
                        conjunction_cycles[c.name] = i
                        print(f"Cycle {c.name} detected: {i}")
                    elif DEBUG:
                        val = conjunction_cycles[c.name]
                        if val == i - val:
                            print(f"Cycle {c.name} confirmed: {val}")
                        else:
                            print(f"Cycle {c.name} not confirmed: {i-val} instead of {val}")

                next_tact.extend(c.broadcast())
    
    res = math.lcm(*conjunction_cycles.values())
    print("Part 2 result:", res)

    return res


if __name__ == "__main__":
    path = "Day20.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve2(data))