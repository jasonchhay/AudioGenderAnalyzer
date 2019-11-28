import numpy as np
from sklearn.naive_bayes import GaussianNB

X = [[-1, -1], [-2, -1], [-3, -2], [1,1], [2, 1], [3, 2]]
Y = [1, 1, 1, 2, 2, 2]
import csv
import math
import statistics


def init_audiofiles():
    audiofiles = []
    with open('C:/Users/Jason/Documents/MATLAB/audio_information.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            audiofiles.append(row)
    return audiofiles


def parse_audiofiles(audiofiles):
    properties = []
    gender = []

    for file in audiofiles:
        temp = [float(file['Pitch']), float(file['SPL'])]
        properties.append(temp)

        if file['Gender'] == 'M':
            gender.append(0)
        else:
            gender.append(1)

    return properties, gender

properties, gender = parse_audiofiles(init_audiofiles())
clf = GaussianNB()
clf.fit(properties, gender)

predictions = []
for i in range(len(properties)):
    X = [properties[i]]
    predictions.append(clf.predict(X)[0])

count_correct = 0

for i in range(len(gender)):
    if gender[i] == predictions[i]:
        count_correct += 1

print("sklearn percent correct:", count_correct/len(gender))
'''
print(clf.predict(X))
print(clf.predict_proba(X) * 100)
'''