import random
from copy import deepcopy

def parse_input(text):
    text = [line.strip() for line in text]
    # Represent the graph as a connections list
    graph = {}
    for line in text:
        parent, kids = line.split(': ')
        kids = kids.split()
        if parent in graph:
            graph[parent].extend(kids)
        else:
            graph[parent] = kids[:]
        for kid in kids:
            if kid in graph:
                graph[kid].append(parent)
            else:
                graph[kid] = [parent]
    return graph


def karger_min_cut(graph):
    while len(graph) > 2:
        node1 = random.choice(list(graph.keys()))
        node2 = random.choice(graph[node1])
        node2_key = next(key for key in graph if node2 in key)
        # Here is a key modification, I store all the node names in the new node
        # Because I need a list of nodes in the end
        new_node = " ".join([node1, node2_key])
        graph[new_node] = graph[node1] + graph[node2_key]
        # Remove self-loops
        for node in new_node.split():
            while node in graph[new_node]:
                graph[new_node].remove(node)

        del graph[node1]
        del graph[node2_key]
    return graph

def solve1(graph):
    min_cut = len(graph) ** 2
    result = 0
    while min_cut != 3:  # That is a given that min cut equals 3
        test_graph = deepcopy(graph)

        merged_graph = karger_min_cut(test_graph)
        min_cut = len(list(merged_graph.values())[0])
        list_lengths = [len(key.split()) for key in merged_graph]
        result = list_lengths[0] * list_lengths[1]
        
    return result
    

if __name__ == "__main__":
    path = "Day25.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve1(data))