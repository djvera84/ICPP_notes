# -*- coding: utf-8 -*-
"""
ICPP Chapter 14
Dynamic Programming
@author: Daniel J. Vera, Ph.D.
"""
import random
import pylab
#%% Random Walks ===========================================================
#%% The Drunkard's Walk ====================================================
# Types to implement: Location, Field, Drunk.
class Location(object):
    def __init__(self, x, y):
        """a and y are numbers"""
        self.x, self.y = x, y
        
    def move(self, delta_x, delta_y):
        """delta_x and delta_y are numbers"""
        return Location(self.x + delta_x, self.y + delta_y)
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def dist_from(self, other):
        ox, oy = other.x, other.y
        x_dist, y_dist = self.x - ox, self.y - oy
        return (x_dist**2 + y_dist**2)**0.5
    
    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'


class Field(object):
    def __init__(self):
        self.drunks = {}
        
    def add_drunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc
            
    def move_drunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        x_dist, y_dist = drunk.take_step()
        current_location = self.drunks[drunk]
        # use move method of Location to get new location
        self.drunks[drunk] = current_location.move(x_dist, y_dist)
    
    def get_loc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]


class Drunk(object):
    def __init__(self, name = None):
        """Assumes name is a str"""
        self.name = name
    
    def __str__(self):
        if self != None:
            return self.name
        return 'Anonymous'


class UsualDrunk(Drunk):
    def take_step(self):
        step_choices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return random.choice(step_choices)


def walk(f, d, num_steps):
    """Assumes: f a Field, d a Drunk in f, and num_steps an int >= 0.
       Move d num_steps times; returns the distance between the final
       location and the location at the start of the walk."""
    start = f.get_loc(d)
    for s in range(num_steps):
        f.move_drunk(d)
    return start.dist_from(f.get_loc(d))
    
def sim_walks(num_steps, num_trials, dClass):
    """Assumes num_steps an int >= 0, num_trials an int > 0,
       dClass a sublcass of Drunk
       Simulates num_trials walks of num_steps steps each.
       Returns a list of the final distances for each trial"""
    Homer = dClass()
    origin = Location(0, 0)
    distances = []
    for t in range(num_trials):
        f = Field()
        f.add_drunk(Homer, origin)
        distances.append(round(walk(f, Homer, num_steps), 1)) 
        # textbook put an intentional bug in line above with num_trials
        # instead of num_steps! Always be skepitcal of simulations!
    return distances


def drunk_test(walk_lengths, num_trials, dClass):
    """Assumes walk_lengths a sequence of ints >= 0
       num trials an int > 0, dClass a sublass of Drunk
       For each number of steps in walk_lengths, runs sim_walks with
       num_trails walks and prints results"""
    for num_steps in walk_lengths:
        distances = sim_walks(num_steps, num_trials, dClass)
        print(dClass.__name__, 'random walk of', num_steps, 'steps')
        print(' Mean =', round(sum(distances)/len(distances), 4))
        print(' Max =', max(distances), ' Min =', min(distances))
#%%
drunk_test((10, 100, 1000, 10000), 100, UsualDrunk)
#%%
drunk_test((0, 1), 100, UsualDrunk)
#%% Biased Random Walks ====================================================


class ColdDrunk(Drunk):
    def take_step(self):
        step_choices = [(0.0, 1.0), (0.0, -2.0), (1.0, 0.0),\
                        (-1.0, 0.0)]
        return random.choice(step_choices)


class EWDrunk(Drunk):
    def take_step(self):
        step_choices = [(1.0, 0.0), (-1.0, 0.0)]
        return random.choice(step_choices)

def sim_all(drunkKinds, walk_lengths, num_trials):
    for dClass in drunkKinds:
        drunk_test(walk_lengths, num_trials, dClass)
#%%
sim_all((UsualDrunk, ColdDrunk, EWDrunk), (100, 1000), 10)
#%%
class styleIterator(object):
    def __init__(self, styles):
        self.index = 0
        self.styles = styles
    
    def next_style(self):
        result = self.styles[self.index]
        if self.index == len(self.styles) - 1:
            self.index = 0
        else:
            self.index += 1
        return result


def sim_drunk(num_trials, dClass, walk_lengths):
    mean_distances = []
    for num_steps in walk_lengths:
        print('Starting simulation of', num_steps, 'steps')
        trials = sim_walks(num_steps, num_trials, dClass)
        mean = sum(trials) / len(trials)
        mean_distances.append(mean)
    return mean_distances

