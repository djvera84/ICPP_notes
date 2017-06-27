# -*- coding: utf-8 -*-
"""
ICPP Chapter 11
Plotting and More about Classes
@author: Daniel J. Vera, Ph.D.
"""
#%% Plotting Using PyLab ===================================================
import pylab

pylab.figure(1)             # create figure 1
pylab.plot([1, 2, 3, 4],    # draw on figure 1
           [1, 7, 3, 5])
pylab.show()                # show figure on screen

pylab.figure(1)                 # create figure 1
pylab.plot([1, 2, 3, 4],        # draw on figure 1
           [1, 2, 3, 4])
pylab.figure(2)                 # create figure 2
pylab.plot([1, 4, 2, 3],        # draw on figure 2
           [5, 6, 7, 8])
pylab.savefig('Figure-Addie')   # save figure 2
pylab.figure(1)                 # go back to working on figure 1
pylab.plot([5, 6, 10, 3])       # draw again on figure 1
pylab.savefig('Figure-Jane')    # save figure 1

# Observe that the last call to pylab.plot is passed only one argument.
# This argument supplies the y values. The corresponding x values default
# to the sequence yielded by range(len([5, 6, 10, 3])), which is why they
# range from 0 to 3 in this case. PyLab has a notion of “current figure.” 
# Executing pylab.figure(x) sets the current figure to the figure numbered
# x. Subsequently executed calls of plotting functions implicitly refer to
# that figure until another invocation of pylab.figure occurs. 
# (from textbook)
#%%
principal = 10000 # intial investment
interest_rate = 0.05
years = 20
values = []
for i in range(years + 1):
    values.append(principal)
    principal += principal * interest_rate
pylab.plot(values)
pylab.title('5% Growth, Compounded Annually')
pylab.xlabel('Years of Coumpounding')
pylab.ylabel('Value of Principal ($)')

#%%
principal = 10000 # intial investment
interest_rate = 0.05
years = 20
values = []
for i in range(years + 1):
    values.append(principal)
    principal += principal * interest_rate
pylab.plot(values, 'ko')
pylab.title('5% Growth, Compounded Annually')
pylab.xlabel('Years of Coumpounding')
pylab.ylabel('Value of Principal ($)')
#%%
principal = 10000 # intial investment
interest_rate = 0.05
years = 20
values = []
for i in range(years + 1):
    values.append(principal)
    principal += principal * interest_rate
pylab.plot(values, linewidth = 30)
pylab.title('5% Growth, Compounded Annually',
            fontsize = 'xx-large')
pylab.xlabel('Years of Coumpounding',
             fontsize = 'x-small')
pylab.ylabel('Value of Principal ($)')
#%%
# pylab.rcParams['lines.linewidth'] = 6
# can use ggplot, see:
# http://matplotlib.org/users/style_sheets.html#style-sheets

#%% Plotting Mortgages, an Extended Example
def find_payment(loan, r, m):
    """Assumes: loan and r are floats, m an int
       Returns the monthly payment for a mortgage of size
       loan at a monthly rate of r for m months"""
    return loan * ((r * (1 + r)**m) / ((1 + r)**m - 1))


class Mortgage(object):
    """Abstract class for building different kinds of mortgages"""
    def __init__(self, loan, ann_rate, months):
        self.loan = loan
        self.rate = ann_rate / 12.0
        self.months = months
        self.paid = [0.0]
        self.outstanding = [loan]
        self.payment = find_payment(loan, self.rate, months)
        self.legend = None # description of mortgage
        
    def make_payment(self):
        self.paid.append(self.payment)
        reduction = self.payment - self.outstanding[-1] * self.rate
        self.outstanding.append(self.outstanding[-1] - reduction)
    
    def get_total_paid(self):
        return sum(self.paid)
    
    def __str__(self):
        return self.legend
    
    def plot_payments(self, style):
        pylab.plot(self.paid[1:], style, label = self.legend)
                
    def plot_balance(self, style):
        pylab.plot(self.outstanding, style, label = self.legend)
        
    def plot_tot_pd(self, style):
        tot_pd = [self.paid[0]]
        for i in range(1, len(self.paid)):
            tot_pd.append(tot_pd[-1] + self.paid[i])
        pylab.plot(tot_pd, style, label = self.legend)
        
    def plot_net(self, style):
        tot_pd = [self.paid[0]]
        for i in range (1, len(self.paid)):
            tot_pd.append(tot_pd[-1] + self.paid[i])
        equity_acquired = pylab.array([self.loan] * 
                                      len(self.outstanding))
        equity_acquired = equity_acquired - pylab.array(self.outstanding)
        net = pylab.array(tot_pd) - equity_acquired
        pylab.plot(net, style, label = self.legend)
        

