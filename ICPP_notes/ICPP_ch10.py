# -*- coding: utf-8 -*-
"""
ICPP Chapter 10
Some Simple Algorithms and Data Structures
@author: Daniel J. Vera, Ph.D.
"""
#%% Search Algorithms ======================================================
# e in L
# def search(L, e):
#     """Assumes L is a list.
#        Returns True if e is in L and False otherwise."""

# Linear Search and Using Indirection to Access Elements
# Python uses the following algorithm to determine if an element is in a
# list:

# for i in range(len(L)):
#    if L[i] == e:
#        return True
# return False

# Binary Search and Exploiting Assumptions

# First linear search of sorted:
def search(L, e):
    """Assumes L is a list, the elements of which are in ascending order.
       Returns True if e is in L and False otherwise"""
    for i in range(len(L)):
        if L[i] == e:
            return True
        if L[i] > e:
            return False
    return False

# Binary search has following idea:
# 1. Pick an index, i, that divides the list L roughly in half.
# 2. Ask if L[i] == e.
# 3. If not, as whehter L[i] is larger or smaller than e.
# 4. Depending upon the answer, search either the left or right half
# of L for e.

def binary_search_rec(L, e):
    """Assumes L is a list, the elemnets of which are in ascending order.
       Returns True if e is in L and False otherwise"""
    
    def b_search(L, e, low, high):
        # Decrements high - low
        if high == low:
            return L[low] == e
        mid = (low + high) // 2
        if L[mid] == e:
            return True
        elif L[mid] > e:
            if low == mid: # nothing left to search
                return False
            else:
                return b_search(L, e, low, mid -1)
        else:
            return b_search(L, e, mid + 1, high)
        
    if len(L) == 0:
        return False
    else:
        return b_search(L, e, 0, len(L) - 1)

#%% Finger Exercise: Why does the code use mid + 1 rather than mid
# in the second recursive call?

# mid gets checked in previous line of code; if L[mid] > e
# we check everything before that (we know already its not equal based
# on the control flow). If L[mid] > e is false, we know we don't have
# to check anything before the mid index so start at mid + 1

#%% Sorting Algorithms =====================================================
# Python implementations to sort run in roughly log-linear time so most of 
# the time, the right thing to do is use either L.sort() which sorts the
# list L or sorted(L) which returns a list with the same elements as L,
# sorted, and does not mutate L. This section is primarily for practice.

# Selection Sort

# "Prefix Sorted L[0, i], suffix L[i+1,len(L)] whose smallest element
# is larger than all elements in prefix.

# Base Case: At start of first iteration, prefix is empty, suffix is
# entire list.
# Induction step: move one element from the suffix to the prefix.
# Append minimum element of suffic to end of prefix.
# Termination: When loop is exited, prefix includes entire list and
# suffix is empty.

def sel_sort(L):
    """Assumes that L is a list of elements that can be compared
       using >. Sorts L in ascending order"""
    suffix_start = 0
    while suffix_start != len(L):
        # look at each element in suffix
        for i in range(suffix_start, len(L)):
            if L[i] < L[suffix_start]:
                #swap position of elements
                L[suffix_start], L[i] = L[i], L[suffix_start]
        suffix_start += 1
# complexity of sel_sort is O(len(L)**2), quadratic in length of L.

# Merge Sort
# Divide and conquer algorithm:
# 1. Threshold input size, below which problem is not subdivided
# 2. Size and number of sub-instances into which instance is split
# 3. Algorithm used to combine sub-solutions.
# Threshold is sometimes called recursive base.

def merge(left, right, compare):
    """Assumes left and right are sorted lists and 
       compare defines an ordering on the elements.
       Returns a new sorted (by compare) list containing
       the same elements as (left + right) would contain."""
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if compare(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while (i < len(left)) :
        result.append(left[i])
        i += 1
    while (j < len(right)):
        result.append(right[j])
        j += 1
    return result

def merge_sort(L, compare = lambda x, y: x < y):
    """Assumes L is a list, compare defines an ordering
       on elements of L.
       Returns a new sorted list with the same elements as L"""
    if len(L) < 2:
        return L[:]
    else:
        middle = len(L) // 2
        left = merge_sort(L[:middle], compare)
        right = merge_sort(L[middle:], compare)
        return merge(left, right, compare)

print(merge_sort([1, 5, 12, 18, 19, 20, 2, 3, 4, 17]))
L = [2, 1, 4, 5, 3]
print(merge_sort(L), merge_sort(L, lambda x, y: x > y))
# complexity of merge_sort is log-linear.

# Exploiting Functions as Parameters
def last_name_first_name(name1, name2):
    arg1 = name1.split(' ')
    arg2 = name2.split(' ')
    if arg1[1] != arg2[1]:
        return arg1[1] < arg2[1]
    else: #last names the same, sort by first name
        return arg1[0] < arg2[0]

def first_name_last_name(name1, name2):
    arg1 = name1.split(' ')
    arg2 = name2.split(' ')
    if arg1[1] != arg2[1]:
        return arg1[0] < arg2[0]
    else: #first names the same, sort by last name
        return arg1[1] < arg2[1]

L =  ['Tom Brady', 'Eric Grimson', 'Gisele Bundchen']
new_L = merge_sort(L, last_name_first_name)
print('Sorted by last name =', new_L)
new_L = merge_sort(L, first_name_last_name)
print('Sorted by first name =', new_L)

# Sorting in Python
L = [3, 5, 2]
D = {'a':12, 'c':5, 'b':'dog'}
print(sorted(L))
print(L)
L.sort()
print(L)
print(sorted(D))
D.sort()
#%%
L = [[1, 2, 3], (3, 2, 1, 0), 'abc']
print(sorted(L, key = len, reverse = True))

#%% Hash Tables

#If we put merge sort together with binary search, we have a nice way to 
#search lists. We use merge sort to preprocess the list in O(n*log(n)) 
#time, and then we use binary search to test whether elements are in the 
#list in O(log(n)) time. If we search the list k times, the overall time 
#complexity is O(n*log(n) + k*log(n)).
#
#Guttag, John V.. Introduction to Computation and Programming Using Python


class intDict(object):
    """A dictionary with integer keys"""
    
    def __init__(self, num_buckets):
        """Create an empty dictionary"""
        self.buckets = []
        self.num_buckets = num_buckets
        for i in range(num_buckets):
            self.buckets.append([])
    
    def add_entry(self, key, dict_val):
        """Assumes key an int. Adds an entry."""
        hash_bucket = self.buckets[key%self.num_buckets]
        for i in range(len(hash_bucket)):
            if hash_bucket[i][0] == key:
                hash_bucket[i] = (key, dict_val)
                return
        hash_bucket.append((key, dict_val))

    def get_value(self, key):
        """Assumes key an int.
           Returns vlaue associated wtih key"""
        has_bucket = self.buckets[key%self.num_buckets]
        for e in  has_bucket:
            if e[0] == key:
                return e[1]
        return None
    
    def __str__(self):
        result = '{'
        for b in self.buckets:
            for e in b:
                result = result + str(e[0]) + ':' + str(e[1]) + ','
        return result[:-1] + '}' #result[:-1] omits last comma

import random
D = intDict(17)
for i in range(20):
    # choose a random in in the range 0 to 10**5 - 1
    key = random.choice(range(10**5))
    D.add_entry(key, i)
print('The value of the intDict is:')
print(D)
print('\n', 'The buckets are:')
for hash_bucket in D.buckets: # violates abstraction barrier
    print(' ' , hash_bucket)
            