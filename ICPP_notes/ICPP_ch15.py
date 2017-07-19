# -*- coding: utf-8 -*-
"""
ICPP Chapter 15
Stochastic Programs, Probability, and Distributions
@author: Daniel J. Vera, Ph.D.
"""
import random
import pylab
#%% Stochastic Programs =====================================================
#def square_root(x, epsilon):
#    """Assumes x and epsilon are of type float; 
#       x > = 0 and epsilon > 0
#       Returns float y such that
#       x - epsilon <= y*y <= x + epsilon"""

#def roll_die():
#    """Returns an int between 1 and 6"""
# Better: """Returns a randomly chosen int between 1 and 6"""

def roll_die():
    """Returns a random int between 1 and 6"""
    return random.choice([1, 2, 3, 4, 5, 6])

def roll_N(n):
    result = ""
    for i in range(n):
        result = result + str(roll_die())
    print(result)

roll_N(10)

#%% Inferential Statistics =================================================
def flip(num_flips):
    """"Assumes num_flips a positive int"""
    heads = 0
    for i in range(num_flips):
        if random.choice(('H', 'T')) == 'H':
            heads += 1
    return heads/num_flips

def flip_sim(num_flips_per_trial, num_trials):
    """Assumes num_flips_per_trial and num_trials positive ints"""
    frac_heads = []
    for i in range(num_trials):
        frac_heads.append(flip(num_flips_per_trial))
    mean = sum(frac_heads)/len(frac_heads)
    return mean

print('Mean =', flip_sim(10, 1))
print('Mean =', flip_sim(10, 1))
print('Mean =', flip_sim(10, 1))
print('Mean =', flip_sim(10, 1))
print('Mean =', flip_sim(10, 1))

print('Mean =', flip_sim(10, 100))
print('Mean =', flip_sim(10, 100))
print('Mean =', flip_sim(10, 100))

print('Mean =', flip_sim(10, 100000))
#%%
def regress_to_mean(num_flips, num_trials):
    # Get fraction of heads for each trial of num_flips
    frac_heads = []
    for t in range(num_trials):
        frac_heads.append(flip(num_flips))
    # Find trials with extreme results and for each of the next trials
    extremes, next_trials = [], []
    for i in range(len(frac_heads) - 1):
        if frac_heads[i] < 0.33 or frac_heads[i] > 0.66:
            extremes.append(frac_heads[i])
            next_trials.append(frac_heads[i + 1])
    # Plot results
    pylab.plot(range(len(extremes)), extremes, 'ko',
               label='Extreme')
    pylab.plot(range(len(next_trials)), next_trials, 'k^',
               label='Next Trial')
    pylab.axhline(0.5)
    pylab.ylim(0, 1)
    pylab.xlim(-1, len(extremes) + 1)
    pylab.xlabel('Extreme Example and Next Trial')
    pylab.ylabel('Fraction Heads')
    pylab.title('Regression to the Mean')
    pylab.legend(loc = 'best')

regress_to_mean(15, 40)

#%% Finger Exercise: Sally averages 5 strokes a hole when she plays golf.
# One day, she took 40 strokes to complete the first nine holes. Her partner
# conjectured that she would probably regress to the mean and take 50 strokes
# to complete the next nine holes. Do you agree with her partner?

# No this is not what regression to the mean implies. Regression to the mean
# as stated in the text and evidenced by the coin simulation graph means
# that her next game will likely regress to 5 strokes per hole again, i.e.
# 45, the mean, not 50 to 'even out'

# To look at some code with similar to above coin simulation, lets assume
# Sally's strokes per game is normal with mean 5 and standard deviation 1.
import numpy as np
sally_strokes = np.random.normal(loc=5, scale=1, size=100)
# This generates a random sample of size 100. Now lets modify the 
# regress_to_mean function above and count extremes as less than 4 strokes
# or more than 6 strokes.

