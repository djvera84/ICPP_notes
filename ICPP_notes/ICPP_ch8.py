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
        """Assumes birthday is of type datetime.date
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

#%% Inheritance ============================================================
class MITPerson(Person):
    
    next_id_num = 0 # identification number
    
    def __init__(self, name):
        Person.__init__(self, name)
        self.id_num = MITPerson.next_id_num
        MITPerson.next_id_num += 1
        
    def get_id_num(self):
        return self.id_num
    
    def __lt__(self, other):
        return self.id_num < other.id_num
    # added in next section on multiple levels of inheritance
    def is_student(self):
        return isinstance(self, Student)
    

p1 = MITPerson('Barbara Beaver')
print(str(p1) + '\'s id number is ' + str(p1.get_id_num()))
#%%
p1 = MITPerson('Mark Guttag')
p2 = MITPerson('Billy Bob Beaver')
p3 = MITPerson('Billy Bob Beaver')
p4 = Person('Billy Bob Beaver')

print('p1 < p2 =', p1 < p2)
print('p3 < p2 =', p3 < p2)
print('p4 < p1 =', p4 < p1)

print('p1 < p4 =', p1 < p4)

#%% Multiple Levels of Inheritance
class Student(MITPerson):
    pass


class UG(Student):
    
    def __init__(self, name, class_year):
        MITPerson.__init__(self, name)
        self.year = class_year
    
    def get_class(self):
        return self.year
    

class Grad(Student):
    pass


p5 = Grad('Buzz Aldrin')
p6 = UG('Billy Beaver', 1984)
print(p5, 'is a graduate student is', type(p5) == Grad)
print(p5, 'is an undergraduate student is', type(p5) == UG)

isinstance([1,2], list)

#%%
print(p5, 'is a student is', p5.is_student())
print(p6, 'is a student is', p6.is_student())
print(p3, 'is a student is', p3.is_student())

#%% Encapsulation and Information Hiding ===================================
class Grades(object):
    def __init__(self):
        """Create empty grade book"""
        self.students = []
        self.grades = {}
        self.is_sorted = True
        
    def add_student(self, student):
        """Assumes: student is of type Student
           Add student to the grade book"""
        if student in self.students:
            raise ValueError('Duplicate student')
        self.students.append(student)
        self.grades[student.get_id_num()] = []
        self.is_sorted = False
    
    def add_grade(self, student, grade):
        """Assumes: grade is a float
           Add grade to the list of grades for student"""
        try:
            self.grades[student.get_id_num()].append(grade)
        except:
            raise ValueError('Student not in mapping')
            
    def get_grades(self, student):
        """Return a list of grades for student"""
        try: # return copy of list of student's grades
            return self.grades[student.get_id_num()][:]
        except:
            raise ValueError('Student not in mapping')
    
    def get_students(self):
        """Return a sorted list of the students in the grade book"""
        if not self.is_sorted:
            self.students.sort()
            self.is_sorted = True
        return self.students[:] # return a copy of list of students
   


def grade_report(course):
    """Assumes course is of type Grades"""
    report = ''
    for s in course.get_students():
        tot = 0.0
        num_grades = 0
        for g in course.get_grades(s):
            tot += g
            num_grades += 1
        try:
            average = tot/num_grades
            report = report + '\n'\
                            + str(s) + '\'s mean grade is ' + str(average)
        except ZeroDivisionError:
            report = report + '\n'\
                     + str(s) + ' has no grades'
    return report

ug1 = UG('Jane Doe', 2014)
ug2 = UG('John Doe', 2015)
ug3 = UG('David Henry', 2003)
g1 = Grad('Billy Buckner')
g2 = Grad('Bucky F. Dent')
six_hundred = Grades()
six_hundred.add_student(ug1)
six_hundred.add_student(ug2)
six_hundred.add_student(g1)
six_hundred.add_student(g2)

for s in six_hundred.get_students():
    six_hundred.add_grade(s, 75)
   
six_hundred.add_grade(g1, 25)
six_hundred.add_grade(g2, 100)
six_hundred.add_student(ug3)
print(grade_report(six_hundred))
#%%


class infoHiding(object):
    def __init__(self):
        self.visible = 'Look at me'
        self.__also_visible__ = 'Look at me too'
        self.__invisible = 'Don\'t look at me directly'
        
    def print_visible(self):
        print(self.visible)
    
    def print_invisible(self):
        print(self.__invisible)
        
    def __print_invisible(self):
        print(self.__invisible)
    
    def __print_invisible__(self):
        print(self.__invbisible)


test = infoHiding()
print(test.visible)
print(test.__also_visible__)
print(test.__invisible)
#%%
test = infoHiding()
test.print_invisible()
test.__print_invisible__()
test.__print_invisible()
#%%


class subClass(infoHiding):
    def __init__(self):
        print('from subclass', self.__invisible)


test = subClass()

#%% Generators
class BetterGrades(object):
    def __init__(self):
        """Create empty grade book"""
        self.students = []
        self.grades = {}
        self.is_sorted = True
        
    def add_student(self, student):
        """Assumes: student is of type Student
           Add student to the grade book"""
        if student in self.students:
            raise ValueError('Duplicate student')
        self.students.append(student)
        self.grades[student.get_id_num()] = []
        self.is_sorted = False
    
    def add_grade(self, student, grade):
        """Assumes: grade is a float
           Add grade to the list of grades for student"""
        try:
            self.grades[student.get_id_num()].append(grade)
        except:
            raise ValueError('Student not in mapping')
            
    def get_grades(self, student):
        """Return a list of grades for student"""
        try: # return copy of list of student's grades
            return self.grades[student.get_id_num()][:]
        except:
            raise ValueError('Student not in mapping')
    
    # better version of get_students
    def better_get_students(self):
        """Return a sorted list of the students in the grade book
           one at a time in alphabetical order"""
        if not self.is_sorted:
            self.students.sort()
            self.is_sorted = True
        for s in self.students:
            yield s


book = BetterGrades()
book.add_student(Grad('Julie'))
book.add_student(Grad('Charlie'))
for s in book.better_get_students():
    print(s)

#%% Mortgages, an Extended Example =========================================
def find_payment(loan, r, m):
    """Assumes: loan and r are floats, m an int
       Returns the monthly payment for a mortgage of size
       loan at a monthly rate of r for m months"""
    return loan * ((r * (1 + r)**m) / ((1 + r)**m - 1))

# Abstract class is a class that contains methods shared by each subclass
# but it not intended to be instantiated directly.
class Mortgage(object):
    """Abstract class for building different kinds of mortgages"""
    def __init__(self, loan, ann_rate, months):
        """Assumes: loan and ann_rate are floats, months an int
           Creates a new mortgage of size loan, duration months, and
           annual reate ann_rate"""
        self.loan = loan
        self.rate = ann_rate / 12
        self.months = months
        self.paid = [0.0]
        self.outstanding = [loan]
        self.payment = find_payment(loan, self.rate, months)
        self.legend = None # description of mortgage.
    
    def make_payment(self):
        """Make a payment"""
        self.paid.append(self.payment)
        reduction = self.payment - self.outstanding[-1] * self.rate
        self.outstanding.append(self.outstanding[-1] - reduction)
    
    def get_total_paid(self):
        """Return the total amount paid so far"""
        return sum(self.paid)
    
    def __str__(self):
        return self.legend


class Fixed(Mortgage):
    def __init__(self, loan, r, months):
        Mortgage.__init__(self, loan, r, months)
        self.legend = 'Fixed, ' + str(round(r*100, 2)) + '%'


class FixedWithPts(Mortgage):
    def __init__(self, loan, r, months, pts):
        Mortgage.__init__(self, loan, r, months)
        self.pts = pts
        self.paid = [loan * (pts/100)]
        self.legend = 'Fixed, ' + str(round(r*100, 2)) + '%, '\
                      + str(pts) + ' points'


class TwoRate(Mortgage):
    def __init__(self, loan, r, months, teaser_rate, teaser_months):
        Mortgage.__init__(self, loan, teaser_rate, months)
        self.teaser_months = teaser_months
        self.teaser_rate = teaser_rate
        self.next_rate = r / 12
        self.legend = str(teaser_rate * 100)\
                     + '% for ' + str(self.teaser_months)\
                     + ' months, then ' + str(round(r*100, 2)) + '%'

    def make_payment(self):
        if len(self.paid) == self.teaser_months + 1:
            self.rate = self.next_rate
            self.payment = find_payment(self.outstanding[-1],
                                        self.rate,
                                        self.months - self.teaser_months)
        Mortgage.make_payment(self)


def compare_mortgages(amt, years, fixed_rate, pts, pts_rate, 
                      var_rate1, var_rate2, var_months):
    tot_months = years * 12
    fixed1 = Fixed(amt, fixed_rate, tot_months)
    fixed2 = FixedWithPts(amt, pts_rate, tot_months, pts)
    two_rate = TwoRate(amt, var_rate2, tot_months, var_rate1, var_months)
    morts = [fixed1, fixed2, two_rate]
    for m in range(tot_months):
        for mort in morts:
            mort.make_payment()
    for m in morts:
        print(m)
        print(' Total payments = $' + str(int(m.get_total_paid())))

compare_mortgages(amt=200000, years=30, fixed_rate=0.07,
                  pts=3.25, pts_rate=0.05, var_rate1=0.045,
                  var_rate2=0.095, var_months=48)