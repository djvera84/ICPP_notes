# -*- coding: utf-8 -*-
"""
ICPP Chapter 17
Sampling and Confidence Intervals
@author: Daniel J. Vera, Ph.D.
"""
import pylab
import numpy as np
import random
import scipy.integrate
#%% Sampling the Boston Marathon ===========================================
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

def make_hist(data, bins, title, xlabel, ylabel):
    pylab.hist(data, bins)
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    mean = sum(data) / len(data)
    std = np.std(data)
    pylab.annotate('Mean =' + str(round(mean, 2)) +\
                   '\nSD =' + str(round(std, 2)), fontsize = 20,
                   xy = (0.65, 0.75), xycoords = 'axes fraction')

times = get_bm_data('bm_results2012.txt')['time']
make_hist(times, 20, '2012 Boston Marathon',
          'Minutes to Complete Race', 'Number of Runners')

# Above is the actual 'population' of the 2012 race.
# Lets do some sampling!
#%%
def sample_times(times, num_examples):
    """Assumes times a list of floats representing finishing
       times of all runners. num_examples an int
       Generates a random sample of size num_examples, and produces
       a histogram showing the distribution along with its mean and 
       standard deviation"""
    sample = random.sample(times, num_examples)
    make_hist(sample, 10, 'Sample of Size ' + str(num_examples),
                 'Minutes to Complete Race', 'Number of Runners')

sample_size = 40
sample_times(times, sample_size)
#%%
def gaussian(x, mu, sigma):
    factor1 = (1 / (sigma *((2 * pylab.pi)**0.5)))
    factor2 = pylab.e**-(((x - mu)**2) / (2 * sigma**2))
    return factor1 * factor2

area = round(scipy.integrate.quad(gaussian, -3, 3, (0, 1))[0], 4)
print('Probability of being within 3',
      'of true mean of tight dist. =', area)
area = round(scipy.integrate.quad(gaussian, -3, 3, (0, 100))[0], 4)
print('Probability of being within 3',
      'of true mean of wide dist. =', area)
#%%
def test_samples(num_trials, sample_size):
    tight_means, wide_means = [], []
    for t in range(num_trials):
        sample_tight, sample_wide = [], []
        for i in range(sample_size):
            sample_tight.append(random.gauss(0, 1))
            sample_wide.append(random.gauss(0, 100))
        tight_means.append(sum(sample_tight) / len(sample_tight))
        wide_means.append(sum(sample_wide) / len(sample_wide))
    return tight_means, wide_means

tight_means, wide_means = test_samples(1000, 40)
pylab.plot(wide_means, 'y*', label = ' SD = 100')
pylab.plot(tight_means, 'bo', label = ' SD = 1')
pylab.xlabel('Sample Number')
pylab.ylabel('Sample Mean')
pylab.title('Means of Samples of Size ' + str(40))
pylab.legend()

pylab.figure()
pylab.hist(wide_means, bins = 20, label = 'SD = 100')
pylab.title('Distribution of Sample Means')
pylab.xlabel('Sample Mean')
pylab.ylabel('Frequency of Occurence')
pylab.legend()