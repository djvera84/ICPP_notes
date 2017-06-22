# -*- coding: utf-8 -*-
"""
ICPP Chapter 9
A Simplistic Introduction to Algorithmic Complexity
@author: Daniel J. Vera, Ph.D.
"""
#%% Thinking About Computational Complexity ================================
# How long will the following function take to run?
def f(i):
    """Assumes i is an int and i >= 0"""
    answer = 1
    while i >= 1:
        answer *= i
        i -= 1
    return answer

def linear_search(L, x):
    for e in L:
        if e == x:
            return True
    return False

def fact(n):
    """Assumes n is a natural number
       Returns n!"""
    answer = 1
    while n > 1:
        answer *= n
        n -= 1
    return answer
# number of steps to run this program fact(.) is something like
#    2 : 1 for the initial assignment statement and 1 for the return
# + 5n : 1 step for the test in while 2 steps for each assignent

def square_root_exhaustive(x, epsilon):
    """Assumes x and epsilon are positive floats & epsilon < 1
       Returns a y such that y*y is within epsilon of x"""
    step = epsilon**2
    ans = 0.0
    while abs(ans**2 - x) >= epsilon and ans*ans <= x:
        ans += step
    if ans*ans > x:
        raise ValueError
    return ans

def square_root_bisection(x, epsilon):
    """Assumes x and epsilon are positive floats & epsilon < 1
       Returns a y such that y*y is within epsilon of x"""
    low = 0.0
    high = max(1.0, x)
    ans = (high + low) / 2.0
    while abs(ans**2 - x) >= epsilon:
        if ans**2 < x:
            low = ans
        else:
            high = ans
        ans = (high + low) / 2.0
    return ans

# Exhaustive enumeration is slow, slow enough to be impractical for
# many combinations of x and epsilon. E.g. 100, 0.0001 requires 1
# billion iterations, roughly, for while loop whereas the bisection
# algorithm requires about 20 of a slightly more complex loop.

#%% Asymptotic Notation ====================================================
def g(x):
    """Assumes x is an int > 0"""
    ans = 0
    # Loop that takes constant time
    for i in range(1000):
        ans += 1
    print('Number of additions so far', ans)
    # Loop that takes time x
    for i in range(x):
        ans += 1
    print('Number of additions so far', ans)
    # Nested loops take time x**2
    for i in range(x):
        for j in range(x):
            ans += 1
            ans += 1
    print('Number of additions so far', ans)
    return ans
# Running time = 1000 + x + 2*x**2 if each line of code takes one unit
# of time
g(10)
g(1000)

#%% Some Important Complexity Classes ======================================
# n = 'size' of inputs to the function
# O(1)          = constant running time
# O(log n)      = logarithmic running time
# O(n)          = linear running time
# O(n log n)    = log-linear running time
# O(n^k)        = polynomial running time, k is constant
# O(c^n)        = exponential running time, c is constant

# Constant Complexity 
# Asympptotic complexity is independent of the size of inputs.
# Constant running time does not imply there are no loops or recursive
# calls in code, just that the number of iterations or calls
# is independent of the size of the inputs.

# Logarithmic Complexity
# Complexity grows as the log of at least one of the inputs.
# E.g. binary search covered in next chapter.
def int_to_str(i):
    """Assumes i is a nonnegative int
       Returns a decimal string representation of i"""
    digits = '0123456789'
    if i == 0:
        return '0'
    result = ''
    while i > 0:
        result = digits[i%10] + result
        i = i // 10
    return result

int_to_str(1333749)

def add_digits(n):
    """Assumes n is a nonnegative int
       Returns the sum of the digits in n"""
    string_rep = int_to_str(n)
    val = 0
    for c in string_rep:
        val += int(c)
    return val

add_digits(1333749)

# Linear Complexity
# Many algorithms that deal with lists or sequences are linear.
# They touch each element of the sequence a constant number of times.

def add_digits_linear(s):
    """Assumes s is a str each character of which is a decimal
       digit. Returns an int that is the sum of the digits in s."""
    val = 0
    for c in s:
        val += int(c)
    return val

def factorial(x):
    """Assumes that x is a postive int
       Returns x!"""
    if x == 1:
        return 1
    else:
        return x * factorial(x - 1)

# Log-Linear Complexity
# Merge sort algorithm is an example and looked at in next chapter.

# Polynomial Complexity
# Most common polynomial algorithms are quadratic.
def is_subset(L1, L2):
    """Assumes L1 and L2 are lists.
       Returns True if each element in L1 is also in L2
       and False otherwise."""
    for e1 in L1:
        matched = False
        for e2 in L2:
            if e1 == e2:
                matched = True
                break
        if not matched:
            return False
    return True
# complexity of is_subset is O(len(L1)*Len(L2))

def intersect(L1, L2):
    """Assumes: L1 and L2 are lists
       Returns a list without duplicates that is the intersection
       of L1 and L2"""
       # Build a list containing common elements
    tmp = []
    for e1 in L1:
        for e2 in L2:
           if e1 == e2:
               tmp.append(e1)
               break
    # Build a list without duplicates
    result = []
    for e in tmp:
        if e not in result:
            result.append(e)
    return result
# First part building the list that might contain duplicates is
# O(len(L1)*len(L2)). The second part is NOT linear since 
# e not in result potentially involves looking at each element
# in result, hence is O(len(tmp)*len(result)); however
# len(result) and len(tmp) are bounded by the min(len(L1), len(L2))
# Therefore complexity of intersect is O(len(L1) * len(L2))

# Exponential Complexity
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

#gen_powerset(['a','b','c','d','e','f','g','h','i','j'])
#gen_powerset(['a','b','c','d','e','f','g','h','i','j',
#              'k','l','m','n','o','p','q','r','s','t'])
#gen_powerset(['a','b','c','d','e','f','g','h','i','j',
#              'k','l','m','n','o','p','q','r','s','t',
#              'u','v','w','x','y','z'])
# exponential in len(L)

# Comparison of Complexity Classes
# This section in the text provides plots to examine algorithms
# in various complexity classes.