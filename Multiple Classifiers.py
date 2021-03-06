# -*- coding: utf-8 -*-
"""21100286_21100170_21100010_21100171_21100316.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HcN9GSfrC559Xvdt6TeQnI8QduVs3DdK
"""

!gdown --id 18qSvsM5W2QFASUlLWFPqxuYFPZcOs25b

!unzip "LUMS_FALL2020_PROJECT_DATA1.zip"

"""# Machine Learning Project
Will be used to make the Speaker Recognition Part
"""

!pip install python_speech_features

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import python_speech_features as mfcc
from scipy.io.wavfile import read
import pickle
import glob
import time
import os
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix

"""### Shared Functions"""

def get_MFCC(audio, sr):
    features = mfcc.mfcc(audio, sr, 0.025, 0.01, 13, appendEnergy = True)
    return np.mean(features, axis=0)

def get_numpy(elem):
  return np.array(elem)

def final_accuracies(y_test, y_pred):
  acc_score = (metrics.accuracy_score(y_test, y_pred))
  acc_score = (round(acc_score,2)) * 100

  macro_precision = (metrics.precision_score(y_test, y_pred, average='macro'))
  macro_precision = (round(macro_precision,2)) * 100

  macro_recall = (metrics.recall_score(y_test, y_pred, average='macro'))
  macro_recall = (round(macro_recall,2)) * 100

  macro_f1 = (metrics.f1_score(y_test, y_pred, average='macro'))
  macro_f1 = (round(macro_f1,2))*100

  confusion = confusion_matrix(y_test, y_pred, labels=np.unique(y_test))
  creport = classification_report(y_test, y_pred)

  return acc_score, macro_precision, macro_recall, macro_f1, confusion, creport

"""# Gender Recognition"""

def get_features2(directory):
  features_list = []
  labels_list = []
  for file in glob.iglob(directory):
    if 'F' in file:
      labels_list.append(0)
      sr, audio = read(file)
      features = get_MFCC(audio, sr)
      features_list.append(features)
    elif 'M' in file:
      labels_list.append(1)
      sr, audio = read(file)
      features = get_MFCC(audio, sr)
      features_list.append(features)
      
  return features_list, labels_list

def one_hot_converter(labels,y):
    one_hot = []
    for i in range(len(y)):
        vec = np.zeros((len(labels,)))
        vec[y[i][0]] = 1
        one_hot.append(vec)
    return np.array(one_hot)

starttime = time.time() 
X_train, y_train = get_features2("Gender_Recognition/Train/**/*.wav")
print ("Training Reading Time is = ", str(time.time() - starttime) + " seconds")

starttime = time.time() 
X_test, y_test = get_features2("Gender_Recognition/Test/**/*.wav")
print ("TestingReading Time is = ", str(time.time() - starttime) + " seconds")

X_train = get_numpy(X_train)
y_train = get_numpy(y_train)
X_test = get_numpy(X_test)
y_test = get_numpy(y_test)

X_train = np.concatenate([np.ones((len(X_train), 1)), X_train], axis=1)
X_test = np.concatenate([np.ones((len(X_test), 1)), X_test], axis=1)

print("Training Data X", X_train.shape)
print("Testing Data X", X_test.shape)
print()
print("Training Data Y", y_train.shape)
print("Testing Data Y", y_test.shape)

y_train = y_train.reshape(len(y_train), 1)
y_test = y_test.reshape(len(y_test), 1)

print("Training Data Y", y_train.shape)
print("Testing Data Y", y_test.shape)

unique_labels = np.unique(y_train)
unique_labels

"""###Part 1 - Multi-Layer Perceptron"""

model = MLPClassifier(random_state=1, max_iter=5000, activation='logistic', solver='sgd')
parameters = {'hidden_layer_sizes': [(128,64),(64),(64,32),(32)], 'learning_rate_init': [0.4,0.1,0.01]}
clf3 = GridSearchCV(model, parameters)
clf3.fit(X_train, y_train)

print(clf3.best_params_)

y_pred = clf3.predict(X_test)
y_pred

acc_score, macro_precision, macro_recall, macro_f1, confusion, classifcation = final_accuracies(y_test, y_pred)

print("Accuracy Score is: {}%".format(acc_score))
print("Macroaveraged Recall is: {}%".format(macro_recall))
print("Macroaveraged Precision is: {}%".format(macro_precision))
print("Macroaveraged F1-score is: {}%".format(macro_f1))

print("\nConfusion Matrix :\n")
print(confusion)

print("\nClassification Report:\n")
print(classifcation)

"""###Part 2 - SVM"""

clf2 = make_pipeline(StandardScaler(),LinearSVC(random_state=0, tol=1e-5))
clf2.fit(X_train, y_train)

y_pred = clf2.predict(X_test)
y_pred

acc_score, macro_precision, macro_recall, macro_f1, confusion, classifcation = final_accuracies(y_test, y_pred)