def regress_to_mean_sally_stroke():
    # Find trials with extreme results and for each of the next trials
    extremes, next_trials = [], []
    for i in range(len(sally_strokes) - 1):
        if sally_strokes[i] < 4 or sally_strokes[i] > 6:
            extremes.append(sally_strokes[i])
            next_trials.append(sally_strokes[i + 1])
    # Plot results
    pylab.plot(range(len(extremes)), extremes, 'ko',
               label='Extreme')
    pylab.plot(range(len(next_trials)), next_trials, 'k^',
               label='Next Trial')
    pylab.axhline(5) # her mean stroke per hole
    pylab.ylim(0, 10)
    pylab.xlim(-1, len(extremes) + 1)
    pylab.xlabel('Extreme Example and Next Trial')
    pylab.ylabel('Sally Strokes Per Hole')
    pylab.title('Regression to the Mean')
    pylab.legend(loc = 'best')
regress_to_mean_sally_stroke()

# As can be seen by the graph, a lot of times, after an extreme, her next
# game goes back to the baseline 5 strokes per hole but not always!
# Obviously MWV every time this is run since its randomly generated and
# We did not set the seed. In the first instance I ran this, I got one 
# trial where she got near an eight strokes per game and the next game
# she got over 8!
#%%
def flip_plot(min_exp, max_exp):
    """Assumes min_exp and max_exp positive integers;
       min_exp < max_exp
       Plots results of 2**min_exp to 2**max_exp coin flips"""
    ratios, diffs, x_axis = [], [], []
    for exp in range(min_exp, max_exp + 1):
        x_axis.append(2**exp)
    for num_flips in x_axis:
        num_heads = 0
        for n in range(num_flips):
            if random.choice(('H', 'T')) == 'H':
                num_heads += 1
        num_tails = num_flips - num_heads
        try:
            ratios.append(num_heads / num_tails)
            diffs.append(abs(num_heads - num_tails))
        except ZeroDivisionError:
            continue
    pylab.title('Difference Between Heads and Tails')
    pylab.xlabel('Number of Flips')
    pylab.ylabel('Abs(#Heads - #Tails)')
    pylab.plot(x_axis, diffs, 'ko') # original code had 'k' in text, 
    # then it was changed to 'ko' to get rid of the lines
    pylab.figure()
    pylab.title('Heads/Tails Ratios')
    pylab.xlabel('Number of Flips')
    pylab.ylabel('#Heads/#Tails')
    pylab.plot(x_axis, ratios, 'ko') # same with the 'ko' replacing 'k'

random.seed(0)
flip_plot(4, 20)
#%% Finger Exercise: Modify the code in flip_plot() so that it produces
# plots like figure 15.7 in text, logarithmic scales.
def flip_plot_log(min_exp, max_exp):
    """Assumes min_exp and max_exp positive integers;
       min_exp < max_exp
       Plots results of 2**min_exp to 2**max_exp coin flips"""
    ratios, diffs, x_axis = [], [], []
    for exp in range(min_exp, max_exp + 1):
        x_axis.append(2**exp)
    for num_flips in x_axis:
        num_heads = 0
        for n in range(num_flips):
            if random.choice(('H', 'T')) == 'H':
                num_heads += 1
        num_tails = num_flips - num_heads
        try:
            ratios.append(num_heads / num_tails)
            diffs.append(abs(num_heads - num_tails))
        except ZeroDivisionError:
            continue
    pylab.title('Difference Between Heads and Tails')
    pylab.xlabel('Number of Flips')
    pylab.xscale('log')
    pylab.ylabel('Abs(#Heads - #Tails)')
    pylab.yscale('log')
    pylab.plot(x_axis, diffs, 'ko') # original code had 'k' in text, 
    # then it was changed to 'ko' to get rid of the lines
    pylab.figure()
    pylab.title('Heads/Tails Ratios')
    pylab.xlabel('Number of Flips')
    pylab.xscale('log')
    pylab.ylabel('#Heads/#Tails')
    pylab.plot(x_axis, ratios, 'ko') # same with the 'ko' replacing 'k'

random.seed(0)
flip_plot_log(4, 20)
#%%
def variance(X):
    """Assumes X is a list of numbers.
       Returns the standard ceviation of X"""
    mean = sum(X) / len(X)
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return tot / len(X)

def std_dev(X):
    """Assumes that X is a list of numbers.
       Returns the standard deviation of X"""
    return variance(X)**0.5
#%%
def make_plot(x_vals, y_vals, title, x_label, y_label, style,
              logX= False, logY = False):
    pylab.figure()
    pylab.title(title)
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.plot(x_vals, y_vals, style)
    if logX:
        pylab.semilogx()
    if logY:
        pylab.semilogy()