def sim_all1(drunkKinds, walk_lengths, num_trials):
    style_choice = styleIterator(('m-', 'r:', 'k-.'))
    for dClass in drunkKinds:
        cur_style = style_choice.next_style()
        print('Starting simulation of', dClass.__name__)
        means = sim_drunk(num_trials, dClass, walk_lengths)
        pylab.plot(walk_lengths, means, cur_style,
                   label = dClass.__name__)
    pylab.title('Mean Distance from Origin ('
                + str(num_trials) + ' trials)')
    pylab.xlabel('Number of Steps')
    pylab.ylabel('Distance from Origin')
    pylab.legend(loc = 'best')
    pylab.semilogx()
    pylab.semilogy()

sim_all1((UsualDrunk, ColdDrunk, EWDrunk),
         (10, 100, 1000, 10000, 100000), 100)
#%%

def get_final_locs(num_steps, num_trials, dClass):
    locs = []
    d = dClass()
    for t in range(num_trials):
        f = Field()
        f.add_drunk(d, Location(0, 0))
        for s in range(num_steps):
            f.move_drunk(d)
        locs.append(f.get_loc(d))
    return locs

def plot_locs(drunkKinds, num_steps, num_trials):
    style_choice = styleIterator(('k+', 'r^', 'mo'))
    for dClass in drunkKinds:
        locs = get_final_locs(num_steps, num_trials, dClass)
        x_vals, y_vals = [], []
        for loc in locs:
            x_vals.append(loc.get_x())
            y_vals.append(loc.get_y())
        mean_x = sum(x_vals) / len(x_vals)
        mean_y = sum(y_vals) / len(y_vals)
        cur_style = style_choice.next_style()
        pylab.plot(x_vals, y_vals, cur_style,
                   label = dClass.__name__ + 'mean loc. = <'
                   + str(mean_x) + ', ' + str(mean_y) + '>')
        pylab.title('Location at End of Walks ('
                    + str(num_steps) + ' steps)')
        pylab.xlabel('Steps East/West of Origin')
        pylab.ylabel('Steps North/South of Origin')
        pylab.legend(loc = 'lower left')

plot_locs((UsualDrunk, ColdDrunk, EWDrunk), 100, 200)
#%%
def trace_walk(drunkKinds, num_steps):
    style_choice = styleIterator(('k+', 'r^', 'mo'))
    f = Field()
    for dClass in drunkKinds:
        d = dClass()
        f.add_drunk(d, Location(0, 0))
        locs = []
        for s in range(num_steps):
            f.move_drunk(d)
            locs.append(f.get_loc(d))
        x_vals, y_vals = [], []
        for loc in locs:
            x_vals.append(loc.get_x())
            y_vals.append(loc.get_y())
        cur_style = style_choice.next_style()
        pylab.plot(x_vals, y_vals, cur_style,
                   label = dClass.__name__)
        pylab.title('Spots Visited on Walk ('
                    + str(num_steps) + ' steps)')
        pylab.xlabel('Steps East/West of Origin')
        pylab.ylabel('Steps North/South of Origin')
        pylab.legend(loc = 'best')

trace_walk((UsualDrunk, ColdDrunk, EWDrunk), 200)

#%% Treacherous Fields =====================================================
class oddField(Field):
    def __init__(self, num_holes, x_range, y_range):
        Field.__init__(self)
        self.wormholes = {}
        for w in range(num_holes):
            x = random.randint(-x_range, x_range)
            y = random.randint(-y_range, y_range)
            new_x = random.randint(-x_range, x_range)
            new_y = random.randint(-y_range, y_range)
            new_loc = Location(new_x, new_y)
            self.wormholes[(x, y)] = new_loc
            
    def move_drunk(self, drunk):
        Field.move_drunk(self, drunk)
        x = self.drunks[drunk].get_x()
        y = self.drunks[drunk]. get_y()
        if (x, y) in self.wormholes:
            self.drunks[drunk] = self.wormholes[(x, y)]
            
def trace_walk_odd(drunkKinds, num_steps):
    style_choice = styleIterator(('k+', 'r^', 'mo'))
    f = oddField(1000, 100, 200)
    for dClass in drunkKinds:
        d = dClass()
        f.add_drunk(d, Location(0, 0))
        locs = []
        for s in range(num_steps):
            f.move_drunk(d)
            locs.append(f.get_loc(d))
        x_vals, y_vals = [], []
        for loc in locs:
            x_vals.append(loc.get_x())
            y_vals.append(loc.get_y())
        cur_style = style_choice.next_style()
        pylab.plot(x_vals, y_vals, cur_style,
                   label = dClass.__name__)
        pylab.title('Spots Visited on Walk ('
                    + str(num_steps) + ' steps)')
        pylab.xlabel('Steps East/West of Origin')
        pylab.ylabel('Steps North/South of Origin')
        pylab.legend(loc = 'best')

trace_walk_odd((UsualDrunk, ColdDrunk, EWDrunk), 500)