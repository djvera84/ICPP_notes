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
#%% Approximate Solutions and Bisection Search =============================
number = 25
epsilon = 0.01
step = epsilon**2
num_guesses = 0
ans = 0.0

while abs(ans**2 - number) >= epsilon and ans <= number:
    ans += step
    num_guesses += 1

print('num_guesses = ', num_guesses)

if abs(ans**2 - number) >= epsilon:
    print('Failed on square root of', number)
else:
    print(ans, 'is close to the square root of', number)
#%%
number = 123456
epsilon = 0.01
step = epsilon**2
num_guesses = 0
ans = 0.0

while abs(ans**2 - number) >= epsilon and ans*ans <= number:
    ans += step
    num_guesses += 1

print('num_guesses = ', num_guesses)

if abs(ans**2 - number) >= epsilon:
    print('Failed on square root of', number)
else:
    print(ans, 'is close to the square root of', number)
#%%
# this takes a while :)
number = 123456
epsilon = 0.01
step = epsilon**3
num_guesses = 0
ans = 0.0

while abs(ans**2 - number) >= epsilon and ans*ans <= number:
    ans += step
    num_guesses += 1

print('num_guesses = ', num_guesses)

if abs(ans**2 - number) >= epsilon:
    print('Failed on square root of', number)
else:
    print(ans, 'is close to the square root of', number)
#%%
number = 25
epsilon = 0.01
num_guesses = 0
low = 0.0
high = max(1.0, number)
ans = (high + low) / 2.0

while abs(ans**2 - number) >= epsilon:
    print('low =', low, 'high =', high, 'ans =', ans)
    num_guesses += 1
    if ans**2 < number:
        low = ans
    else:
        high = ans
    ans = (high + low) / 2.0


print('num_guesses = ', num_guesses)
print(ans, 'is close to the square root of', number)
#%%
number = 123456
epsilon = 0.01
num_guesses = 0
low = 0.0
high = max(1.0, number)
ans = (high + low) / 2.0

while abs(ans**2 - number) >= epsilon:
    print('low =', low, 'high =', high, 'ans =', ans)
    num_guesses += 1
    if ans**2 < number:
        low = ans
    else:
        high = ans
    ans = (high + low) / 2.0


print('num_guesses = ', num_guesses)
print(ans, 'is close to the square root of', number)
#%%
number = 123456789
epsilon = 0.01
num_guesses = 0
low = 0.0
high = max(1.0, number)
ans = (high + low) / 2.0

while abs(ans**2 - number) >= epsilon:
    print('low =', low, 'high =', high, 'ans =', ans)
    num_guesses += 1
    if ans**2 < number:
        low = ans
    else:
        high = ans
    ans = (high + low) / 2.0


print('num_guesses = ', num_guesses)
print(ans, 'is close to the square root of', number)
#%% Finger Exercise: What would the code in Figure 3.4 do if the statement 
# x = 25 were replaced by x = -25?
number = -25
epsilon = 0.01
num_guesses = 0
low = 0.0
high = max(1.0, number)
ans = (high + low) / 2.0

while abs(ans**2 - number) >= epsilon:
    print('low =', low, 'high =', high, 'ans =', ans)
    num_guesses += 1
    if ans**2 < number:
        low = ans
    else:
        high = ans
    ans = (high + low) / 2.0


print('num_guesses = ', num_guesses)
print(ans, 'is close to the square root of', number)
# run an infinite loop: the while statement is subtracting -25 from smaller
# numbers so will always be >= epsilon

#%% Finger Exercise: What would have to be changed to make the code in
# Figure 3.4 work for finding an approximation to the cube root of both 
# negative and positive numbers? (Hint: think about changing low to 
# ensure that the answer lies within the region being searched.)
number = -27
epsilon = 0.01
num_guesses = 0
low = min(number, 0.0)
high = max(1.0, number)
ans = (high + low) / 2.0

while abs(ans**3 - number) >= epsilon:
    print('low =', low, 'high =', high, 'ans =', ans)
    num_guesses += 1
    if ans**3 < number:
        low = ans
    else:
        high = ans
    ans = (high + low) / 2.0


print('num_guesses = ', num_guesses)
print(ans, 'is close to the cube root of', number)

#%% A Few Words About using Floats =========================================
x = 0.0

for i in range(10) :
    x = x + 0.1

if x == 1.0:
    print(x, '= 1.0')
else:
    print(x, "is not 1.0")
    
# Finger Exercise: What is the decimal equivalent of the binary number 
# 10011?

# 10011 = 1*2^4 + 0*2^3 + 0*2^2+ 1*2^1 + 1*2^0 =  16 + 2 + 1 = 19

#%% Newton-Raphson =========================================================
# Newton-Raphson for Square Root
# Find x such that x**2 - 24 is within epsilon of 0
epsilon = 0.01
k = 24.0
guess = k / 2.0

while abs(guess*guess - k) >= epsilon:
    guess = guess - (((guess**2) - k) / (2 * guess))
print('Square root of', k, 'is about', guess)

# Finger Exercise: Add some code to the implementation of Newton-Raphson
# that keeps track of the number of iterations use to find the root.
# Us that code as part of a program that comapres the efficiency of
# Newton-Raphson and bisection search. (You should discover 
# Newton-Raphson is more efficient.)

epsilon = 0.01
k = 24.0
guess = k / 2.0
step = 0

while abs(guess*guess - k) >= epsilon:
    guess = guess - (((guess**2) - k) / (2 * guess))
    step += 1
print('Square root of', k, 'is about', guess)
print("Newton Raphson found answer in", step, "steps.")


num_guesses = 0
low = 0.0
high = max(1.0, k)
ans = (high + low) / 2.0

while abs(ans**2 - k) >= epsilon:
    num_guesses += 1
    if ans**2 < k:
        low = ans
    else:
        high = ans
    ans = (high + low) / 2.0
print(ans, 'is close to the square root of', k)
print('Bisection search found answer in', num_guesses, "steps")

print("\nSummary: \nNR Steps:", step, "\nBS Steps:", num_guesses)