import pandas as pd 
import numpy as np 
import os
from sklearn.svm import SVC
from sklearn import preprocessing, metrics 
from sklearn.model_selection import cross_val_score, LeaveOneOut
from sklearn.decomposition import PCA

# The following variables should contain the location of the EEG files, 
# as well as the subjects, trials, and tasks that are to be used in classification.
folder_loc = ""
subjects = []
trials = []
tasks = ["VPA Task"]
task_categories = {"VPA Task": ["true_congruent_correct", "false_congruent_correct", 
              "true_incongruent_correct", "false_incongruent_correct"]}

df = pd.DataFrame(columns=['Subject', 'Trial', 'Task', 'Category', 'Group','time', 
                           'Fp1', 'AF3', 'F7', 'F3', 'FC1', 'FC5', 'T7', 'C3', 'CP1', 'CP5',
                           'P7', 'P3', 'Pz', 'PO3', 'O1', 'Oz', 'O2', 'PO4', 'P4', 'P8', 'CP6',
                           'CP2', 'C4', 'T8', 'FC6', 'FC2', 'F4', 'F8', 'AF4', 'Fp2', 'Fz', 'Cz'])

def leave_one_out_f1(x, y):
    clf = SVC(kernel='linear')
    loo = LeaveOneOut()
    loo.get_n_splits(x)
    y_pred = []
    for train_index, test_index in loo.split(x):
        clf.fit(x[train_index], y[train_index])
        y_pred.append(*clf.predict(x[test_index]))
    return metrics.f1_score(y, y_pred)
    
for subject in subjects:
    for trial in trials:
        for task in tasks:
            for category in categories[task]:
                file_name = "{}-{} {} {}.csv".format(subject, trial, task, category)
                file_loc = os.path.join(folder_loc, subject, file_name)
                tmp = pd.read_csv(file_loc, index_col=0)
                tmp['Subject'] = subject
                tmp['Trial'] = trial 
                tmp['Task'] = task
                tmp['Category'] = category
                if int(subject) <50:
                    tmp['Group'] = 0
                else:
                    tmp['Group'] = 1
                # If downsampling frequency is changed, samples will need to be changed also
                samples = 256
                if len(tmp) > samples - 1:
                    tmp = tmp.truncate(after=samples - 1)
                df = df.append(tmp)

df['GFP'] = df.loc[:,'Fp1':'Cz'].mean(axis=1)

x = []
y = []
for subject in subjects:
    tmp = df[df['Subject'] == subject]['GFP']
    x.append(tmp)
    y.append(0 if int(subject) < 50 else 1)
x = np.array(x)
y = np.array(y)

print('GFP:', leave_one_out_f1(x,y))

channels = ['Fp1', 'AF3', 'F7', 'F3', 'FC1', 'FC5', 'T7', 'C3', 'CP1', 'CP5',
                           'P7', 'P3', 'Pz', 'PO3', 'O1', 'Oz', 'O2', 'PO4', 'P4', 'P8', 'CP6',
                           'CP2', 'C4', 'T8', 'FC6', 'FC2', 'F4', 'F8', 'AF4', 'Fp2', 'Fz', 'Cz']

for channel in channels:
    x = []
    for subject in subjects:
        tmp = df[df['Subject'] == subject][channel]
        x.append(tmp)
    x = np.array(x)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    x = np.array(x_scaled)
    x = [item for subject in x for item in subject]
    df[channel] = x

scores = []
for channel in channels:
    x = []
    y = []
    for subject in subjects:
        tmp = df[df['Subject'] == subject][channel]
        x.append(tmp)
        y.append(0 if int(subject) < 23 else 1)
    x = np.array(x)
    y = np.array(y)

    f1 = leave_one_out_f1(x,y)
    print(channel, f1)