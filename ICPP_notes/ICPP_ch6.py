# -*- coding: utf-8 -*-
"""
ICPP Chapter 6
Testing and Debugging
@author: Daniel J. Vera, Ph.D.
"""
#%% Testing ================================================================
# def is_bigger(x, y):
#    """Assumes x and y are ints
#       Returns True if x is less than y and False
#       otherwise."""

# Test suite:
# 1. x > 0, y > 0
# 2. x > 0, y < 0
# 3. x < 0, y < 0
# 4. x < 0. y > 0
# 5. x = 0, y = 0
# 6. x = 0, y != 0
# 7. x != 0, y = 0

# Black-Box Testing

# def sqrt(x, epsilon):
#    """Assumes x, epsilon floats x >= 0 epsilon > 0 
#       Returns result such that 
#       x - epsilon < = result*result <= x + epsilon"""

def copy(L1, L2): 
    """ Assumes L1, L2 are lists Mutates L2 to be a copy of L1""" 
    while len(L2) > 0: #remove all elements from L2 
        L2.pop() #remove last element of L2 
    for e in L1: #append L1' s elements to initially empty L2 
        L2.append(e) 

# Above works most of the time, but not when L1 and L2 refer 
# to the same list. Remember cloning! Something like this can help:
# if L1 == L2, L2 = L2[:]

# Glass-box Testing
def is_prime(x): 
    """Assumes x is a nonnegative int 
       Returns True if x is prime; False otherwise""" 
    if x < = 2:
        return False 
    for i in range(2, x):
        if x % i == 0: 
            return False 
    return True
# Examing code, we see 0, 1, and 2 are special cases and need to be tested.
# Function has bug because is_prime(2) evaluates erroneously to False!

def abs(x): 
    """Assumes x is an int 
       Returns x if x >= 0 and –x otherwise"""
    if x < -1: 
        return -x 
    else: 
        return x
# bug: abs(-1) returns -1.

# Rules of Thumb
# 1. Exercise both branches of all if statements
# 2. Make sure that each except clause is executed (chapter 7 ICPP)
# 3. For each for loop, have test cases in which
#           i.   The loop is not entered (e.g. test on empty list)
#           ii.  The body of loop executed exactly once
#           iii. The body of the loop is executed more than once.
#4. For each while loop:
#           i.  Same as foor loops above
#           ii.  Look at all ways of exiting loop
# 
# For recursive functions, include test cases that cause function
# to return with no recursive calls, exactly one call, and more than one.

#%% Debugging
def is_pal(x):
    """Assumes xi is a list
       Returns True if the list is palindrome; False otherwise"""
    temp = x
    temp.reverse
    if temp == x:
        return True
    else:
        return False
    
def silly_bug(n):
    """Assumes n is an int > 0
       Gets n inputs from user
       Prints 'Yes' if the sequence of inputs forms palindrome;
       'No' otherwise"""
    for i in range(n):
        result = []
        elem = input('Enter element: ')
        result.append(elem)
    if is_pal(result):
        print('Yes')
    else:
        print('No')
       
silly_bug(2)

#%%
def fixing_silly_bug(n):
    """Assumes n is an int > 0
       Gets n inputs from user
       Prints 'Yes' if the sequence of inputs forms palindrome;
       'No' otherwise"""
    for i in range(n):
        result = []
        elem = input('Enter element: ')
        result.append(elem)
    print(result) # first test
    if is_pal(result):
        print('Yes')
    else:
        print('No')
        
fixing_silly_bug(2)

#%%
def fixing_silly_bug(n):
    """Assumes n is an int > 0
       Gets n inputs from user
       Prints 'Yes' if the sequence of inputs forms palindrome;
       'No' otherwise"""
    for i in range(n):
        result = []
        elem = input('Enter element: ')
        print(result) # second test   
        result.append(elem)
    print(result) # first test
    if is_pal(result):
        print('Yes')
    else:
        print('No')
        
fixing_silly_bug(2)
#%%
def maybe_correct_silly(n): # hint: still not correct
    """Assumes n is an int > 0
       Gets n inputs from user
       Prints 'Yes' if the sequence of inputs forms palindrome;
       'No' otherwise"""
    result = []
    for i in range(n):
        elem = input('Enter element: ')      
        result.append(elem)
    print(result) # first test
    if is_pal_fix(result): # see below
        print('Yes')
    else:
        print('No')
        
maybe_correct_silly(2)

#%% 
def is_pal_fix(x):
    """Assumes xi is a list
       Returns True if the list is palindrome; False otherwise"""
    temp = x
    print(temp, x) # fourth test
    temp.reverse()
    print(temp, x) # third test
    if temp == x:
        return True
    else:
        return False
#%% After foruth test, should see that there is no () after reverse
# After we would see an aliasing bug on line 161 in above. Here is the fix:
def correct_silly(n): # hint: still not correct
    """Assumes n is an int > 0
       Gets n inputs from user
       Prints 'Yes' if the sequence of inputs forms palindrome;
       'No' otherwise"""
    result = []
    for i in range(n):
        elem = input('Enter element: ')      
        result.append(elem)
    if is_pal_fixed(result):
        print('Yes')
    else:
        print('No')

def is_pal_fixed(x):
    """Assumes xi is a list
       Returns True if the list is palindrome; False otherwise"""
    temp = x[:]
    temp.reverse()
    if temp == x:
        return True
    else:
        return False

correct_silly(2)