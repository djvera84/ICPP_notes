# -*- coding: utf-8 -*-
"""
ICPP Chapter 21
Lies, Damned Lies, Statistics
@author: Daniel J. Vera, Ph.D.
"""
import pylab
import random
from scipy import stats
#%%
def plot_housing(impression):
    """Assumes impression a str. Must be one of 'flat',
       'volatile' and 'fair'
       Produce bar chart of housing prices over time"""
    f = open('midWestHousingPrices.txt', 'r')
    # Each line of file contains year quarter price
    # for Midwest region of U.S.
    labels , prices = ([], [])
    for line in f:
        year, quarter, price = line.split()
        label = year[2:4] + '\n Q' + quarter[1]
        labels.append(label)
        prices.append(int(price) / 1000)
    quarters = pylab.arange(len(labels)) #x coords of bar
    width = 0.8 # Width of bars
    pylab.bar(quarters, prices, width)
    pylab.xticks(quarters+width/2, labels)
    pylab.title('Housing Prices in U.S. Midwest')
    pylab.xlabel('Quarter')
    pylab.ylabel('Average Price ($1,000\'s)')
    if impression == 'flat':    
        pylab.ylim(1, 500)
    elif impression == 'volatile':
        pylab.ylim(180, 220)
    elif impression == 'fair':
        pylab.ylim(150, 250)
    else:
        raise ValueError

plot_housing('flat')
pylab.figure()
plot_housing('volatile')

# Look at Anscombe's Quartet

#%%
def june_prob(num_trials):
    june48 = 0
    for trial in range(num_trials):
        june = 0
        for i in range(446):
            if random.randint(1, 12) == 6:
                june += 1
        if june >= 48:
            june48 += 1
    j_prob = round(june48 / num_trials, 4)
    print('Probability of at least 48 births in June =', j_prob)

june_prob(10000)

#%%
def any_prob(num_trials):
    any_month48 = 0
    for trial in range(num_trials):
        months = [0] * 12
        for i in range(446):
            months[random.randint(0,11)] += 1
        if max(months) >= 48:
            any_month48 += 1
    a_prob = round(any_month48 / num_trials, 4)
    print('Probability of at least 48 births in some month =', a_prob)

any_prob(10000)
#%%
stats.ttest_1samp([1, 1], 0.5)[1]
# p-value associated with the hypothesis that coin is fair given
# getting 2 heads (say heads is 1) in 2 flips.