def run_trial(num_flips):
    num_heads = 0
    for n in range(num_flips):
        if random.choice(('H', 'T')) == 'H':
            num_heads += 1
    num_tails = num_flips - num_heads
    return (num_heads, num_tails)

def flip_plot1(min_exp, max_exp, num_trials):
    """Assumes min_exp, max_exp, and num_trials ints > 0;
       min_exp < max_exp
       Plots results of num_trials trials of
       2**min_exp to 2**max_exp coin flips"""
    ratio_means, diff_means, ratio_sds, diff_sds = [], [], [], []
    x_axis = []
    for exp in range(min_exp, max_exp + 1):
        x_axis.append(2**exp)
    for num_flips in x_axis:
        ratios, diffs = [], []
        for t in range(num_trials):
            num_heads, num_tails = run_trial(num_flips)
            ratios.append(num_heads / num_tails)
            diffs.append(abs(num_heads - num_tails))
        ratio_means.append(sum(ratios) / num_trials)
        diff_means.append(sum(diffs) / num_trials)
        ratio_sds.append(std_dev(ratios))
        diff_sds.append(std_dev(diffs))
    num_trials_string = ' (' + str(num_trials) + ' Trials)'
    title = 'Mean Heads/Tails Ratios' + num_trials_string
    make_plot(x_axis, ratio_means, title, 'Number of Flips',
              'Mean Heads/Tails', 'ko', logX = True)
    title = "SD Heads/Tails Ratios" + num_trials_string
    make_plot(x_axis, ratio_sds, title, 'Number of Flips',
              'Standard Deviation', 'ko', logX = True, logY = True)
    title = "Mean abs(#Heads - #Tails)" + num_trials_string
    make_plot(x_axis, diff_means, title, 'Number of Flips',
              'Mean abs(#Heads - #Tails)', 'ko', logX = True, logY = True)
    title = "SD abs(#Heads - #Tails)" + num_trials_string
    make_plot(x_axis, diff_sds, title,
              'Number of Flips','Standard Deviation', 'ko',
              logX = True, logY = True)

flip_plot1(4, 20, 20)

def cv(X):
    mean = sum(X) / len(X)
    try:
        return std_dev(X) / mean
    except ZeroDivisionError:
        return float('nan')
#%%
def flip_plot2(min_exp, max_exp, num_trials):
    """Assumes min_exp, max_exp, and num_trials ints > 0;
       min_exp < max_exp
       Plots results of num_trials trials of
       2**min_exp to 2**max_exp coin flips"""
    ratio_means, diff_means, ratio_sds, diff_sds = [], [], [], []
    ratio_cvs, diff_cvs, x_axis = [], [], []
    for exp in range(min_exp, max_exp + 1):
        x_axis.append(2**exp)
    for num_flips in x_axis:
        ratios, diffs = [], []
        for t in range(num_trials):
            num_heads, num_tails = run_trial(num_flips)
            ratios.append(num_heads / float(num_tails))
            diffs.append(abs(num_heads - num_tails))
        ratio_means.append(sum(ratios) / num_trials)
        diff_means.append(sum(diffs) / num_trials)
        ratio_sds.append(std_dev(ratios))
        diff_sds.append(std_dev(diffs))
        ratio_cvs.append(cv(ratios))
        diff_cvs.append(cv(diffs))
    num_trials_string = ' (' + str(num_trials) + ' Trials)'
    title = 'Mean Heads/Tails Ratios' + num_trials_string
    make_plot(x_axis, ratio_means, title, 'Number of Flips',
              'Mean Heads/Tails', 'ko', logX = True)
    title = 'SD Heads/Tails Ratios' + num_trials_string
    make_plot(x_axis, ratio_sds, title, 'Number of Flips',
              'Standard Deviation', 'ko', logX = True, logY = True)
    title = 'Mean abs(#Heads - #Tails)' + num_trials_string
    make_plot(x_axis, diff_means, title, 'Number of Flips',
              'Mean abs(#Heads - #Tails)', 'ko', logX = True, logY = True)
    title = 'SD abs(#Heads - #Tails)' + num_trials_string
    make_plot(x_axis, diff_sds, title,
              'Number of Flips','Standard Deviation', 'ko',
              logX = True, logY = True)
    title = 'Coeff. of Var. abs(#Heads - #Tails)' + num_trials_string
    make_plot(x_axis, diff_cvs, title, 'Number of Flips',
              'Coef. of Var. abs(#Heads - #Tails)', 'ko', logX = True)
    title = 'Coeff. of Var. Heads/Tails Ratio' + num_trials_string
    make_plot(x_axis, ratio_cvs, title,'Number of Flips',
              'Coeff. of Var.', 'ko', logX = True, logY = True)

