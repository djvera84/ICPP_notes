# -*- coding: utf-8 -*-
"""
ICPP Chapter 5
Structured Types, Mutability, and Higher-Order Functions
@author: Daniel J. Vera, Ph.D.
"""
#%% ========================================================================
# scalar data types: int, float, (no internal accesible structure)
# non-scalar/structured: str, tuple (simple generalization of str), list,
# range, and dict.

#%% Tuples =================================================================
# tuples are immutable ordered sequences of elements.
t1 = ()
t2 = (1, 'two', 3)
print(t1)
print(t2)

# singleton tuple with '1' is (1,), NOT (1) since () group expressions.
3 * ('a', 2)

t1 = (1, 'two', 3)
t2 = (t1, 3.25)
print(t2)
print(t1 + t2)
print((t1 + t2)[3])
print((t1 + t2)[2:5])

# A for statement can be used to iterate over the elements of a tuple.

def intersect(t1, t2):
    """Assumes tw and t2 are tuples
       Returns a tuple containing elements
       that are in both t1 and t2"""
    result = ()
    for e in t1:
        if e in t2:
            result += (e,)
    return result

x, y = (3, 4)
a, b, c = 'xyz'

def find_extreme_divisors(n1, n2):
    """Assumes that n1 and n2 are positive ints
       Retunrs a tuple containing the smallest 
       common divisor > 1 and the largest common 
       divisor of n1 and n2. If no common divisor
       returns (None, None) """
    min_val, max_val = None, None
    for i in range(2, min(n1, n2) + 1):
        if n1 % i == 0 and n2 % i == 0:
            if min_val == None:
                min_val = i
            max_val = i
    return(min_val, max_val)

min_divisor, max_divisor = find_extreme_divisors(100, 200)

#%% Ranges =================================================================
# Like strings and tuples, ranges are immutable
range(10)[2:6][2]
range(0, 7, 2) == range(0, 8, 2)
range(0, 7, 2) == range(6, -1, -2)

#%% Lists and Mutability ===================================================
# Like a tuple, a list is an ordered sequence of values, where each value
# is identified by an index, except are MUTABLE
L = ['I did it all', 4, 'love']
for i in range(len(L)):
    print(L[i])

[1, 2, 3, 4][1:3][1]

Techs = ['MIT', 'Caltech']
Ivys = ['Harvard', 'Yale', 'Brown']

Univs = [Techs, Ivys]
Univs1 = [['MIT', 'Caltech'], ['Harvard', 'Yale', 'Brown']]
print('Univs =', Univs)
print('Univs1 =', Univs1)
print(Univs == Univs1)

print(Univs == Univs1) # test value equality
print(id(Univs) == id(Univs1)) # test object equality
print('Id of Univs =', id(Univs))
print('Id of Univs 1 =', id(Univs1))

print('Ids of Univs[0] and Univs[1]',
      id(Univs[0]), id(Univs[1])) 
print('Ids of Univs1[0] and Univs1[1]', 
      id(Univs1[ 0]), id(Univs1[ 1]))

Techs.append('RPI')

print('Univs =', Univs)
print('Univs1 =', Univs1)

# As with tuples, a for statement can be used to iterate over elements
# of a list.

for e in Univs:
    print('Univs contains', e)
    print(' which contains')
    for u in e:
        print(' ', u)
        
L1 = [1, 2, 3]
L2 = [4, 5, 6]
L3 = L1 + L2
print('L3 =', L3)
L1. extend(L2)
print('L1 =', L1)
L1.append(L2)
print('L1 =', L1)

#%% Cloning

def remove_dups(L1, L2):
    """Assumes that L1 and L2 are lists.
       Removes any element from L1 that also occurs in L2"""
    for e1 in L1:
        if e1 in L2:
            L1.remove(e1)
            
L1 = [1, 2, 3, 4]
L2 = [1, 2, 5, 6]
remove_dups(L1, L2)
print('L1 =', L1)
# use slicing to avoid anomaly: for e1 in L1[:]
def remove_dups2(L1, L2):
    """Assumes that L1 and L2 are lists.
       Removes any element from L1 that also occurs in L2"""
    for e1 in L1[:]:
        if e1 in L2:
            L1.remove(e1)
            
L1 = [1, 2, 3, 4]
L2 = [1, 2, 5, 6]
remove_dups2(L1, L2)
print('L1 =', L1)

# Can also use list(L) to make a copy of the list L.

#%% List Comprehension
L = [x**2 for x in range (1,7)]
print(L)

mixed = [1, 2, 'a', 3, 4.0]
print([x**2 for x in mixed if type(x) == int])

#%% Functions as Objects ===================================================
import math
def fib(n):
    """Assumes n int >= 0. Returns Fibonacci of n"""
    if n == 0 or n == 1:
        return 1
    else: 
        return fib(n - 1) + fib(n - 2)

def apply_to_each(L, f):
    """Assumes L is a list, f a function
       Mutates L by replacing each element, e, of L by f(e)"""
    for i in range(len(L)):
        L[i] = f(L[i])

L = [1, -2, 3.33]
print('L =', L)
print('Apply abs to each element of L.')
apply_to_each(L, abs)
print('L =', L)
print('Apply int to each element of L', L)
apply_to_each(L, int)
print('L =', L)
print('Apply factorial to each element of L', L)
apply_to_each(L, math.factorial)
print('L =', L)
print('Apply Fibonnaci to each element of L', L)
apply_to_each(L, fib)
print('L =', L)

for i in map(fib, [2, 6, 4]):
    print(i)

L1 = [1, 28, 36]
L2 = [2, 57, 9]
for i in map(min, L1, L2):
    print(i)
    
lambda x, y: x * y

L = []
for i in map(lambda x, y,: x**y, [1, 2, 3, 4], [3, 2, 1, 0]):
    L.append(i)
print(L)

#%% Strings, Tuples, Ranges, and Lists

L = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even_elems = []
for e in L:
    if e%2 == 0:
        even_elems.append(e)
print(even_elems)

print('My favorite professor--John G.--rocks'. split(' ')) 
print('My favorite professor--John G.--rocks'. split('-')) 
print('My favorite professor--John G.--rocks'. split('--'))

#%% Dictionaries

month_numbers = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,'May':5, 
                 1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May'}

print('The third month is ' + month_numbers[3])
dist = month_numbers['Apr'] - month_numbers['Jan']
print('Apr and Jan are', dist, 'months apart')

month_numbers['June'] = 6
month_numbers['May'] = 'V'

keys = []
for e in month_numbers:
    keys.append(str(e))
    
print(keys)
keys.sort()
print(keys)

birth_stones = {'Jan':'Garnet', 'Feb':'Amethyst', 'Mar':'Acquamarine',
                'Apr': 'Diamond', 'May':'Emerald'}
months = birth_stones.keys()
print(months)
birth_stones['June'] = 'Pearl'
print(months)
