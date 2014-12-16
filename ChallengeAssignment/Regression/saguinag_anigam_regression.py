
# coding: utf-8

# Challenge Assignment
# ====================
# 
# S. Aguinaga, A. Nigam
# ---------------------
# 

# Dec. 13, 2014
# </br>
# 

## Workspace: -----------

## Classification




# Code source: Jaques Grobler
# License: BSD 3 clause


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import scipy as sp
##
from sklearn import svm
from sklearn import cross_validation

### this section is taking an significant time to run-through
#clf = svm.SVC(kernel='linear',C=1)
#scores = cross_validation.cross_val_score(clf, traindata_cds, trainlabel_cds, cv=10)
#print scores.mean()
##print "Standard deviation", scores.std()
#
## clf.fit(traindata_cds, trainlabel_cds)
#
## cds_yhat=clf.predict(testdata_cds)
## print cds_yhat

## ########################################
##
## Regression
##
## ########################################

## input data
reg_df_train=pd.read_csv('reg_challenge_train.csv')
reg_df_test =pd.read_csv('reg_challenge_test.csv')

#print 'Read training and test data into separate data frames:\n',reg_df_train.describe()
# consists of 21 attributes and a target/class

## drop the target class from the data set
trn_reg   = reg_df_train.drop('target',1)
trn_label = reg_df_train['target']
X_train   = trn_reg[trn_reg.columns[0]]

tst_reg =reg_df_test.drop('target',1)
tst_label = reg_df_test.target
X_test = tst_reg[tst_reg.columns[0]]


# Use only one feature
reg_X_train = X_train[:, np.newaxis]
reg_X_test  = X_test[:, np.newaxis]

from sklearn import linear_model

## Create linear regression object
lin_reg_obj = linear_model.LinearRegression()

## Train the model using the training sets
lin_reg_obj.fit(trn_reg, trn_label)
print "Coefficients:\n",lin_reg_obj.coef_

# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((lin_reg_obj.predict(tst_reg) - tst_label) ** 2))

## Explained variance score: 1 is perfect prediction
print("Variance score: %.2f" % lin_reg_obj.score(tst_reg, tst_label))


## Plot outputs
##print np.shape(trn_reg), np.shape(trn_label)
##print type(trn_reg), type(trn_label)
##
### need a slice of the data frame
### get one feature
##print trn_reg[trn_reg.columns[0]]
###dat_X = trn_reg[:,1]
###print np.shape(dat_X)
###print type(dat_X)
#
#
## Plot outputs
fig = plt.figure()
ax = plt.gca()
#print tst_reg.columns
##print np.shape()
##ax.scatter(tst_reg, tst_label,  color='black',alpha=0.05, edgecolors='none')
#
##ax.scatter(tst_reg)
##ax.set_yscale('log')
#
##ax.axis([fig_ax[0],fig_ax[1],50,200])
for x in np.arange(0,np.shape(tst_reg)[1]):
    ax.scatter(tst_reg[tst_reg.columns[x]], tst_label,  color='black',alpha=0.05, edgecolors='none')
    print np.shape(tst_reg[tst_reg.columns[x]])
    print np.shape(lin_reg_obj.predict(tst_reg))
    
    ax.plot(tst_reg[tst_reg.columns[x]], lin_reg_obj.predict(tst_reg), color='blue',linewidth=3,alpha=0.05)
##fig_ax = ax.axis()
##print fig_ax
##ax.axis([fig_ax[0],fig_ax[1],99.995,100.001])
plt.xticks(())
plt.yticks(())

plt.show()