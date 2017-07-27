# -*- coding: utf-8 -*-
"""
ICPP Chapter 19
Randomized Trials and Hypothesis Checking
@author: Daniel J. Vera, Ph.D.
"""
import scipy
import pylab
import random
from scipy import stats
#%%
#Code to create Figure 19.1
treatment_dist = (119.5, 5.0)
control_dist = (120, 4.0)
random.seed(0) #Used to generate second set of results
sample_size = 100
treatment_times, control_times = [], []
for s in range(sample_size):
    treatment_times.append(random.gauss(treatment_dist[0],
                                       treatment_dist[1]))
    control_times.append(random.gauss(control_dist[0],
                                     control_dist[1]))
control_mean = sum(control_times)/len(control_times)
treatment_mean = sum(treatment_times)/len(treatment_times)
control_mean = 120.17
treatment_mean = 118.79
print('Treatment mean - control mean =', treatment_mean - control_mean,
      'minutes')
pylab.plot(treatment_times, 'bo',
        label = 'Treatment group (mean = ' +\
        str(round(treatment_mean, 2)) + ')')
pylab.plot(control_times, 'kv',
        label = 'Control group (mean = ' +
        str(round(control_mean,2)) + ')')
pylab.title('Test of PED-X')
pylab.xlabel('Cyclist')
pylab.ylabel('Finishing Time (minutes)')
pylab.ylim(100, 145)
pylab.legend()

#%% Checking Significance ==================================================
t_stat = -2.13165598142 # t-statistic for PED-X example in text
t_dist = []
num_bins = 1000
for i in range(10000000):
    t_dist.append(scipy.random.standard_t(198))

pylab.hist(t_dist, bins = num_bins,
           weights = pylab.array(len(t_dist) * [1.0]) / len(t_dist))
pylab.axvline(t_stat, color = 'w')
pylab.axvline(-t_stat, color = 'w')
pylab.title('T-distribution with 198 Degrees of Freedom')
pylab.xlabel('T-statistic')
pylab.ylabel('Probability')
#%%
control_mean = sum(control_times)/len(control_times)
treatment_mean = sum(treatment_times)/len(treatment_times)


print('Treatment mean - control mean =', treatment_mean - control_mean,
      'minutes')
two_sample_test = stats.ttest_ind(treatment_times, control_times,
                                  equal_var = False)
print('The t-statistic from two-sample test is', two_sample_test[0])
print('The p-value from two-sample test is', two_sample_test[1])

#%% One-tail and One-sample Tests ==========================================
one_sample_test = stats.ttest_1samp(treatment_times, 120)
print('The t-statistic from one-sample test is', one_sample_test[0])
print('The p-value from one-sample test is', one_sample_test[1])

#%% Significant of Not?
num_games = 1273
lyndsay_wins = 667
outcomes = [1.0] * lyndsay_wins + [0.0] * (num_games - lyndsay_wins)
print('The p-value from a one-sample test is',
      stats.ttest_1samp(outcomes, 0.5)[1])
#%%
num_games = 1273
lyndsay_wins = 667
num_trials = 10000
at_least = 0
for t in range(num_trials):
    l_wins = 0
    for g in range(num_games):
        if random.random() < 0.5:
            l_wins += 1
    if l_wins >= lyndsay_wins:
        at_least += 1
print('Probability of result at least this',
      'extreme by accident =', at_least / num_trials)
#%%
num_games = 1273
lyndsay_wins = 667
num_trials = 10000
at_least = 0
for t in range(num_trials):
    l_wins, j_wins = 0, 0
    for g in range(num_games):
        if random.random() < 0.5:
            l_wins += 1
        else:
            j_wins += 1
    if l_wins >= lyndsay_wins or j_wins >= lyndsay_wins:
        at_least += 1
print('Probability of result at least this',
      'extreme by accident =', at_least / num_trials)
#%% Multiple Hypotheses ====================================================
def get_bm_data(filename):
    """Read the contents of the given file. Assumes the file
       in a comma-seperated format, with 6 elements in each entry:
       0. Name (string), 1. Gender (string), 2. Age (int)
       3. Division (int), 4. Country (string), 5. Overall time (float)
       Returns: dict containing a list for each of the 6 variables."""
    
    data ={}
    f = open(filename)
    line = f.readline()
    data['name'], data['gender'], data['age'] = [], [], []
    data['division'], data['country'], data['time'], = [], [], []
    while line != '':
        split = line.split(',')
        data['name'].append(split[0])
        data['gender'].append(split[1])
        data['age'].append(split[2])
        data['division'].append(split[3])
        data['country'].append(split[4])
        data['time'].append(float(split[5][:-1])) # remove \n
        line = f.readline()
    f.close()
    return data

data = get_bm_data('bm_results2012.txt')
countries_to_compare = ['BEL', 'BRA', 'FRA', 'JPN', 'ITA']
# Build mapping from country to list of female finishing times
country_times = {}
for i in range (len(data['name'])): #for each racer
    if data['country'][i] in countries_to_compare and\
       data['gender'][i] == 'F':
        try:
            country_times[data['country'][i]].append(data['time'][i])
        except KeyError:
             country_times[data['country'][i]] = [data['time'][i]]
# Compare finishing times of countries
for c1 in countries_to_compare:
    for c2 in countries_to_compare:
        if c1 < c2: # < rather than != so each pair examined once
            p_val = stats.ttest_ind(country_times[c1],
                                    country_times[c2],
                                    equal_var = False)[1]
            if p_val < 0.05:
                print(c1, 'and', c2,
                      'have significantly different means,',
                      'p-value =', round(p_val, 4))
#%%
num_hyps = 20
sample_size = 30
population = []
for i in range(5000): # Create large population
    population.append(random.gauss(0, 1))
sample1s, sample2s = [], []
for i in range(num_hyps): # Generate many pairs of small samples
    sample1s.append(random.sample(population, sample_size))
    sample2s.append(random.sample(population, sample_size))
# Check pairs for statistically signficant difference
num_sig = 0
for i in range(num_hyps):
    if scipy.stats.ttest_ind(sample1s[i], sample2s[i])[1] < 0.05:
        num_sig += 1
print('Number of statistically significant (p < 0.05) results =',
      num_sig)