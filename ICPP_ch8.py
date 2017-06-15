# -*- coding: utf-8 -*-
"""
ICPP Chapter 8
Classes and Object-Oriented Programming
@author: Daniel J. Vera, Ph.D.
"""
#%% Abstract Data Types and Classes ========================================
class IntSet(object):
    """An IntSet is a set of integers"""
    # Information about the implenetation (not the abstraction)
    # Value of the set is represented by a list of ints, self.vals.
    # Each in in the set occurs in self.vals exactly once.

    def __init__(self):
        """Create an empty set of integers"""
        self.vals = []
    
    def insert(self, e):
        """Assumes e is an integer and inserts e into self"""
        if e not in self.vals:
            self.vals.append(e)
            
    def member(self, e):
        """Assumes e is an integer
           Returns True if e is in self, False otherwise"""
        return e in self.vals
    
    def remove(self, e):
        """Assumes e is an integer and removes e from self
           Raises ValueError if e is not in self"""
        try:
            self.vals.remove(e)
        except:
            raise ValueError(str(e) + ' not found')
    
    def get_members(self):
        """Returns a list containing the elements of self.
        Nothing can be assumed about the order of the elements."""
        return self.vals[:]
    
    def __str__(self):
        """Returns a string representation of self"""
        self.vals.sort()
        result = ''
        for e in self.vals:
            result = result + str(e) + ','
        return '{' + result[:-1] + '}' #-1 omits trailing comma


print(type(IntSet), type(IntSet.insert))
# First line in the above class definition indicates that IntSet is a
# subclass of object.

a_set = IntSet()
a_set.insert(3)
print(a_set.member(3))
#%%
# When the print command is used, the __str__ function associated with
# the object to be printed is automatically invoked.
another_set = IntSet()
another_set.insert(3)
another_set.insert(4)
print(another_set)
#%% Designing Programs Using Abstract Data Types

#Data abstraction encourages program designers to focus on the centrality
#of data objects rather than functions. Thinking about a program more as 
#a collection of types than as a collection of functions leads to a 
#profoundly different organizing principle. Among other things, it 
#encourages one to think about programming as a process of combining 
#relatively large chunks, since data abstractions typically encompass 
#more functionality than do individual functions. This, in turn, leads us
#to think of the essence of programming as a process not of writing 
#individual lines of code, but of composing abstractions.

# Using Classes to Keep Track of Students and Faculty
import datetime


class Person(object):

    def __init__(self, name):
        """Create a person"""
        self.name = name
        try:
            last_blank = name.rindex(' ')
            self.last_name = name[last_blank+1:]
        except:
            self.last_name = name
        self.birthday = None
        
    def get_name(self):
        """Returns self's full name"""
        return self.name
    
    def get_last_name(self):
        return self.last_name
    
    def set_birthday(self, birthdate):
        """Assumes birthdaye is of type datetime.date
           Sets self's birthday to birthdate"""
        self.birthday = birthdate
        
    def get_age(self):
        """Returns self's currrent age in days"""
        if self.birthday == None:
            raise ValueError
        return(datetime.date.today() - self.birthday).days
    
    def __lt__(self, other):
        """Returns True if self precedes other in alphabetical
           order, and False otherwise. Comparison is based on last
           names, but if these are the same, full names are compared."""
        if self.last_name == other.last_name:
            return self.name < other.name
        return self.last_name < other.last_name
    
    def __str__(self):
        """Returns self's name"""
        return self.name


me = Person('Daniel Vera') # because I don't know Michael Guttag
him = Person('Barack Hussein Obama')
her = Person('Araceli')
print(him.get_last_name())
him.set_birthday(datetime.date(1961, 8, 4))
her.set_birthday(datetime.date(1986, 9, 5))
print(him.get_name(), 'is', him.get_age(), 'days old.')
#%%
p_list = [me, him, her]
for p in p_list:
    print(p)
p_list.sort()
for p in p_list:
    print(p)