print("Accuracy Score is: {}%".format(acc_score))
print("Macroaveraged Recall is: {}%".format(macro_recall))
print("Macroaveraged Precision is: {}%".format(macro_precision))
print("Macroaveraged F1-score is: {}%".format(macro_f1))

print("\nConfusion Matrix :\n")
print(confusion)

print("\nClassification Report:\n")
print(classifcation)

"""###Part 3 - Gaussian"""

clf1 = GaussianNB()
clf1.fit(X_train,y_train.ravel())

y_pred = clf1.predict(X_test)
y_pred

acc_score, macro_precision, macro_recall, macro_f1, confusion, classifcation = final_accuracies(y_test, y_pred)

print("Accuracy Score is: {}%".format(acc_score))
print("Macroaveraged Recall is: {}%".format(macro_recall))
print("Macroaveraged Precision is: {}%".format(macro_precision))
print("Macroaveraged F1-score is: {}%".format(macro_f1))

print("\nConfusion Matrix :\n")
print(confusion)

print("\nClassification Report:\n")
print(classifcation)

"""#Speaker Recognition"""

def extract_label(file):
  r = file.split('SPK')[-1]
  return r[:3]

def get_features(directory):
  features_list = []
  labels_list = []
  for file in glob.iglob(directory):
    extracted_label = extract_label(file)
    labels_list.append(extracted_label)
    sr, audio = read(file)
    features = get_MFCC(audio, sr)
    features_list.append(features)
  return get_array(features_list, labels_list)

def get_array(features, labels):
  m = len(features)
  X = np.concatenate([np.ones((m, 1)), features], axis=1)
  X, Y = np.array(X), np.array(list(map(int, labels)))
  return X, Y.reshape(Y.shape[0], 1)

def one_hot_converter2(labels,y):
    one_hot = []
    for i in range(len(y)):
        vec = np.zeros((len(labels,)))
        vec[y[i][0]] = 1
        one_hot.append(vec)
    return np.array(one_hot)

starttime = time.time() 
X_train_speaker, y_train_speaker = get_features("Speaker_Recognition/Train/**/*.wav")
print ("Training Reading Time is = ", str(time.time() - starttime) + " seconds")

starttime = time.time() 
X_test_speaker, y_test_speaker = get_features("Speaker_Recognition/Test/**/*.wav")
print ("TestingReading Time is = ", str(time.time() - starttime) + " seconds")

print("Training Data X", X_train_speaker.shape)
print("Testing Data X", X_test_speaker.shape)
print()
print("Training Data Y", y_train_speaker.shape)
print("Testing Data Y", y_test_speaker.shape)

unique_labels_speaker = np.unique(y_train_speaker)
unique_labels_speaker.shape

"""###Part 1 - Multi-Layer Perceptron"""

model = MLPClassifier(random_state=1, max_iter=5000, activation='logistic', solver='sgd')
parameters = {'hidden_layer_sizes': [(128,64),(64),(64,32),(32)], 'learning_rate_init': [0.4,0.1,0.01]}
clf3 = GridSearchCV(model, parameters)
clf3.fit(X_train_speaker, y_train_speaker)

print(clf3.best_params_)

y_pred_speaker = clf3.predict(X_test_speaker)
y_pred_speaker

acc_score, macro_precision, macro_recall, macro_f1, confusion, classifcation = final_accuracies(y_test_speaker, y_pred_speaker)

print("Accuracy Score is: {}%".format(acc_score))
print("Macroaveraged Recall is: {}%".format(macro_recall))
print("Macroaveraged Precision is: {}%".format(macro_precision))
print("Macroaveraged F1-score is: {}%".format(macro_f1))

print("\nConfusion Matrix :\n")
print(confusion)

print("\nClassification Report:\n")
print(classifcation)

"""###Part 2 - SVM"""

clf2 = make_pipeline(StandardScaler(),LinearSVC(random_state=0, tol=1e-5))
clf2.fit(X_train_speaker, y_train_speaker)

y_pred_speaker = clf2.predict(X_test_speaker)
y_pred_speaker

acc_score, macro_precision, macro_recall, macro_f1, confusion, classifcation = final_accuracies(y_test_speaker, y_pred_speaker)

print("Accuracy Score is: {}%".format(acc_score))
print("Macroaveraged Recall is: {}%".format(macro_recall))
print("Macroaveraged Precision is: {}%".format(macro_precision))
print("Macroaveraged F1-score is: {}%".format(macro_f1))

print("\nConfusion Matrix :\n")
print(confusion)

print("\nClassification Report:\n")
print(classifcation)

"""###Part 3 - Gaussian"""

clf3 = GaussianNB()
clf3.fit(X_train_speaker,y_train_speaker)

y_pred_speaker = clf3.predict(X_test_speaker)
y_pred_speaker

accuracy_speaker = metrics.accuracy_score(y_test_speaker,y_pred_speaker)*100
accuracy_speaker

creport_speaker = classification_report(y_test_speaker, y_pred_speaker)
print(creport_speaker)