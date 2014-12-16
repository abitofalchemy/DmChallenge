# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 12:35:17 2014

@author: aastha
"""
from __future__ import division
import pandas as pd

print "reading data"
cds_df_train=pd.read_csv('../class_challenge_train.csv')
cds_df_test=pd.read_csv('../class_challenge_test.csv')

traindata_cds=cds_df_train.drop('class',1)
trainlabel_cds=cds_df_train['class']
#print traindata_cds.head()
#print trainlabel_cds.head()

testdata_cds=cds_df_test.drop('class',1)
testlabel_cds=cds_df_test['class']

def calculateAcc(ylabel,yhat):
    ctr=0
    for i in range(len(yhat)):
        if(ylabel.iloc[i]==yhat[i]):
            ctr=ctr+1
    error=ctr/len(yhat)
    return error

from sklearn import cross_validation
skf = cross_validation.StratifiedKFold(trainlabel_cds, n_folds=10)

##SVM
print "Starting SVM"
from sklearn import svm

svm_acc=[]
for train_index, test_index in skf:
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = traindata_cds.iloc[train_index], traindata_cds.iloc[test_index]
    y_train, y_test = trainlabel_cds.iloc[train_index], trainlabel_cds.iloc[test_index] 

    clf = svm.SVC()

    clf.fit(X_train, y_train)
    cds_yhat=clf.predict(X_test)
    svm_acc.append(calculateAcc(y_test,cds_yhat))
 
#Decision Trees
print "Starting Decision Trees"
from sklearn import tree

dt_acc=[]
for train_index, test_index in skf:
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = traindata_cds.iloc[train_index], traindata_cds.iloc[test_index]
    y_train, y_test = trainlabel_cds.iloc[train_index], trainlabel_cds.iloc[test_index] 

    clf = tree.DecisionTreeClassifier()

    clf.fit(X_train, y_train)
    cds_yhat=clf.predict(X_test)
    dt_acc.append(calculateAcc(y_test,cds_yhat))
    
#Random Forest
print "Starting Random Forest"
from sklearn.ensemble import RandomForestClassifier

rf_acc=[]
for train_index, test_index in skf:
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = traindata_cds.iloc[train_index], traindata_cds.iloc[test_index]
    y_train, y_test = trainlabel_cds.iloc[train_index], trainlabel_cds.iloc[test_index] 

    clf = RandomForestClassifier()

    clf.fit(X_train, y_train)
    cds_yhat=clf.predict(X_test)
    rf_acc.append(calculateAcc(y_test,cds_yhat))

##Best of 3
import numpy as np
mean_svm=np.mean(svm_acc)
mean_dt=np.mean(dt_acc)
mean_rf=np.mean(rf_acc)

print "Mean SVM accuracy",mean_svm
print "Mean Decision Tree accuracy",mean_dt
print "Mean Random Forest accuracy",mean_rf

#Chosing random forest because it gives best cv accuracy
clf = RandomForestClassifier()
clf.fit(traindata_cds, trainlabel_cds)
cds_yhat=clf.predict(testdata_cds)


f=open('classification_ontestdata.txt', 'w')
for item in cds_yhat:
  f.write("%s\n" % item)
  
f.flush()
f.close()