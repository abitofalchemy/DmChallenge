
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
def linear_regression_classification():
    ## ########################################
    ##
    ## Regression
    ##
    ## ########################################



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
    reg_df_train=pd.read_csv('reg_challenge_train.csv')
    reg_df_test =pd.read_csv('reg_challenge_test.csv')
    
    #print 'Read training and test data into separate data frames:\n',reg_df_train.describe()
    # consists of 21 attributes and a target/class
    
    ## drop the target class from the data set
    df_X_train = reg_df_train.drop('target',1)
    y_train    = reg_df_train['target']
    one_X_train  = df_X_train[df_X_train.columns[0]]
    #print df_X_train.describe()
    
    df_X_test = reg_df_test.drop('target',1)
    y_test    = reg_df_test.target
    one_X_test  = df_X_test[df_X_test.columns[0]]
    #print df_X_test.describe()
    
    
    ## visualizing the dataset
    # Two subplots, unpack the axes array immediately
#    f, (ax1, ax2) = plt.subplots(2, 1, sharex=False)
#    ax2.scatter(np.arange(0,len(y_train)),y_train,  color='black',alpha=0.05, edgecolors='none')
#    
#    for i in np.arange(0,np.shape(df_X_train)[1]):
#        ax1.scatter(df_X_train[df_X_train.columns[i]],y_train,  color='black',alpha=0.05, edgecolors='none')
#
#    plt.show()

    ##
    # Take fist two features
    X = df_X_train[['attr1','attr2']]
    Y = y_train
    
    #print np.shape(two_X_train),'\n', two_X_train.head()
    h = 0.2 # step size in mesh

    logreg = linear_model.LogisticRegression(C=1e5)
    # we create an instance of Neighbours Classifier and fit the data.
    logreg.fit(X, Y)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, m_max]x[y_min, y_max].
    x_min, x_max = X["attr1"].min() - .5, X["attr1"].max() + .5
    y_min, y_max = X.attr2.min() - .5, X.attr2.max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = logreg.predict(np.c_[xx.ravel(), yy.ravel()])
    print 'Done: Plot the decision boundary'
    
    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1, figsize=(4, 3))
    plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)
    print 'Done put result into a color plot'
    
    # Plot also the training points
    plt.scatter(X.attr1, X.attr2, c=Y, edgecolors='k', cmap=plt.cm.Paired)
#    plt.xlabel('Sepal length')
#    plt.ylabel('Sepal width')
    print 'Done. plot training points'
    
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())

    plt.show()
