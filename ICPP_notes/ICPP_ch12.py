# -*- coding: utf-8 -*-
"""
ICPP Chapter 12
Knapsack and Graph Optimization Problems
@author: Daniel J. Vera, Ph.D.
"""
#%% Knapsack Problems ======================================================
# Greedy Algorithms
class Item(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.weight = w
        
    def get_name(self):
        return self.name
    
    def get_value(self):
        return self.value
    
    def get_weight(self):
        return self.weight
    
    def __str__(self):
        result = '<' + self.name + ', ' + str(self.value)\
        + ', ' + str(self.weight) + '>'
        return result
    
    
def value(item):
    return item.get_value()

def weight_inverse(item):
    return 1.0 / item.get_weight()

def density(item):
    return item.get_value() / item.get_weight()

# Greedy Algorithm Implementation
def greedy(items, max_weight, key_function):
    """Assumes items a list, max_weight >= 0,
       key_function maps elements of items to numbers"""
    items_copy = sorted(items, key=key_function, reverse=True)
    result = []
    total_value, total_weight = 0.0, 0.0
    for i in range(len(items_copy)):
        if (total_weight + items_copy[i].get_weight()) <= max_weight:
            result.append(items_copy[i])
            total_weight += items_copy[i].get_weight()
            total_value += items_copy[i].get_value()
    return (result, total_value)

def build_items():
    names = ['clock', 'painting', 'radio', 'vase', 'book', 'computer']
    values = [175, 90, 20, 50, 10, 200]
    weights = [10, 9, 4, 2, 1, 20]
    items = []
    for i in range(len(values)):
        items.append(Item(names[i], values[i], weights [i]))
    return items

def test_greedy(items, max_weight, key_function):
    taken, val = greedy(items, max_weight, key_function)
    print('Total value of items taken is', val)
    for item in taken:
        print('   ', item)

def test_greedys(max_weight = 20):
    items = build_items()
    print('Use greedy by value to fill knapsack of size', max_weight)
    test_greedy(items, max_weight, value)
    print('\nUse greedy by weight to fill knapsack of size', max_weight)
    test_greedy(items, max_weight, weight_inverse)
    print('\nUse greedy by density to fill knapsack of size', max_weight)
    test_greedy(items, max_weight, density)

#%% An Optimal Solution to the 0/1 Knapsack Problem
# First recall the gen_power_set function from chapter 9 of text.
def gen_powerset(L):
    """Assumes L is a list
       Returns a list of lists that contains all possible
       combinations of the lements of L. E.g., if L is
       [1, 2], it will return a list with elements
       [], [1], [2]. and [1, 2]."""
    powerset = []
    for i in range(0, 2**len(L)):
        bin_str = get_binary_rep(i, len(L))
        subset = []
        for j in range(len(L)):
            if bin_str[j] == '1':
                subset.append(L[j])
        powerset.append(subset)
    return powerset

# uses
def get_binary_rep(n, num_digits):
    """Assumes n and num_digits are non-negative ints
       Returns a str of length num_digits that is a binary
       representation of n"""
    result = ''
    while n > 0:
        result = str(n%2) + result
        n = n // 2
    if len(result) > num_digits:
        raise ValueError('not enough digits')
    for i in range(num_digits - len(result)):
        result = '0' + result
    return result
#%%
def choose_best(pset, max_weight, get_val, get_weight):
    best_val = 0.0
    best_set = None
    for items in pset:
        items_val = 0.0
        items_weight = 0.0
        for item in items:
            items_val += get_val(item)
            items_weight += get_weight(item)
        if items_weight <= max_weight and items_val > best_val:
            best_val = items_val
            best_set = items
    return (best_set, best_val)

def test_best(max_weight = 20):
    items = build_items()
    pset = gen_powerset(items)
    taken, val = choose_best(pset, max_weight, Item.get_value,
                            Item.get_weight)
    print('Total value of items taken is', val)
    for item in taken:
        print(item)

#%% Graph Optimization Problems ============================================
class Node(object):
    def __init__(self, name):
        """Assumes name is a string"""
        self.name = name
        
    def get_name(self):
        return self.name
    
    def __str__(self):
        return self.name
    

class Edge(object):
    def __init__(self, src, dest):
        """Assumes src and dest are nodes"""
        self.src = src
        self.dest = dest
        
    def get_source(self):
        return self.src
    
    def get_destination(self):
        return self.dest
    
    def __str__(self):
        return self.src.src.get_name() + '->' + self.dest.get_name()


class WeightedEdge(Edge):
    def __init__(self, src, dest, weight = 1.0):
        """Assumes src and dest are nodes, weight a number"""
        self.src = src
        self.dest = dest
        self.weight = weight
       
    def get_weight(self):
        return self.weight
    
    def __str__(self):
        return self.src.get_name() + '->(' + str(self.weight) + ')'\
               + self.dest.get_name()


class Digraph(object):
    # nodes is a list of nodes in the graph
    # edges is a dict mapping each node to a list of its children
    def __init__(self):
        self.nodes =[]
        self.edges = {}
    
    def add_node(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.append(node)
            self.edges[node] = []
            
    def add_edge(self, edge):
        src = edge.get_source()
        dest = edge.get_destination()
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    
    def children_of(self, node):
        return self.edges[node]
    
    def has_node(self, node):
        return node in self.nodes
    
    def __str__(self):
        result = ''
        for src in self.nodes:
            for dest in self.edges[src]:
                result = result + src.get_name + '->'\
                         + dest.get_name + '\n'
        return result [:-1] # omit final newline


def Graph(Digraph):
    def add_edge(self, edge):
        Digraph.add_edge(self, edge)
        rev = Edge(edge.get_destination(), edge.get_source())
        Digraph.add_edge(self, rev)

#If client code works correctly using an instance of the supertype, it should
#also work correctly when an instance of the subtype is substituted for the 
#instance of the supertype. And indeed if client code works correctly using
#an instance of Digraph, it will work correctly if an instance of Graph is
#substituted for the instance of Digraph. The converse is not true. There are
#many algorithms that work on graphs (by exploiting the symmetry of edges)
#that do not work on directed graphs.

# Some Classic Graph-Theoretic Problems
# Shortest Path: Depth-First Search and Breadth-First Search
def print_path(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result

# depth-first search
def dfs(graph, start, end, path, shortest, to_print = False):
    """Assumes graph is a Digraph; start and end are nodes;
       path and shortest are lists of nodes
       Returns a shortest path from start to end in graph"""
    path = path + [start]
    if to_print:
           print('Current DFS path:', print_path(path))
    if start == end:
        return path
    for node in graph.children_of(start):
        if node not in path: # avoid cycles
            if shortest == None or len(path) < len(shortest):
                new_path = dfs(graph, node, end, path, shortest, to_print)
                if new_path != None:
                    shortest = new_path
    return shortest

def shortest_path(graph, start, end, to_print = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return dfs(graph, start, end, [], None, to_print)

def test_sp():
    nodes = []
    for name in range(6): # Create 6 nodes
        nodes.append(Node(str(name)))
    g = Digraph()
    for n in nodes:
        g.add_node(n)
    g.add_edge(Edge(nodes[0], nodes[1]))
    g.add_edge(Edge(nodes[1], nodes[2]))
    g.add_edge(Edge(nodes[2], nodes[3]))
    g.add_edge(Edge(nodes[2], nodes[4]))
    g.add_edge(Edge(nodes[3], nodes[4]))
    g.add_edge(Edge(nodes[3], nodes[5]))
    g.add_edge(Edge(nodes[0], nodes[2]))
    g.add_edge(Edge(nodes[1], nodes[0]))
    g.add_edge(Edge(nodes[3], nodes[1]))
    g.add_edge(Edge(nodes[4], nodes[0]))
    sp = shortest_path(g, nodes[0], nodes[5], to_print = True)
    print('Shortest path is', print_path(sp))
    
    sp = bfs(g, nodes[0], nodes[5])
    print('Shortest path found by BFS:', print_path(sp))

# breadth-first search
def bfs(graph, start, end, to_print = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    init_path = [start]
    path_queue = [init_path]
    if to_print:
        print('Current BFS path:', print_path(init_path))
    while len(path_queue) !=0:
        # Get and remove oldest element in path_queue
        tmp_path = path_queue.pop(0)
        print('Current BFS path:', print_path(tmp_path))
        last_node = tmp_path[-1]
        if last_node == end:
            return tmp_path
        for next_node in graph.children_of(last_node):
            if next_node not in tmp_path:
                new_path = tmp_path + [next_node]
                path_queue.append(new_path)
    return None

#%%=========================================================================
# Finger Exercise: Consider a digraph with weighted edges. Is the first
# path found by BFS guranteed to minimize the sum of the weights of the
# edges.

# No, the shortest may be more expensive then in terms of weights. Consider
# following example

def test_sp_weight():
    nodes = []
    for name in range(5): # Create 5 nodes
        nodes.append(Node(str(name)))
        g = Digraph()
    for n in nodes:
        g.add_node(n)
    g.add_edge(WeightedEdge(nodes[0], nodes[1], 1))
    g.add_edge(WeightedEdge(nodes[0], nodes[2], 1))
    g.add_edge(WeightedEdge(nodes[1], nodes[3], 1))
    g.add_edge(WeightedEdge(nodes[3], nodes[4], 1))
    g.add_edge(WeightedEdge(nodes[2], nodes[4], 10))
    spw = bfs(g, nodes[0], nodes[4])
    print('Shortest path found by BFS:', print_path(spw))

test_sp_weight()

# The above finds the path 0->2->4 as the shortest path but the weight,
# as we defined it is 1 + 10 = 11 for this path.

# The path 0->1->3->4 is longer but its weight is 1 + 1 + 1 + 1 = 4 < 11
