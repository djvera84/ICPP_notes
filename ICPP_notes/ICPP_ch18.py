# -*- coding: utf-8 -*-
"""
ICPP Chapter 18
Understanding Experimental Data
@author: Daniel J. Vera, Ph.D.
"""
import pylab
import numpy as np
#%% The Behavior of Springs ================================================

def get_data(filename):
    data_file = open(filename, 'r')
    distances = []
    masses = []
    data_file.readline() # ignore header
    for line in data_file:
        d, m = line.split(' ')
        distances.append(float(d))
        masses.append(float(m))
    data_file.close()
    return (masses, distances)

def plot_data(input_file):
    masses, distances = get_data(input_file)
    distances = pylab.array(distances)
    masses = pylab.array(masses)
    forces = masses * 9.81
    pylab.plot(forces, distances, 'bo',
               label = 'Measured Displacements')
    pylab.title('Measured Displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')

plot_data('springData.txt')

#%% Using Linear Regression to Find a Fit
def fit_data(input_file):
    masses, distances = get_data(input_file)
    distances = pylab.array(distances)
    forces = pylab.array(masses) * 9.81
    pylab.plot(forces, distances, 'ko',
               label = 'Measured displacements')
    pylab.title('Measured Displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')
    # find linear fit
    a, b = pylab.polyfit(forces, distances, 1)
    predicted_distances = a * pylab.array(forces) + b
    k = 1.0 / a # slope a is delta(distance) / delta(force)
    # k is the reciprocal of slope
    pylab.plot(forces, predicted_distances,
               label = 'Displacements predicted by\n linear fit, k ='
               + str(round(k, 5)))
    pylab.legend(loc = 'best')

fit_data('springData.txt')
#%%
# find cubic fit
def fit_data_cubic(input_file):
    masses, distances = get_data(input_file)
    distances = pylab.array(distances)
    forces = pylab.array(masses) * 9.81
    pylab.plot(forces, distances, 'ko',
               label = 'Measured displacements')
    pylab.title('Measured Displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')
    # find linear fit
    a, b = pylab.polyfit(forces, distances, 1)
    predicted_distances = a * pylab.array(forces) + b
    k = 1.0 / a # slope a is delta(distance) / delta(force)
    # k is the reciprocal of slope
    pylab.plot(forces, predicted_distances,
               label = 'Displacements predicted by\n linear fit, k ='
               + str(round(k, 5)))
    pylab.legend(loc = 'best')
    fit = pylab.polyfit(forces, distances, 3)
    predicted_distances = pylab.polyval(fit, forces)
    pylab.plot(forces, predicted_distances, 'k:', label = 'cubic fit')
fit_data_cubic('springData.txt')    

#%% Finger exercise: Modify the code in Figure 18.5 so that it produces the 
# plot in Figure 18.8 in the text
def fit_data_cubic_fe(input_file):
    masses, distances = get_data(input_file)
    distances = pylab.array(distances)
    forces = pylab.array(masses) * 9.81
    pylab.plot(forces, distances, 'ko',
               label = 'Measured displacements')
    pylab.title('Measured Displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')
    # find linear fit
    a, b = pylab.polyfit(forces, distances, 1)
    predicted_distances = a * pylab.array(forces) + b
    k = 1.0 / a # slope a is delta(distance) / delta(force)
    # k is the reciprocal of slope
    pylab.plot(forces, predicted_distances,
               label = 'Displacements predicted by\n linear fit, k ='
               + str(round(k, 5)))
    pylab.legend(loc = 'best')
    fit = pylab.polyfit(forces, distances, 3)
    predicted_distances = pylab.polyval(fit, forces)
    forces_fe = np.append(forces, np.array([15]))
    predicted_distances_fe = pylab.polyval(fit, forces_fe)
    pylab.plot(forces_fe, predicted_distances_fe, 'k:', label = 'cubic fit')
    pylab.xlim([0, 16])
fit_data_cubic_fe('springData.txt')
#%% Back to linear fit:
# Hooke's law only valid up to some elastic limit, perhaps 7 in this case
def fit_data2(input_file):
    masses, distances = get_data(input_file)
    distances = pylab.array(distances[:-6])
    forces = pylab.array(masses[:-6]) * 9.81
    pylab.plot(forces, distances, 'ko',
               label = 'Measured displacements')
    pylab.title('Measured Displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')
    # find linear fit
    a, b = pylab.polyfit(forces, distances, 1)
    predicted_distances = a * pylab.array(forces) + b
    k = 1.0 / a # slope a is delta(distance) / delta(force)
    # k is the reciprocal of slope
    pylab.plot(forces, predicted_distances,
               label = 'Displacements predicted by\n linear fit, k ='
               + str(round(k, 5)))
    pylab.legend(loc = 'best')

fit_data2('springData.txt')
#%% The Behaviour of Projectiles ===========================================
def get_trajectory_data(filename):
    data_file = open(filename, 'r')
    distances = []
    heights1, heights2, heights3, heights4 = [], [], [], []
    data_file.readline()
    for line in data_file:
        d, h1, h2, h3, h4 = line.split()
        distances.append(float(d))
        heights1.append(float(h1))
        heights2.append(float(h2))
        heights3.append(float(h3))
        heights4.append(float(h4))
    data_file.close()
    return (distances, [heights1, heights2, heights3, heights4])

