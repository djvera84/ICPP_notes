# -*- coding: utf-8 -*-
"""
ICPP Chapter 13
Dynamic Programming
@author: Daniel J. Vera, Ph.D.
"""
import random
#%% Fibonacci Sequences, Revisited =========================================
def fib(n):
    """Assumes n is an int >= 0
       Returns Fibonacci of n"""
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def fast_fib(n, memo = {}):
    """Assumes n is an int >= 0, memo used only by recursive calls
       Returns Fibonacci of n"""
    if n == 0 or n == 1:
        return 1
    try:
        return memo[n]
    except KeyError:
        result = fast_fib(n-1, memo) + fast_fib(n-2, memo)
        memo[n] = result
        return result

#%% Dynamic Programming and the 0/1 Knapsack Problem =======================
# For completeness of these notes, I included the class from previous
# chapter notes.
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


def max_val(to_consider, avail):
    """Assumes to_consider is a list of items, avail a weight
       Returns a tuple of the total value of a solution to the 
       0/1 knapsack problem and the items of that solution"""
    if to_consider == [] or avail == 0:
        result = (0, ())
    elif to_consider[0].get_weight() > avail:
        # Explore right branch only
        result = max_val(to_consider[1:], avail)
    else:
        next_item = to_consider[0]
        # Explore left branch
        with_val, with_to_take = max_val(to_consider[1:],
                                         avail - next_item.get_weight())
        with_val += next_item.get_value()
        # Explore right branch
        without_val, without_to_take = max_val(to_consider[1:], avail)
        # Choose better branch
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
    return result

def small_test():
    names = ['a', 'b', 'c', 'd']
    vals = [6, 7, 8, 9]
    weights = [3, 3, 2, 5]
    items = []
    for i in range (len(vals)):
        items.append(Item(names[i], vals[i], weights[i]))
    val, taken = max_val(items, 5)
    for item in taken:
        print(item)
    print('Total value of items taken =', val)

def build_many_items(num_items, max_val, max_weight):
    items = []
    for i in range(num_items):
        items.append(Item(str(i),
                          random.randint(1, max_val),
                          random.randint(1, max_weight)))
    return items

def big_test(num_items):
    items = build_many_items(num_items, 10, 10)
    val, taken = max_val(items, 40) # original was 
    print('Items Taken')
    for item in taken:
        print(item)
    print('Total value of items taken =', val)

small_test()
big_test(10)
#big_test(40)
# big_test(40) will take too long!
#%% Without class structure:
def max_val2(to_consider, vals, weights, avail):
    """Assumes to_consider is a list of items, avail a weight
       Returns a tuple of the total value of a solution to the 
       0/1 knapsack problem and the items of that solution"""
    if to_consider == [] or avail == 0:
        result = (0, ())
    elif weights[0] > avail:
        # Explore right branch only
        result = max_val2(to_consider[1:], vals[1:], weights[1:], avail)
    else:
        next_item = to_consider[0]
        next_val = vals[0]
        next_weight = weights[0]
        # Explore left branch
        with_val, with_to_take = max_val2(to_consider[1:], vals[1:],
                                         weights[1:], avail - next_weight)
        with_val += next_val
        # Explore right branch
        without_val, without_to_take = max_val2(to_consider[1:], vals[1:],
                                         weights[1:], avail)
        # Choose better branch
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
    return result

names = ['a', 'b', 'c', 'd']
vals = [6, 7, 8, 9]
weights = [3, 3, 2, 5]
items = []
for i in range (len(vals)):
    items.append([names[i], vals[i], weights[i]])
val, taken = max_val2(names, vals, weights, 5)
for item in taken:
    print(item)
print('Total value of items taken =', val) 

#%%
def fast_max_val(to_consider, avail, memo = {}):
    """Assumes to_consider a list of items, avail a weight,
       memo supplied by recursive calls
       Returns a tuple of the total value of a solution to the
       0/1 knapsack problem and the items of that solution."""
    if (len(to_consider), avail) in memo:
        result = memo[(len(to_consider), avail)]
    elif to_consider == [] or avail == 0:
        result = (0, ())
    elif to_consider[0].get_weight() > avail:
        # Explore right branch only
        result = fast_max_val(to_consider[1:], avail, memo)
    else:
        next_item = to_consider[0]
        # Explore left branch
        with_val, with_to_take =\
                  fast_max_val(to_consider[1:],
                               avail - next_item.get_weight(), memo)
        with_val += next_item.get_value()
        # Exloire right branch
        without_val, without_to_take = fast_max_val(to_consider[1:],
                                                    avail, memo)
        # Choose better branch
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
    memo[(len(to_consider), avail)] = result
    return result
                  
def big_test_v2(num_items):
    items = build_many_items(num_items, 10, 10)
    val, taken = fast_max_val(items, 1000) # original was 
    print('Items Taken')
    for item in taken:
        print(item)
    print('Total value of items taken =', val)

big_test_v2(40)
big_test_v2(256)

def build_many_items_reals(num_items, max_val, max_weight):
    items = []
    for i in range(num_items):
        items.append(Item(str(i),
                          random.randint(1, max_val),
                          random.randint(1, max_weight)*random.random()))
    return items
# build_many_items_reals would give an enormous space for possible
# weights as random.random() returns a random floating point number
# between 0.0 and 1.0.