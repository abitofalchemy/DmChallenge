# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 12:35:17 2014

@author: aastha
"""
from __future__ import division
import pandas as pd
from sklearn import cross_validation
from sklearn import neighbors
from sklearn import linear_model, datasets

print "reading data"
cds_df_train =pd.read_csv('reg_challenge_train.csv')
cds_df_test  =pd.read_csv('reg_challenge_test.csv')

traindata_cds=cds_df_train.drop('target',1)
trainlabel_cds=cds_df_train['target']


testdata_cds=cds_df_test.drop('target',1)
testlabel_cds=cds_df_test['target']

def calculateAcc(ylabel,yhat):
    ctr=0
    for i in range(len(yhat)):
        if(ylabel.iloc[i]==yhat[i]):
            ctr=ctr+1
    error=ctr/len(yhat)
    return error

from sklearn import cross_validation
skf = cross_validation.StratifiedKFold(trainlabel_cds, n_folds=10)

##Linear Regression
print "Starting Linear Regression"
from sklearn import svm

linr_acc=[]
for train_index, test_index in skf:
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = traindata_cds.iloc[train_index], traindata_cds.iloc[test_index]
    y_train, y_test = trainlabel_cds.iloc[train_index], trainlabel_cds.iloc[test_index] 

    rgr = linear_model.LinearRegression()

    rgr.fit(X_train, y_train)
    cds_yhat=rgr.predict(X_test)
    linr_acc.append(calculateAcc(y_test,cds_yhat))
 
#Logistic Regression
print "Starting Logistic Regression"

lg_acc=[]
for train_index, test_index in skf:
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = traindata_cds.iloc[train_index], traindata_cds.iloc[test_index]
    y_train, y_test = trainlabel_cds.iloc[train_index], trainlabel_cds.iloc[test_index] 

    h = 0.2 # step size in mesh
    
    rgrs = linear_model.LogisticRegression(C=1e5)
    # we create an instance of Neighbours Classifier and fit the data.
    #    logreg.fit(X, Y)
    rgrs.fit(X_train, y_train)
    cds_yhat=rgrs.predict(X_test)
    lg_acc.append(calculateAcc(y_test,cds_yhat))
print  "Done with logistic regression"


##Best of 2
import numpy as np
mean_linr=np.mean(linr_acc)
mean_lgrg=np.mean(lg_acc)

#
print "Mean Linear Regression accuracy",mean_linr
print "Mean Logistic Regression accuracy",mean_lgrg
#print "Mean Random Forest accuracy",mean_rf
#
#Chosing random forest because it gives best cv accuracy
regr = linear_model.LogisticRegression(C=1e5)
regr.fit(traindata_cds, trainlabel_cds)
cds_yhat=regr.predict(testdata_cds)
#
#
f=open('regression_fromtestdata.txt', 'w')
for item in cds_yhat:
  f.write("%s\n" % item)
  
f.flush()
f.close()