def process_trajectories(filename):
    distances, heights = get_trajectory_data(filename)
    num_trials = len(heights)
    # Get array containing mean height at each distance
    tot_heights = pylab.array([0] * len(distances))
    for h in heights:
        tot_heights = tot_heights + pylab.array(h)
    mean_heights = tot_heights / len(heights)
    pylab.title('Trajectory of Projectile (Mean of '\
                                           + str(num_trials) + ' Trials)')
    pylab.xlabel('Inches from Launch Point')
    pylab.ylabel('Inches Above Launch Point')
    pylab.plot(distances, mean_heights, 'ko')
    fit = pylab.polyfit(distances, mean_heights, 1)
    altitudes = pylab.polyval(fit, distances)
    pylab.plot(distances, altitudes, 'b', label = 'Linear Fit')
    fit = pylab.polyfit(distances, mean_heights, 2)
    altitudes = pylab.polyval(fit, distances)
    pylab.plot(distances, altitudes, 'k:', label = 'Quadratic Fit')
    pylab.legend()

process_trajectories('launcherData.txt')

#%% Coefficient of Determination
def r_squared(measured, predicted):
    """Assumes measured a one-dimensional array of measured values
               predicted a one-dimensional array of predicted values
       Returns coefficient of determination"""
    estimate_error = ((predicted - measured)**2).sum()
    mean_of_measured = measured.sum() / len(measured)
    variability = ((measured - mean_of_measured)**2).sum()
    return 1 - estimate_error / variability

def process_trajectories_rsquared(filename):
    distances, heights = get_trajectory_data(filename)
    num_trials = len(heights)
    # Get array containing mean height at each distance
    tot_heights = pylab.array([0] * len(distances))
    for h in heights:
        tot_heights = tot_heights + pylab.array(h)
    mean_heights = tot_heights / len(heights)
    pylab.title('Trajectory of Projectile (Mean of '\
                                           + str(num_trials) + ' Trials)')
    pylab.xlabel('Inches from Launch Point')
    pylab.ylabel('Inches Above Launch Point')
    pylab.plot(distances, mean_heights, 'ko')
    fit = pylab.polyfit(distances, mean_heights, 1)
    altitudes = pylab.polyval(fit, distances)
    pylab.plot(distances, altitudes, 'b', label = 'Linear Fit')
    print('RSquare of linear fit =', r_squared(mean_heights, altitudes))
    fit = pylab.polyfit(distances, mean_heights, 2)
    altitudes = pylab.polyval(fit, distances)
    pylab.plot(distances, altitudes, 'k:', label = 'Quadratic Fit')
    print('RSquare of qudratic fit =', r_squared(mean_heights, altitudes))
    pylab.legend()
    
process_trajectories_rsquared('launcherData.txt')
#%% Using a Computational Model
def get_horizontal_speed(quad_fit, min_x, max_x):
    """Assumes quad_fit has coefficients of a quadratic polynomial
               min_x and max_x are distances in inches
       Returns horizontal speed in feet per second"""
    inches_per_foot = 12
    x_mid = (max_x - min_x) / 2
    a, b, c = quad_fit[0], quad_fit[1], quad_fit[2]
    # model: a * x^2 + b *x + c
    y_peak = a * x_mid**2 + b * x_mid + c
    g = 32.16 * inches_per_foot #accel. of gravity in inches/sec/sec
    t = (2 * y_peak / g)**0.5 # time in seconds from peak to target
    print('Horizontal speed =',
          int(x_mid/(t * inches_per_foot)), 'feet/sec')

def process_trajectories_rsquared_speed(filename):
    distances, heights = get_trajectory_data(filename)
    num_trials = len(heights)
    # Get array containing mean height at each distance
    tot_heights = pylab.array([0] * len(distances))
    for h in heights:
        tot_heights = tot_heights + pylab.array(h)
    mean_heights = tot_heights / len(heights)
    pylab.title('Trajectory of Projectile (Mean of '\
                                           + str(num_trials) + ' Trials)')
    pylab.xlabel('Inches from Launch Point')
    pylab.ylabel('Inches Above Launch Point')
    pylab.plot(distances, mean_heights, 'ko')
    fit = pylab.polyfit(distances, mean_heights, 1)
    altitudes = pylab.polyval(fit, distances)
    pylab.plot(distances, altitudes, 'b', label = 'Linear Fit')
    print('RSquare of linear fit =', r_squared(mean_heights, altitudes))
    fit = pylab.polyfit(distances, mean_heights, 2)
    altitudes = pylab.polyval(fit, distances)
    pylab.plot(distances, altitudes, 'k:', label = 'Quadratic Fit')
    print('RSquare of qudratic fit =', r_squared(mean_heights, altitudes))
    pylab.legend()
    get_horizontal_speed(fit, distances[-1], distances[0])
    
process_trajectories_rsquared_speed('launcherData.txt')