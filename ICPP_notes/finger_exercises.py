# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 07:11:30 2017

@author: dvera
"""
# Finger exercise: Implement a function that calculates the probability of
# rolling exactly two 3s in k rolls of a fair die. Use this function to plot
# the probabilitry as k varies from 2 to 100.

import random
import pylab
import math

# Probability of rolling one 3 in one roll is 1 / 6 for fair die. Therefore,
# in k trials the probability of rolling exactly 2 rolls is 
# (k choose 2) * (1/6)**2 * (5/6)**(k-2)

def choose(n, k):
    """Assumes n, k >= 0 integers and n > k"""
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

def binomial_prob(n, k, p=1/6):
    """Assumes n, k >= 0 integers and n > k,
       p a float between 0 and 1, default 1/6, (think dice) 
       Returns probability of rolling exactly k rolls in n trials"""
    binomial = choose(n, k)
    successes = p**k
    failures = (1 - p)**(n-k)
    return binomial * successes * failures

def plot_binom_probs(min_trial = 2, max_trial = 100):
    x_vals = []
    probs = []
    for i in range(min_trial, max_trial + 1):
        x_vals.append(i)
    for x in x_vals:
        probs.append(binomial_prob(x, 2))
    pylab.figure()
    pylab.plot(x_vals, probs, 'b|')
    pylab.xlabel('Number of Trials')
    pylab.ylabel('Probability of Exactly 2 Successes in x trials')

plot_binom_probs()
#%% Exponential and Geometric Distributions
def clear(n, p, steps):
    """Assumes n & steps positive ints, p a float
       n: the initial number of molecules
       p: the probability of molecules being cleared
       steps: the length of the simulation"""
    num_remaining = [n]
    for t in range(steps):
        num_remaining.append(n*((1-p)**t))
    pylab.plot(num_remaining)
    pylab.xlabel('Time')
    pylab.ylabel('Molecules Remaining')
    pylab.title('Clearance of Drug')

clear(1000, 0.01, 1000)

def clear_log_scale(n, p, steps):
    """Assumes n & steps positive ints, p a float
       n: the initial number of molecules
       p: the probability of molecules being cleared
       steps: the length of the simulation"""
    num_remaining = [n]
    for t in range(steps):
        num_remaining.append(n*((1-p)**t))
    pylab.plot(num_remaining)
    pylab.xlabel('Time')
    pylab.ylabel('Molecules Remaining')
    pylab.semilogy()
    pylab.title('Clearance of Drug')

clear_log_scale(1000, 0.01, 1000)

# random.expovariate(lambd) gives exponential distribution with mean 1/lambd
# Geometric distribution is discrete analog of exponential distribution.
#%%
def successful_starts(success_prob, num_trials):
    """Assumes success_prob is a float representing probaiblity of a 
       single attempt being successful. num_trials a positive int.
       Returns a list of the number of attempts needed before a
       success for each trial"""
    tries_before_success = []
    for t in range(num_trials):
        consec_failures = 0
        while random.random() > success_prob:
            consec_failures += 1
        tries_before_success.append(consec_failures)
    return tries_before_success

prob_of_success = 0.5
num_trials = 5000
distribution = successful_starts(prob_of_success, num_trials)
pylab.hist(distribution, bins = 14)
pylab.xlabel('Tries Before Success')
pylab.ylabel('Number of Occurences Out of ' + str(num_trials))
pylab.title('Probability of Starting Each Try = '\
            + str(prob_of_success))

#%% Benford's Distribution
# A set of decimal numbers is said to satisfy Benford’s law107 if the 
# probability of the first digit being d is consistent with 
# P(d) = log10(1 + 1/ d).

#%% Hashing and Collisions =================================================
def collision_prob(n, k):
    prob = 1.0
    for i in range(1, k):
        prob = prob * ((n-i) / n)
    return 1 - prob

collision_prob(1000, 50)
collision_prob(1000, 200)

def sim_insertions(num_indices, num_insertions):
    """Assumes num_indices and num_insertions are positive ints.
       Returns 1 if there is a collision; 0 otherwise"""
    choices = range(num_indices) # list of possible indices
    used = []
    for i in range(num_insertions):
        hash_val = random.choice(choices)
        if hash_val in used: # there is a collision
            return 1
        else:
            used.append(hash_val)
    return 0

def find_prob(num_indices, num_insertions, num_trials):
    collisions = 0
    for t in range(num_trials):
        collisions += sim_insertions(num_indices, num_insertions)
    return collisions / num_trials

print('Actual probability of a collision =', collision_prob(1000, 50))
print('Est. probability of a collision =', find_prob(1000, 50, 10000))
print('Actual probability of a collision =', collision_prob(1000, 200))
print('Est. probability of a collision =', find_prob(1000, 200, 10000))

#%% How Often Does the Better Team Win?

def play_series(num_games, team_prob):
    num_won = 0
    for game in range(num_games):
        if random.random() <= team_prob:
            num_won += 1
    return (num_won > num_games//2)

def fraction_won(team_prob, num_series, series_len):
    won = 0
    for series in range(num_series):
        if play_series(series_len, team_prob):
            won += 1
    return won/float(num_series)

def sim_series(num_series):
    prob = 0.5
    fracs_won, probs = [], []
    while prob <= 1.0:
        fracs_won.append(fraction_won(prob, num_series, 7))
        probs.append(prob)
        prob += 0.01
    pylab.axhline(0.95) # Draw a line at 95%
    pylab.plot(probs, fracs_won, 'k', linewidth = 5)
    pylab.xlabel('Probability of Winning a Game')
    pylab.ylabel('Probability of Winning a Series')
    pylab.title(str(num_series) + ' Seven-Game Series')

sim_series(400)