flip_plot2(4, 20, 20)
#%%
flip_plot2(4, 20, 1000) #takes a while to run, ~ 20 min.

#%% Distributions ==========================================================
def flip_for_sim(num_flips):
    """Assumes num_flips a positive int"""
    heads = 0
    for i in range(num_flips):
        if random.choice(('H', 'T')) == 'H':
            heads += 1
    return heads / float(num_flips)

def flip_sim(num_flips_per_trial, num_trials):
    frac_heads = []
    for i in range(num_trials):
        frac_heads.append(flip_for_sim(num_flips_per_trial))
    mean = sum(frac_heads) / len(frac_heads)
    sd = std_dev(frac_heads)
    return (frac_heads, mean, sd)

def label_plot(num_flips, num_trials, mean, sd):
    pylab.title(str(num_trials) + ' trials of'
                + str(num_flips) + 'flips each')
    pylab.xlabel('Fraction of Heads')
    pylab.ylabel('Number of Trials')
    pylab.annotate('Mean =' + str(round(mean, 4))\
                   + '\nSD = ' + str(round(sd, 4)), size='x-large',
                   xycoords = 'axes fraction', xy = (0.67, 0.5))

def make_plots(num_flips1, num_flips2, num_trials):
    val1, mean1, sd1 = flip_sim(num_flips1, num_trials)
    pylab.hist(val1, bins = 20)
    xmin, xmax = pylab.xlim()
    label_plot(num_flips1, num_trials, mean1, sd1)
    pylab.figure()
    val2, mean2, sd2 = flip_sim(num_flips2, num_trials)
    pylab.hist(val2, bins = 20)
    pylab.xlim(xmin, xmax)
    label_plot(num_flips2, num_trials, mean2, sd2)

make_plots(100, 1000, 100000)

#%% Normal Distributions
import scipy.integrate


def gaussian(x, mu, sigma):
    factor1 = (1.0 / (sigma * ((2 * pylab.pi)**0.5)))
    factor2 = pylab.e**-(((x - mu)**2) / (2 * sigma**2))
    return factor1 * factor2

def check_empirical(num_trials):
    for t in range(num_trials):
        mu = random.randint(-10, 10)
        sigma = random.randint(1, 10)
        print('For mu =', mu, 'and sigma =', sigma)
        for num_std in (1, 2, 3):
            area = scipy.integrate.quad(gaussian, mu - num_std * sigma,
                                                  mu + num_std * sigma,
                                        (mu, sigma)) [0]
            print('     Fraction within', num_std, 'std =',
                  round(area, 4))

check_empirical(3)
#%%
def show_error_bars(min_exp, max_exp, num_trials):
    """Assumes min_exp and max_exp positive ints; min_exp < max_exp
       num_trials a positive integer
       Plots mean fraction of heads with error bars"""
    means, sds, x_vals = [], [], []
    for exp in range(min_exp, max_exp + 1):
        x_vals.append(2**exp)
        frac_heads, mean, sd = flip_sim(2**exp, num_trials)
        means.append(mean)
        sds.append(sd)
    pylab.errorbar(x_vals, means, yerr=1.96*pylab.array(sds))
    pylab.semilogx()
    pylab.title('Mean Fraction of Heads('
                + str(num_trials) + ' trials)')
    pylab.xlabel('Number of flips per trial')
    pylab.ylabel('Fraction of heads & 95% confidence')
        
show_error_bars(3, 10, 100)

#%% Continuous and Discrete Uniform Distributions

# use random.uniform(min, max) for continuous
# use random.randint(min, max) for discrete

#%% Binomial and Multinomial Distributions
# Finger Exercise: Implement a function that calculates the probability of
# rolling exactly two 3’s in k rolls of a fair die. Use this function to 
# plot the probability as k varies from 2 to 100.
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

