# -*- coding: utf-8 -*-
"""
ICPP Chapter 16
Monte Carlo Simulation
@author: Daniel J. Vera, Ph.D.
"""
import random
import numpy as np

#%% Pascal's Problem =======================================================
def roll_die():
    return random.choice([1, 2, 3, 4, 5, 6])
    # changing above to [1, 1, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6] yields
    # dramatic effects and represents a 'cheater's dice'
    # fair dice: [1, 2, 3, 4, 5, 6]

def check_Pascal(num_trials):
    """Assumes num_trials an int > 0
       Prints an estimate of the probability of winning"""
    num_wins = 0
    for i in range(num_trials):
        for j in range(24):
            d1 = roll_die()
            d2 = roll_die()
            if d1 == 6 and d2 == 6:
                num_wins += 1
                break
    print('Probability of Winning =', num_wins / num_trials)

check_Pascal(1000000)
1 - (35.0 / 36.0)**24

#%% Pass or Don't Pass? ====================================================

class CrapsGame(object):
    def __init__(self):
        self.pass_wins, self.pass_losses = 0, 0
        self.dp_wins, self.dp_losses, self.dp_pushes = 0, 0, 0
        
    def play_hand(self):
        throw = roll_die() + roll_die()
        if throw == 7 or throw == 11:
            self.pass_wins += 1
            self.dp_losses += 1
        elif throw == 2 or throw == 3 or throw == 12:
            self.pass_losses += 1
            if throw == 12:
                self.dp_pushes += 1
            else:
                self.dp_wins += 1
        else:
            point = throw
            while True:
                throw = roll_die() + roll_die()
                if throw == point:
                    self.pass_wins += 1
                    self.dp_losses += 1
                    break
                elif throw == 7:
                    self.pass_losses += 1
                    self.dp_wins += 1
                    break
    
    def pass_results(self):
        return (self.pass_wins, self.pass_losses)
    
    def dp_results(self):
        return (self.dp_wins, self.dp_losses, self.dp_pushes)


def craps_sim(hands_per_game, num_games):
    """Assumes hands_per_game and num_games are ints > 0
       Play num_games of hands_per_game hands; print results"""
    games = []
    
    # Play num_games games
    for t in range(num_games):
        c = CrapsGame()
        for i in range (hands_per_game):
            c.play_hand()
        games.append(c)
        
    # Produce statistics for each game
    pROI_per_game, dpROI_per_game = [], []
    for g in games:
        wins, losses = g.pass_results()
        pROI_per_game.append((wins - losses) / float(hands_per_game))
        wins, losses, pushes = g.dp_results()
        dpROI_per_game.append((wins - losses) / float(hands_per_game))
    
    # Produce and print summary statistics
    
    meanROI = str(round((100*sum(pROI_per_game)/num_games), 4)) + '%'
    sigma = str(round(100*np.std(pROI_per_game), 4)) + '%'
    print('Pass:',  'Mean ROI =', meanROI, 'Std. Dev. =', sigma)
      
    meanROI = str(round((100*sum(dpROI_per_game)/num_games), 4)) + '%'
    sigma = str(round(100*np.std(dpROI_per_game), 4)) + '%'
    print('Don\'t Pass:',  'Mean ROI =', meanROI, 'Std. Dev. =', sigma)

# Structure of craps_sim simulation:
#   1. Runs multiple games (or trials) and accumulates the results;
#      each game has multiple hands so there is a nested loop.
#   2. Produces and stores statistics for each game.
#   3. Produces outputs and summary statistics.
# ROI = (gain - cost) / cost, "simple ROI."
# In game above, since the pass and don't pass lines pay even money,
# the ROI is (number of wins - number of losses) / (number of bets)
                
craps_sim(20, 10)
craps_sim(1000000, 10)
craps_sim(20, 1000000)
#%% Using Table Lookup to Improve Performance ==============================

def play_hand_table(self):
    # An alternative, faster, implentation of play_hand
    points_dict = {4:1/3, 5:2/5, 6:5/11, 8:5/11, 9:2/5, 10:1/3}
    throw = roll_die() + roll_die()
    if throw == 7 or throw == 11:
        self.pass_wins += 1
        self.dp_losses += 1
    elif throw == 2 or throw == 3 or throw == 12:
        self.pass_losses += 1
        if throw == 12:
            self.dp_pushes += 1
        else:
            self.dp_wins += 1
    else:
        if random.random() <= points_dict[throw]: # point before 7
            self.pass_wins += 1
            self.dp_losses += 1
        else:
            self.pass_losses += 1
            self.dp_wins += 1
#%% Finding π ==============================================================

def throw_needles(num_needles):
    in_circle = 0
    for needles in range(1, num_needles + 1):
        x = random.random()
        y = random.random()
        if (x*x + y*y)**0.5 <= 1:
            in_circle += 1
    # Counting needles in one quadrant only, so mulitply by 4
    return 4 * (in_circle / num_needles)

def get_est(num_needles, num_trials):
    estimates = []
    for t in range(num_trials):
        pi_guess = throw_needles(num_needles)
        estimates.append(pi_guess)
    sdev = np.std(estimates)
    cur_est = sum(estimates) / len(estimates)
    print('Est. = ', str(round(cur_est, 5)) + ',',
          'Std. Dev =', str(round(sdev, 5)) + ',',
          'Needles =', num_needles)
    return(cur_est, sdev)

def est_pi(precision, num_trials):
    num_needles = 1000
    sdev = precision
    while sdev > precision/1.96:
        cur_est, sdev = get_est(num_needles, num_trials)
        num_needles *= 2
    return cur_est

est_pi(0.01, 100)