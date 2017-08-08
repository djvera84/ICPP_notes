# -*- coding: utf-8 -*-
"""
ICPP Chapter 24
Classification Methods
@author: Daniel J. Vera, Ph.D.
"""
import random
import pylab
import sklearn.linear_model
#%% Evaluating Classifiers =================================================
def accuracy(true_pos, false_pos, true_neg, false_neg):
    numerator = true_pos + true_neg
    denominator = true_pos + true_neg + false_pos + false_neg
    return numerator / denominator

def sensitivity(true_pos, false_neg):
    try:
        return true_pos / (true_pos + false_neg)
    except ZeroDivisionError:
        return float('nan')

def specificity(true_neg, false_pos):
    try:
        return true_neg / (true_neg + false_pos)
    except ZeroDivisionError:
        return float('nan')

def pos_pred_val(true_pos, false_pos):
    try:
        return true_pos / (true_pos + false_pos)
    except ZeroDivisionError:
        return float('nan')

def neg_pred_val(true_neg, false_neg):
    try:
        return true_neg / (true_neg + false_neg)
    except ZeroDivisionError:
        return float('nan')

def get_stats(true_pos, false_pos, true_neg, false_neg, to_print=True):
    accur = accuracy(true_pos, false_pos, true_neg, false_neg)
    sens = sensitivity(true_pos, false_neg)
    spec = specificity(true_neg, false_pos)
    ppv = pos_pred_val(true_pos, false_pos)
    if to_print:
        print(' Accuracy =', round(accur, 3))
        print(' Sensitivity =', round(sens, 3))
        print(' Specificity =', round(spec, 3 ))
        print(' Pos. Pred. Val =', round(ppv, 3))
    return (accur, sens, spec, ppv)

#%% Predicting the Gender of Runners =======================================
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
        data['age'].append(int(split[2]))
        data['division'].append(split[3])
        data['country'].append(split[4])
        data['time'].append(float(split[5][:-1])) # remove \n
        line = f.readline()
    f.close()
    return data


class Runner(object):
    def __init__(self, gender, age, time):
        self.feature_vec = (age, time)
        self.label = gender
        
    def feature_dist(self, other):
        dist = 0.0
        for i in range(len(self.feature_vec)):
            dist += abs(self.feature_vec[i] - other.feature_vec[i])**2
        return dist**0.5
    
    def get_time(self):
        return self.feature_vec[1]
    
    def get_age(self):
        return self.feature_vec[0]
    
    def get_label(self):
        return self.label
    
    def get_features(self):
        return self.feature_vec
    
    def __str__(self):
        return str(self.get_age()) + ', ' + str(self.get_time())\
               + ', ' + self.label


def build_marathon_examples(filename):
    data = get_bm_data(filename)
    examples = []
    for i in range(len(data['age'])):
        a = Runner(data['gender'][i], data['age'][i],
                   data['time'][i])
        examples.append(a)      
    return examples

