
# coding: utf-8
# Challenge Assignment
# ====================
# 
# S. Aguinaga, A. Nigam
# ---------------------
# Dec. 13, 2014

# Attribution:
# Code source: Jaques Grobler
# License: BSD 3 clause

from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import scipy as sp
##
from sklearn import svm
from sklearn import cross_validation
from sklearn import neighbors
from sklearn import linear_model, datasets

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
def linear_regression_classification(X_train,y_train, X_test,y_test):
    ## ########################################
    ##
    ## Regression
    ##
    ## ########################################

    ## Create linear regression object
    lin_reg_obj = linear_model.LinearRegression()

    ## Train the model using the training sets
    lin_reg_obj.fit(X_train, y_train)
    print "Coefficients:\n",lin_reg_obj.coef_

    # The mean square error
    print("Residual sum of squares: %.2f"
          % np.mean((lin_reg_obj.predict(X_test) - y_test) ** 2))

    ## Explained variance score: 1 is perfect prediction
    print("Variance score: %.2f" % lin_reg_obj.score(X_test, y_test))

    ## Plot outputs
    fig = plt.figure()
    ax = plt.gca()
    #print tst_reg.columns
    print np.shape(X_test), np.shape(y_test)
    ax.scatter(X_test, y_test,  color='black',alpha=0.05, edgecolors='none')
    ax.plot(X_test, lin_reg_obj.predict(X_test), color='blue',linewidth=3)
    
#    plt.scatter(diabetes_X_test, diabetes_y_test,  color='black')
#    plt.plot(diabetes_X_test, regr.predict(diabetes_X_test), color='blue',
#             linewidth=3)

    plt.xticks(())
    plt.yticks(())

    plt.show()
    return

def welcome(sys_argvs):
    print '\n'
    print '-'*80
    print sys_argvs
    return

def NearestNeighborsRegression(X,y,T):
    ###############################################################################
    print "NearestNeighborsRegression: ", np.size(X),np.size(y),np.size(T)
    # Fit regression model
    n_neighbors = 5

    for i, weights in enumerate(['uniform', 'distance']):
        knn = neighbors.KNeighborsRegressor(n_neighbors, weights=weights)
        print np.shape(X[:len(T)]), np.shape(y[:len(T)]), np.shape(T)
        y_ = knn.fit(X[:len(T)], y[:len(T)]).predict(T)
        
        plt.subplot(2, 1, i + 1)
                                    #print np.shape(T), np.shape(y_)
        plt.scatter(X, y, c='k', label='data')
        plt.plot(T, y_[0:len(T)], c='g', label='prediction')
        plt.axis('tight')
        plt.legend()
        plt.title("KNeighborsRegressor (k = %i, weights = '%s')" % (n_neighbors,
                                                                    weights))

    plt.show()

################################################################
##  main
###############################################################
if __name__ == "__main__":
    welcome(sys.argv)
    
    ## input data
    reg_df_train=pd.read_csv('../reg_challenge_train.csv')
    reg_df_test =pd.read_csv('../reg_challenge_test.csv')
    
    
    
    ## drop the target class from the data set
    df_X_train = reg_df_train.drop('target',1)
    y_train    = reg_df_train['target']
    
    df_X_test = reg_df_test.drop('target',1)
    y_test    = reg_df_test.target
    
    
    ## visualizing the dataset
    # Two subplots, unpack the axes array immediately
#    f, (ax1, ax2) = plt.subplots(2, 1, sharex=False)
#    ax2.scatter(np.arange(0,len(y_train)),y_train,  color='black',alpha=0.05, edgecolors='none')
#    
#    for i in np.arange(0,np.shape(df_X_train)[1]):
#        ax1.scatter(df_X_train[df_X_train.columns[i]],y_train,  color='black',alpha=0.05, edgecolors='none')
#
#    plt.show()

    # Take fist two features
    #X = df_X_train[['attr1','attr2']]
    #X_test = df_X_test[['attr1','attr2']]
    #Y = y_train
    from sklearn import cross_validation
    skf = cross_validation.StratifiedKFold(y_train, n_folds=10)

    def calculateAcc(ylabel,yhat):
        ctr=0
        for i in range(len(yhat)):
            if(ylabel.iloc[i]==yhat[i]):
                ctr=ctr+1
        error=ctr/len(yhat)
        return error

    ## Linear Regression
    print "Starting Linear Regression"
    
    linreg_acc=[]
    for train_index, test_index in skf:
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = df_X_train.iloc[train_index], df_X_test.iloc[test_index]
        y_train, y_test = y_train.iloc[train_index], y_train.iloc[test_index]
        
        rgr = linear_model.LinearRegression()
        
        rgr.fit(X_train, y_train)
        rgr_yhat=rgr.predict(X_test)
        linreg_acc.append(calculateAcc(y_test,rgr_yhat))

    
#    ## Train the model using the training sets
#    lin_reg_obj.fit(df_X_train, y_train)
#    print "Coefficients:\n",lin_reg_obj.coef_
#
#    # The mean square error
#    print("Residual sum of squares: %.2f" % np.mean((lin_reg_obj.predict(df_X_test) - y_test) ** 2))
#    
#    ## Explained variance score: 1 is perfect prediction
#    print("Variance score: %.2f" % lin_reg_obj.score(df_X_test.attr1, y_test))
#    
#    ## Plot outputs
#    fig = plt.figure()
#    ax = plt.gca()
#    #print tst_reg.columns
#    #print np.shape(X_test), np.shape(y_test)
#    ax.scatter(df_X_test.attr1, y_test,  color='black',alpha=0.05, edgecolors='none')
#    ax.plot(df_X_test, lin_reg_obj.predict(df_X_test), color='blue',alpha=0.05,linewidth=3)
#    
#    plt.xticks(())
#    plt.yticks(())
#    
#    plt.show()
#    sys.exit()
#    
#    
#    h = 0.2 # step size in mesh
#
#    logreg = linear_model.LogisticRegression(C=1e5)
#    # we create an instance of Neighbours Classifier and fit the data.
#    logreg.fit(X, Y)
#
#    # Plot the decision boundary. For that, we will assign a color to each
#    # point in the mesh [x_min, m_max]x[y_min, y_max].
#    x_min, x_max = X["attr1"].min() - .5, X["attr1"].max() + .5
#    y_min, y_max = X.attr2.min() - .5, X.attr2.max() + .5
#    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
#    Z = logreg.predict(np.c_[xx.ravel(), yy.ravel()])
#    print 'Done: Plot the decision boundary'
#    
#    # Put the result into a color plot
#    Z = Z.reshape(xx.shape)
#    plt.figure(1, figsize=(9, 6))
#    plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)
#    print 'Done put result into a color plot'
#
#    # Plot also the training points
#    #plt.scatter(X.attr1, X.attr2, c=Y, edgecolors='k', cmap=plt.cm.Paired)
#    #plt.scatter(X.attr1,Y, c=Y, edgecolors='k', cmap=plt.cm.Paired)
#    
##    plt.xlabel('Sepal length')
##    plt.ylabel('Sepal width')
#    print 'Done. plot training points'
#    
##    plt.xlim(xx.min(), xx.max())
##    plt.ylim(yy.min(), yy.max())
##    plt.xticks(())
##    plt.yticks(())
#
#    plt.show()
#    fig = plt.figure()
#    fig.savefig('temp.png')