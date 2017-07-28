# -*- coding: utf-8 -*-
"""
ICPP Chapter 20
Conditional Probability and Bayesian Statistics
@author: Daniel J. Vera, Ph.D.
"""
from scipy import stats
import random
#%% Conditional Probabilities ==============================================
# Finger exercise: Estimate the probability that a randomly chosen American
# is both male and weighs more than 180 pounds. Assume that 50% of the 
# population is male, and that the weights of the male population are normally
# distributed with a mean of 210 pounds and a standard deviation of 30 pounds. 
# (Hint: think about using the empirical rule.)

#Let X = 1 if male and 0 if female
#Let W = weight of a person
#W|X = 1 is normally distributed with mean 210 and standard devation 30.
#
#P(W > 180 and X = 1) = P(W > 180 | X = 1) * P(X = 1)
#= P(W > 180 | X = 1) * 0.5
#= P((W - 210) / 30 > (180 - 210) / 30 | X = 1) * 0.5
#= (1 - stats.norm.cdf(-1)) * 0.5
#
#Now we now that 68.27% of distribution is between -1 and 1 so we have
#half of that from -1 to 0 or 34.135%, roughly, added to 50% we get
#approximately 84.135%, then dividing by 2 we get 42.065%. Or we can just
#evaluate above expression:
(1 - stats.norm.cdf(-1)) * 0.5

#%% Bayes' Theorem =========================================================

# Canc = has breast cancer
# TP = true positive
# FP = false positive
# P(TP | Canc) = 0.9
# P(FP | not Canc) = 0.07
# P(Canc | woman in 40s) = 0.008
# P(not Canc | woman in 40s) = 0.992

# Bayes' Theorem: P(A|B) = (P(A) * P(B|A)) / P(B) 
# Proof: P(A|B) = P(AB) / P(B) = P(BA) / P(B) = (P(A) * P(B|A)) / P(B). QED

# P(Canc | Pos) = P(Pos | Canc) * P(Canc) / P(Pos)
# Now,
# P(Pos) = P(Pos|Canc) * P(Canc) + P(Pos|Not Canc) * P(Not Canc)
# = 0.9 * 0.008 + 0.07 * 0.992
# = 0.7664
# Therefore P(Canc | Pos) = 0.9 * 0.008 / 0.07664 = 0.094

# Finger exercise: You are wandering through a forest and see a field of 
# delicious-looking mushrooms. You fill your basket with them, and head home 
# prepared to cook them up and serve them to your husband. Before you cook 
# them, however, he demands that you consult a book about local mushroom 
# species to check whether they are poisonous. The book says that 80% of the
# mushrooms in the local forest are poisonous. However, you compare your
# mushrooms to the ones pictured in the book, and decide that you are 95%
# certain that your mushrooms are safe. How comfortable you should you be
# about serving them to your husband (assuming that you would rather not
# become a widow)?

# M = Mushroom is poisonous. 
# P(M) = 80%
# S = identify as safe (based on book)
# 
# P(M|S) = P(S|M) * P(M) / P(S)
# Now P(S) = P(S|M) * P(M) + P(S|!M) * P(!M)
# = (0.05) * (0.80) + (0.95) * (0.20) = 0.23
# Therefore P(M|S) = (0.05 * .80) / 0.23 = 17.4%, there about 82.6% sure
# that its safe.

#%% Bayesian Updating ======================================================
# Three dice, A, B, C, each has probability of rolling a six of 1/5, 1/6 and
# 1/7, respectively. Roll 6 on first dice roll. What if also on second?
# How do we make precise the notion that its probably dice A?
def calc_bayes(prior_a, prob_b_if_a, prob_b):
    """prior_a: initial estimate of probability of A independent of B
       prior_b_if_a: est. of probability of B assuming A is true
       prob_b: est. of probability of B
       returns probability of A given B"""
    return prior_a * prob_b_if_a / prob_b

prior_dice_a = 1/3
prob6_if_a = 1/5
prob6 = (1/5 + 1/6 + 1/7)/3

post_a = calc_bayes(prior_dice_a, prob6_if_a, prob6)
print('Probability of type A =', round(post_a, 4))
post_a = calc_bayes(post_a, prob6_if_a, prob6)
print('Probability of type A =', round(post_a, 4))

#%%
# throw other than 6?
post_a = calc_bayes(prior_dice_a, 1 - prob6_if_a, 1 - prob6)
print('Probability of type A =', round(post_a, 4))
post_a = calc_bayes(post_a, 1 - prob6_if_a, 1 - prob6)
print('Probability of type A =', round(post_a, 4))

# what if we think 90% of dice are of type A?
post_a = calc_bayes(0.9, 1 - prob6_if_a, 1 - prob6)
print('Probability of type A =', round(post_a, 4))
post_a = calc_bayes(post_a, 1 - prob6_if_a, 1 - prob6)
print('Probability of type A =', round(post_a, 4))

#%% stick with prior of type A being 90% but suppose we actually picked C.
# recall C has probability 1/7 coming up a 6.
num_rolls = 200
post_a = prior_a
for i in range(num_rolls + 1):
    if i % (num_rolls//10) == 0:
        print('After', i, 'rolls. Probability of type A =',
              round(post_a, 4))
    is_six = random.random() < 1/7 # because die is of type C
    if is_six:
        post_a = calc_bayes(post_a, prob6_if_a, prob6)
    else:
        post_a = calc_bayes(post_a, 1 - prob6_if_a, 1 - prob6)
        
# Note: there is a bug in this code as sometimes you get probabilities > 1.