def divide80_20(examples):
    sample_indices = random.sample(range(len(examples)), 
                                   len(examples) // 5)
    training_set, test_set = [], []
    for i in range(len(examples)):
        if i in sample_indices:
            test_set.append(examples[i])
        else:
            training_set.append(examples[i])
    return training_set, test_set

#%% K-nearest Neighbors ====================================================
def find_k_nearest(example, example_set, k):
    k_nearest, distances = [], []
    # Build lists containing first k examples and their distances
    for i in range(k):
        k_nearest.append(example_set[i])
        distances.append(example.feature_dist(example_set[i]))
    max_dist = max(distances) # Get maximum distance
    # Look at examples not yet considered
    for e in example_set[k:]:
        dist = example.feature_dist(e)
        if dist < max_dist:
            # replace farther neigbhor by this one
            max_index = distances.index(max_dist)
            k_nearest[max_index] = e
            distances[max_index] = dist
            max_dist = max(distances)
    return k_nearest, distances

def k_nearest_classify(training, test_set, label, k):
    """Assumes training and test_set are lists of examples, k an int
       Uses a k-nearest neighbor classifier to predict whether each
       example in test_set has the given label.
       Returns number of true positives, false positives,
       true negatives, and false negatives"""
    true_pos, false_pos, true_neg, false_neg = 0, 0, 0, 0
    for e in test_set:
        nearest, distances = find_k_nearest(e, training, k)
        # conduct vote
        num_match = 0
        for i in range(len(nearest)):
            if nearest[i].get_label() == label:
                num_match += 1
        if num_match > k // 2: # guess label
            if e.get_label() == label:
                true_pos += 1
            else:
                false_pos += 1
        else: # guess not label
            if e.get_label() != label:
                true_neg += 1
            else:
                false_neg += 1
    return true_pos, false_pos, true_neg, false_neg
#%%
examples = build_marathon_examples('bm_results2012.txt')
training, test_set = divide80_20(examples)
true_pos, false_pos, true_neg, false_neg =\
   k_nearest_classify(training, test_set, 'M', 9)
get_stats(true_pos, false_pos, true_neg, false_neg)
#%%
def prevalence_classify(training, test_set, label):
    """Assumes training and test_set lists of examples
       Uses a prevalence-based classifier to predict
       whether each example in test_set is of class label
       Returns numer of true positives, false positives,
       true negatives, and fasle negatives"""
    
    num_with_label = 0
    for e in training:
        if e.get_label() == label:
            num_with_label += 1
    prob_label = num_with_label / len(training)
    true_pos, false_pos, true_neg, false_neg = 0, 0, 0, 0
    for e in test_set:
        if random.random() < prob_label: # guess label
            if e.get_label() == label:
                true_pos += 1
            else:
                false_pos += 1
        else: # guess not label
            if e.get_label() != label:
                true_neg += 1
            else:
                false_neg += 1
    return true_pos, false_pos, true_neg, false_neg
#%%
true_pos, false_pos, true_neg, false_neg =\
   prevalence_classify(training, test_set, 'M')
get_stats(true_pos, false_pos, true_neg, false_neg)
#%% Down sample training by factor of 10
reduced_training = random.sample(training, len(training) // 10)
true_pos, false_pos, true_neg, false_neg =\
    k_nearest_classify(reduced_training, test_set, 'M', 9)
get_stats(true_pos, false_pos, true_neg, false_neg)
#%% n-fold cross validation
def find_k(training, min_k, max_k, num_folds, label):
    # Find average accuracy for range of odd values of k
    accuracies = []
    for k in range(min_k, max_k + 1, 2):
        score = 0.0
        for i in range(num_folds):
            # downsample to reduce computation time
            fold = random.sample(training, min(5000, len(training)))
            examples, test_set = divide80_20(fold)
            true_pos, false_pos, true_neg, false_neg =\
            k_nearest_classify(examples, test_set, label, k)
            score += accuracy(true_pos, false_pos, true_neg, false_neg)
        accuracies.append(score/num_folds)
    pylab.plot(range(min_k, max_k +1, 2), accuracies)
    pylab.title('Average Accuracy vs k (' + str(num_folds)\
                + ' folds)')
    pylab.xlabel('k')
    pylab.ylabel('Accuracy')

find_k(training, 1, 21, 5, "M")

#%% Regression-based Classifiers ===========================================
# Build training sets for men and women
age_m, age_w, time_m, time_w = [], [], [], []
for e in training:
    if e.get_label() == 'M':
        age_m.append(e.get_age())
        time_m.append(e.get_time())
    else:
        age_w.append(e.get_age())
        time_w.append(e.get_time())
# downsample to make plot of examples readable
ages, times = [], []
for i in random.sample(range(len(age_m)), 300):
    ages.append(age_m[i])
    times.append(time_m[i])

# Produce scatter plot of examples
pylab.plot(ages, times, 'yo', markersize=6, label='Men')
ages, times = [], []
for i in random.sample(range(len(age_w)), 300):
    ages.append(age_w[i])
    times.append(time_w[i])
pylab.plot(ages, times, 'k^', markersize=6, label='Women')
# Learn two first-degree linear regression models
m_model = pylab.polyfit(age_m, time_m, 1)
f_model = pylab.polyfit(age_w, time_w, 1)
#Plot lines corresponding to models
xmin, xmax = 15, 85
pylab.plot((xmin, xmax), (pylab.polyval(m_model, (xmin, xmax))),
           'k', label='Men')
pylab.plot((xmin, xmax), (pylab.polyval(f_model, (xmin, xmax))),
           'k--', label='Women')
pylab.title('Linear Regression Models')
pylab.xlabel('Age')
pylab.ylabel('Finishing time (minutes)')
pylab.legend()
#%%
true_pos, false_pos, true_neg, false_neg = 0, 0, 0, 0
for e in test_set:
    age = e.get_age()
    time = e.get_time()
    if abs(time - pylab.polyval(m_model, age)) <\
       abs(time - pylab.polyval(f_model, age)):
        if e.get_label() == 'M':
            true_pos += 1
        else:
            false_pos += 1
    else:
        if e.get_label() == 'F':
            true_neg += 1
        else:
            false_neg += 1
get_stats(true_pos, false_pos, true_neg, false_neg)
#%%

feature_vecs, labels = [], []
for i in range(25000): # create 4 examples in each iteration
    feature_vecs.append([random.gauss(0, 0.5), random.gauss(0, 0.5),
                         random.random()])
    labels.append('A')
    
    feature_vecs.append([random.gauss(0, 0.5), random.gauss(2, 0.5),
                         random.random()])
    labels.append('B')
    
    feature_vecs.append([random.gauss(2, 0.5), random.gauss(0 , 0.5),
                         random.random()])
    labels.append('C')
    
    feature_vecs.append([random.gauss(2, 0.5), random.gauss(2 , 0.5),
                         random.random()])
    labels.append('D')

model = sklearn.linear_model.LogisticRegression().fit(feature_vecs, labels)

print('model.classes_ =', model.classes_)
for i in range(len(model.coef_)):
    print('For label', model.classes_[i],
          'feature weights =', model.coef_[i])
print('[0, 0] probs =', model.predict_proba([[0, 0, 1]])[0])
print('[0, 2] probs =', model.predict_proba([[0, 2, 2]])[0])
print('[2, 0] probs =', model.predict_proba([[2, 0, 3]])[0])
print('[2, 2] probs =', model.predict_proba([[2, 2, 4]])[0])

#%% another example
feature_vecs, labels = [], []
for i in range(20000):
    feature_vecs.append([random.gauss(0, 0.5), random.gauss(0, 0.5)])
    labels.append('A')
    
    feature_vecs.append([random.gauss(2, 0.5), random.gauss(2, 0.5)])
    labels.append('D')

model = sklearn.linear_model.LogisticRegression().fit(feature_vecs, labels)

print('model.coef=', model.coef_)
print('[0, 0] probs =', model.predict_proba([[0, 0]])[0])
print('[0, 2] probs =', model.predict_proba([[0, 2]])[0])
print('[2, 0] probs =', model.predict_proba([[2, 0]])[0])
print('[2, 2] probs =', model.predict_proba([[2, 2]])[0])

#%% back to Boston marathon example
def apply_model(model, test_set, label, prob=0.5):
    # Create vector containing feature vectors for all test examples
    test_feature_vecs = [e.get_features() for e in test_set]
    probs = model.predict_proba(test_feature_vecs)
    true_pos, false_pos, true_neg, false_neg = 0, 0, 0, 0
    for i in range(len(probs)):
        if probs[i][1] > prob:
            if test_set[i].get_label() == label:
                true_pos += 1
            else:
                false_pos += 1
        else:
            if test_set[i].get_label() != label:
                true_neg += 1
            else:
                false_neg += 1
    return true_pos, false_pos, true_neg, false_neg

examples = build_marathon_examples('bm_results2012.txt')
training, test = divide80_20(examples)

feature_vecs, labels = [], []
for e in training:
    feature_vecs.append([e.get_age(), e.get_time()])
    labels.append(e.get_label())
model = sklearn.linear_model.LogisticRegression().fit(feature_vecs, labels)

print('Feature weights for label M:',
      'age =', str(round(model.coef_[0][0], 3)) + ',',
      'time =', round(model.coef_[0][1], 3))

true_pos, false_pos, true_neg, false_neg = \
                          apply_model(model, test, 'M', 0.5)
get_stats(true_pos, false_pos, true_neg, false_neg)
#%% call with prob = 0.578
print('Feature weights for label M:',
      'age =', str(round(model.coef_[0][0], 3)) + ',',
      'time =', round(model.coef_[0][1], 3))

true_pos, false_pos, true_neg, false_neg = \
                          apply_model(model, test, 'M', 0.578)
get_stats(true_pos, false_pos, true_neg, false_neg)

#%% ROC curves
def build_ROC(model, test_set, label, title, plot=True):
    x_vals, y_vals = [], []
    p = 0.0
    while p <= 1.0:
        true_pos, false_pos, true_neg, false_neg =\
                                  apply_model(model, test_set, label, p)
        x_vals.append(1.0 - specificity(true_neg, false_pos))
        y_vals.append(sensitivity(true_pos, false_neg))
        p += 0.01
    auroc = sklearn.metrics.auc(x_vals, y_vals, True)
    if plot:
        pylab.plot(x_vals, y_vals)
        pylab.plot([0, 1], [0, 1,], '--')
        pylab.title(title + ' (AUROC = '\
                               + str(round(auroc, 3)) + ')')
        pylab.xlabel('1 - Specificity')
        pylab.ylabel('Sensitivity')
    return auroc

build_ROC(model, test, 'M', 'ROC for Predicting Gender')

#%% Finger exercise: Write code to plot the ROC curve and compute the AUROC
# when the model built in Figure 24.15 is tested on 200 randomly chosen 
# competitors. Use that code to investigate the impact of the number of 
# training examples (try varying it from 10 to 1010 in increments of 50) 
# on the AUROC.
examples = build_marathon_examples('bm_results2012.txt')
training, test = divide80_20(examples)
training, test_set = divide80_20(examples)
test_set200 = random.sample(test_set, 200)

feature_vecs, labels = [], []
for e in training:
    feature_vecs.append([e.get_age(), e.get_time()])
    labels.append(e.get_label())
model_fe = sklearn.linear_model.LogisticRegression().fit(feature_vecs, labels)

def build_ROC_test(model, test_set, label, title, plot=True):
    x_vals, y_vals = [], []
    p = 0.0
    while p <= 1.0:
        true_pos, false_pos, true_neg, false_neg =\
                                  apply_model(model, test_set, label, p)
        x_vals.append(1.0 - specificity(true_neg, false_pos))
        y_vals.append(sensitivity(true_pos, false_neg))
        p += 0.01
    auroc = sklearn.metrics.auc(x_vals, y_vals, True)
    if plot:
        pylab.plot(x_vals, y_vals)
        pylab.plot([0, 1], [0, 1,], '--')
        pylab.title(title + ' (AUROC = '\
                               + str(round(auroc, 3)) + ')')
        pylab.xlabel('1 - Specificity')
        pylab.ylabel('Sensitivity')
    return auroc
build_ROC(model_fe, test_set200, 'M', 'ROC for Predicting Gender')

aurocs = []
sample_sizes = []
for i in range(10, 1010, 50):
    test_set_i = random.sample(test_set, i)
    aurocs.append(build_ROC(model_fe, test_set_i, 'M', 
              'ROC for Predicting Gender',
              plot=False))
    sample_sizes.append(i)

pylab.plot(sample_sizes, aurocs)
pylab.title('AUC of Different Test Sample Sizes')
pylab.xlabel('Sample Size for Test')
pylab.ylabel('AUROC')
pylab.xlim([5, 1000])
pylab.ylim([0.4, 1])
#%% Surviving the Titanic ==================================================
