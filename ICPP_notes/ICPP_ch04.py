# -*- coding: utf-8 -*-
"""
ICPP Chapter 4
Functions, Scoping, and Abstraction
@author: Daniel J. Vera, Ph.D.
"""
#%% Functions and Scoping ==================================================

# Function Definitions
def max_val(x, y):
    if x > y:
        return x
    else: 
        return y

max_val(3, 4)
#%% Finger Exercise: Write a function isIn that accepts two strings as 
# arguments and returns True if either string occurs anywhere in the other
# and False otherwiswe. Hint: you may want to use the built-in str operation
# in.
def is_in(string1, string2):
    if string1 in string2:
        return True
    elif string2 in string1:
        return True
    else:
        return False

# Keyword Arguments and Default Values
def print_name(first_name, last_name, reverse):
    if reverse:
        print(last_name + ", " + first_name)
    else:
        print(first_name, last_name)

print_name('Olga', 'Puchmajerova', False)
print_name('Olga', 'Puchmajerova', reverse=False)
print_name('Olga', last_name='Puchmajerova', reverse=False)
print_name(last_name='Puchmajerova', first_name='Olga',
           reverse = False)
# following throws error: 
#   print_name('Olga', last_name='Puchmajerova', False)

#%%
def print_name(first_name, last_name, reverse = False):
    if reverse:
        print(last_name + ", " + first_name)
    else:
        print(first_name, last_name)

print_name('Olga', 'Puchmajerova')
print_name('Olga', 'Puchmajerova', True)
print_name('Olga', 'Puchmajerova', reverse=True)

#%% Scoping
def f(x): # name x used as formal parameter
    y = 1
    x = x + y
    print('x =', x)
    return x

x = 3
y = 2
z = f(x) # value of x used as actual parameter
print('z =', z)
print('x =', x)
print('y =', y)

#%%
def f(x):
    def g():
        x = 'abc'
        print('x =', x)
    def h():
        z = x
        print('z =', z)
    x = x + 1
    print('x =', x)
    h()
    g()
    print('x =', x)
    return g

x = 3
z = f(x)
print('x =', x)
print('z = ', z)
z()
#%% Specifications =========================================================
def find_root(x, power, epsilon):
    """Assumes x and epsilon int or float, power an int, epsilon > 0 & 
    power >= 1. Returns float y such that y**power is within epsilon of x.
    If such a float does not exist, it returns None"""
    
    if x < 0 and power % 2 == 0: # Negative number has no even-powered roots
        return None
    
    low = min(-1.0, x)
    high = max(1.0, x)
    ans = (high + low) / 2.0
    
    while abs(ans**power - x) >= epsilon:
        if ans**power < x:
            low = ans
        else:
            high = ans
        ans = (high + low) / 2.0
    
    return ans

def test_find_root():
    epsilon = 0.0001
    for x in [0.25, -0.25, 2, -2, 8, -8]:
        for power in range(1,4):
            print('Testing x =', str(x), 'and power = ', power)
            result = find_root(x, power, epsilon)
            if result == None:
                print('    No root')
            else:
                print('    ', result**power, '~=', x)
    
#%% Recursion ==============================================================
def iterative_factorial(n):
    """Assumes n an int > 0
       Returns n!"""
    result = 1
    while n > 1:
        result = result * n
        n -= 1
    return result

def recursive_factorial(n):
    """Assumes n an int > 0
       Returns n!"""
    if n == 1:
        return n
    else:
        return n * recursive_factorial(n - 1)

#%% Fibonacci Numbers
def fib(n):
    """Assumes n int >= 0. Returns Fibonacci of n"""
    if n == 0 or n == 1:
        return 1
    else: 
        return fib(n - 1) + fib(n - 2)

def test_fib(n):
    for i in range(n+1):
        print('fib of', i, '=', fib(i))

# Finger exercise: When the implementation of fib in Figure 4.7 is used to 
# compute fib(5), how many times does it compute the value of fib(2) on the 
# way to computing fib(5)?

# Draw a "tree" and count. It computes fib(2) a total of 3 times.

#%% Palindromes
def is_palindrome(s):
    """Assumes s is a str. Returns True if letters in s form a palindrome;
       False otherwise. Non-letters and capitaization are ignored."""
    def to_chars(s):
        s = s.lower()
        letters = ''
        for c in s:
            if c in 'abcdefghijklmnopqrstuvwxyz':
                letters = letters + c
        return letters
    
    def is_pal(s):
        if len(s) <= 1:
            return True
        else:
            return s[0] == s[-1] and is_pal(s[1:-1])
    
    return is_pal(to_chars(s))
#%%
def is_palindrome_viz(s):
    """Assumes s is a str. Returns True if is a palindrome; False otherwise.
       Punctuation makrs, blanks, and capitlization are ignored."""
       
    def to_chars(s):
        s = s.lower()
        letters = ''
        for c in s:
            if c in 'abcdefghijklmnopqrstuvwxyz':
                letters = letters + c
        return letters
    
    def is_pal(s):
        print(' is_pal called with', s)
        if len(s) <= 1:
            print('   About to return True from base case')
            return True
        else:
            answer = s[0] == s[-1] and is_pal(s[1:-1])
            print('   About to return', answer, 'for', s)
            return answer
    
    return is_pal(to_chars(s))

def test_is_palindrome_viz():
    print('Try dogGod')
    print(is_palindrome_viz('dogGod'))
    print('Try doGood')
    print(is_palindrome_viz('doGood'))
    
#%% Global Variables =======================================================
def fib2(x):
    """Assumes x an int >= 0. Returns Fibonacci of x"""
    global num_fib_calls
    num_fib_calls += 1
    if x == 0 or x == 1:
        return 1
    else:
        return fib(x-1) + fib(x-2)
    
def test_fib2(n):
    for i in range(n+1):
        global num_fib_calls
        num_fib_calls = 0
        print('fib of', i, '=', fib(i))
        print('fib called', num_fib_calls, 'times.')

#%% Modules ================================================================
# Suppose following were in a module called circle.py
pi = 3.14159

def area(radius):
    return pi * (radius**2)

def circumference(radius):
    return 2 * pi * radius

def sphere_surface(radius):
    return 4.0 * area(radius)

def sphere_volume(radius):
    return (4.0 / 3/0) * pi * (radius**3)

# we could then have the following code:
#import circle
#pi =3
#print(pi)
#print(circle.pi)
#print(circle.area(3))
#print(circle.curcumference(3))
#print(circle.sphere_surface(3))

#%% Files ==================================================================
name_handle = open('kids', 'w')
for i in range(2):
    name = input('Enter name: ')
    name_handle.write(name + '\n')
name_handle.close()

name_handle = open('kids', 'r')
for line in name_handle:
    print(line)
name_handle.close()

name_handle = open('kids','a')
name_handle.write('David\n')
name_handle.write('Mandy\n')
name_handle.close() 
name_handle = open('kids','r')
for line in name_handle:
    print(line[:-1])
name_handle.close()

    
