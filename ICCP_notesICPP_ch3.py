# -*- coding: utf-8 -*-
"""
ICPP Chapter 3
Some Simple Numerical Programs
@author: Daniel J. Vera, Ph.D.
"""
#%% Exhaustive Enumeration =================================================
x = int(input('Enter an integer: '))
ans = 0

while ans**3 < abs(x):
    #print('Value of the decrementing function abs(x) - ans**3 is',
    #      abs(x) - ans**3)    
    ans += 1

if ans**3 != abs(x):
    print(x, "is not a perfect cube.")
else:
    if x < 0:
        ans = -ans
    print('Cube root of', x, 'is', ans)
# 'decrementing function' for loop above is abs(x) - ans**3
#%%
max_value = int(input('Enter a positive integer: '))
i = 0

while i < max_value:
    i += 1
print(i)

#%% Finger Exercise: Write a program that asks the user to enter an integer
# and prints two integers, root and pwr, such that 0 < pwr < 6 and
# root**pwr is equal to the integer entered by the user. If no such pair of
# integers exists, it should print a message to that effect.

# Note that although the finger exercise says pwr is can be 1, 2, ..., 6
# clearly every integer is the '1-th' power of itself so we start modify
# to say 1 < pwr < 6
x = int(input('Enter an integer: '))
root = 0    # root has to be < x 
pwr = 2     # 1 < pwr < 6

# idea is to 'nest' while loops and check every iteration of pwr, i.e.
# pwr = 1, 2, ..., 6
while pwr < 7:
    while root**pwr < abs(x):
        root += 1
    if root**pwr == abs(x):        
        break
    root = 0 # reset the root and try again
    pwr += 1

if x < 0:
    root = -root
    if root**pwr != x:
        print("No such integers.")
    else:
        print("(", root, ")", '^', pwr, '=', x)
elif root**pwr != x:
    print("There is no", pwr, "root of", x)
else: 
    print("(", root, ")", '^', pwr, '=', x)
    
#%% For Loops ==============================================================
x = 4

for i in range(0, x):
    print(i)
#%%
x = 4
for i in range(0, x):
    print(i)
    x = 5
#%%
x = 4
for j in range(x):
    for i in range(x):
        print(i)
        x = 2
#%%
# Find the cube root of a perfect cube
x = int(input('Enter an integer: '))
for ans in range(abs(x) + 1):
    if ans**3 >= abs(x):
        break
if ans**3 != abs(x):
    print(x, 'is not a perfect cube.')
else:
    if x < 0:
        ans = -ans
    print('Cube root of', x, 'is', ans)
#%%
total = 0
for c in '123456789':
    total = total + int(c)
print(total)

#%% Finger Exercise: Let s be a string that contains a sequence of decimal
# numbers seperated by commas, e.g., s = '1.23,2.4,3.123'. Write a prgram
# that prints the sum of the numbers in s.
total = 0
a_string = input(
    'Please type a sequence of decimal numbers seperated by commas: '
    )
numbers = a_string.split(',')
for c in numbers:
    total += float(c)
print(total)
