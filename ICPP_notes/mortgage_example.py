# -*- coding: utf-8 -*-
"""
From ICPP Chapter 11
Section 11.2 Plotting Mortgages
@author: Daniel J. Vera, Ph.D.
"""
import pylab

def find_payment(loan, r, m):
    """Assumes: loan and r are floats, m an int
       Returns: monthly payment for a mortgage of size
       loan at monthly rate of r for m months"""
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
        for i in range(1, len(self.paid)):
            tot_pd.append(tot_pd[-1] + self.paid[i])
        equity_acquired = pylab.array([self.loan] * len(self.outstanding))
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
        self.paid = [loan*(pts/100.0)]
        self.legend = 'Fixed, ' + str(r*100) +'%, ' + str(pts) + ' points'
        
        
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


def plot_mortgages(morts, amt):
    def label_plot(figure, title, xlabel, ylabel):
        pylab.figure(figure)
        pylab.title(title)
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
        pylab.legend(loc = 'best')
    styles = ['k-','k-.', 'k:']
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
    label_plot(payments, 'Monthly Payments of $' + str(amt) + ' Mortgages',
               'Months', 'Monthly Payments')
    label_plot(cost, 'Cash Outlay of $' + str(amt) + ' Mortgages',
               'Months', 'Total Payments')
    label_plot(balance, 'Balance Remaining of $' + str(amt) + ' Mortgages',
               'Months', 'Remaining Loan Balance of $')
    label_plot(net_cost, 'Net Cost of $' + str(amt) + ' Mortgages',
               'Months', 'Payments - Equity $')

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

compare_mortgages(amt=200000, years=30, fixed_rate=0.07, pts=3.25,
                  pts_rate=0.05, var_rate1=0.045, var_rate2=0.095, 
                  var_months=48)