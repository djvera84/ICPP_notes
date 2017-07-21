# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:06:31 2017

@author: dvera
"""
import random
import numpy as np

def roll_die():
    return random.choice([1, 2, 3, 4, 5, 6])


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
