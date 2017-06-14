# -*- coding: utf-8 -*-
"""
ICPP Chapter 7
Exceptions and Assertions
@author: Daniel J. Vera, Ph.D.
"""
#%% Handling Exceptions ====================================================
num_successes = 10
num_failures = 0 # play with 0 and non-zero values
try:
    success_failure_ratio = num_successes / num_failures
    print('The success/failure ratio is', success_failure_ratio)
except ZeroDivisionError:
    print('No failures, so the success/failure raio is undefined.')
print('Now here')

#%% Finger Exercise: Implement a function that meets the specification
# below. Use a try-except block.
def sum_digits(a_string): 
    """Assumes s is a string 
       Returns the sum of the decimal digits in s
       For example, if s is 'a2b3c' it returns 5"""
    string_sum = []
    for i in a_string:
        try:
            string_sum.append(int(i))
        except ValueError:
            continue
    if string_sum == []:
        return None
    else:
        return sum(string_sum)

print(sum_digits('a2b3c'))                 # should evaluate to 5
print(sum_digits('gshewrt3jdalkfi7'))      # should evaluate to 10
print(sum_digits('a5s1$#23+67pq489-'))     # should evaluate to 45
print(sum_digits(''))                      # should evaluate to None
print(sum_digits('abc') == None)           # should evaluate to True
print(sum_digits('7'))                     # should evaluate to 7
print(sum_digits('120'))                   # should evaluate to 3

#%%
# Following is bad
val = int(input('Enter an integer: '))
print('The square of the number you entered is', val**2)

# Instead we should handle the exception.
while True:
    val = input('Enter an integer: ')
    try:
        val = int(val)
        print('The square of the number you entered is', val**2)
        break # to exit the while loop
    except ValueError:
        print(val, 'is not an integer')

#%%
# Can encapsulate above code in a function as is but a better function
# is more general, for example:
def read_val(val_type, request_msg, error_msg):
    while True:
        val = input(request_msg + ' ')
        try:
            return(val_type(val)) # convert str to val_type before returning
        except ValueError:
            print(val, error_msg)

read_val(int, 'Enter an integer:', 'is not an integer')

# read_val is an example of a polymorphic function, i.e.
# it works for arguments of many different types.

#%% Exceptions as a Control Flow Mechanism =================================
#%% Finger Exercise: Implement a function that satisfies the specification
def find_an_even(L): 
    """Assumes L is a list of integers
       Returns the first even number in L
       Raises ValueError if L does not contain an even number"""
    for i in range(len(L)):
        try:
            if L[i] % 2 == 0:
                return L[i]
        except:
            raise ValueError
    raise ValueError

print(find_an_even([2,3]))          # should be 2
print(find_an_even([1,1,3,4,2]))    # should be 4
print(find_an_even([1,3,2,7]))      # should be 2

# find_an_even([])             # should raise ValueError
# find_an_even([7, 3, 5, 9])   # should raise ValueError
#%%
def get_ratios(vect1, vect2):
    """Assumes: vect1 and vect2 are equal length lists of numbers
       Returns: a list containing meaningful values of
               vect1[i] / vect2[i]"""
    ratios = []
    for index in range(len(vect1)):
        try:
            ratios.append(vect1[index] / vect2[index])
        except ZeroDivisionError:
            ratios.append(float('nan')) # nan = Not a Number
        except:
            raise ValueError('get_ratios called with bad arguments')
    return ratios

try:
    print(
            get_ratios(
                    [1.0, 2.0, 7.0, 6.0],
                    [1.0, 2.0, 0.0, 3.0]
                    )
            )
    print(get_ratios([],[]))
    print(get_ratios([1.0, 2.0], [3.0]))
except ValueError as msg:
    print(msg)