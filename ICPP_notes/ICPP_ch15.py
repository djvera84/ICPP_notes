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