#a1 = pylab.array([1, 2, 4])
#print('a1 =', a1) 
#a2 = a1 * 2
#print('a2 =', a2)
#print('a1 + 3 =', a1 + 3)
#print('3 - a1 =', 3 - a1)
#print('a1 - a2 =', a1 - a2)
#print('a1 * a2 =', a1 * a2)


class Fixed(Mortgage):
    def __init__(self, loan, r, months):
        Mortgage.__init__(self, loan, r, months)
        self.legend = 'Fixed, ' + str(r*100) + '%'


class FixedWithPts(Mortgage):
    def __init__(self, loan, r, months, pts):
        Mortgage.__init__(self, loan, r, months)
        self.pts = pts
        self.paid = [loan * (pts/100.0)]
        self.legend = 'Fixed, ' + str(r*100) + '%, '\
                      + str(pts) + ' points'


class TwoRate(Mortgage):
    def __init__(self, loan, r, months, teaser_rate, teaser_months):
        Mortgage.__init__(self, loan, teaser_rate, months)
        self.teaser_months = teaser_months
        self.teaser_rate = teaser_rate
        self.next_rate = r / 12.0
        self.legend = str(teaser_rate * 100)\
                     + '% for ' + str(self.teaser_months)\
                     + ' months, then ' + str(r*100) + '%'

    def make_payment(self):
        if len(self.paid) == self.teaser_months + 1:
            self.rate = self.next_rate
            self.payment = find_payment(self.outstanding[-1],
                                        self.rate,
                                        self.months - self.teaser_months)
        Mortgage.make_payment(self)


def compare_mortgages(amt, years, fixed_rate, pts, pts_rate, 
                      var_rate1, var_rate2, var_months):
    tot_months = years * 12
    fixed1 = Fixed(amt, fixed_rate, tot_months)
    fixed2 = FixedWithPts(amt, pts_rate, tot_months, pts)
    two_rate = TwoRate(amt, var_rate2, tot_months, var_rate1, var_months)
    morts = [fixed1, fixed2, two_rate]
    for m in range(tot_months):
        for mort in morts:
            mort.make_payment()
    plot_mortgages(morts, amt)

def plot_mortgages(morts, amt):
    def label_plot(figure, title, xlabel, ylabel):
        pylab.figure(figure)
        pylab.title(title)
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
        pylab.legend(loc = 'best')
        styles = ['k-', 'k-.', 'k:']
        # Give names to figure numbers
        payments, cost, balance, net_cost = 0, 1, 2, 3
        for i in range(len(morts)):
            pylab.figure(payments)
            morts[i].plot_payments(styles[i])
            pylab.figure(cost)
            morts[i].plot_tot_pd(styles[i])
            pylab.figure(balance)
            morts[i].plot_balance(styles[i])
            pylab.figure(net_cost)
            morts[i].plot_net(styles[i])
        label_plot(payments, 'Monthly Payments of $', + str(amt) +
                   ' Mortgages', 'Months', 'Monthly Payments')
        label_plot(cost, 'Cash Outlay of $' + str(amt) +
                   ' Mortgages', 'Months', 'Total Payments')
        label_plot(balance, 'Balance Remaining of $' + str(amt) +
                   ' Mortgages', 'Months', 'Remaining Loan Balance of $')
        label_plot(net_cost, 'Net Cost of $' + str(amt) +
                   ' Mortgages', 'Months', 'Payments - Equity $')
        
compare_mortgages(amt=200000, years=30, fixed_rate=0.07,
                  pts=3.25, pts_rate=0.05, var_rate1=0.045,
                  var_rate2=0.095, var_months=48)