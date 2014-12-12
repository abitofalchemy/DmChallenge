#print(__doc__)


# Code source: Jaques Grobler
# License: BSD 3 clause


import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import sys

# Load the diabetes dataset
diabetes = datasets.load_diabetes()


# Use only one feature
diabetes_X = diabetes.data[:, np.newaxis]
diabetes_X_temp = diabetes_X[:, :, 2]
print np.shape(diabetes.data)
#print diabetes.data[:,1]
print np.shape(diabetes_X), np.shape(diabetes_X_temp)

# Split the data into training/testing sets
diabetes_X_train = diabetes_X_temp[:-20]
diabetes_X_test = diabetes_X_temp[-20:]
print len(diabetes_X_train)
#print (diabetes_X_temp[0:])


# Split the targets into training/testing sets
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test = diabetes.target[-20:]

# Create linear regression object
regr = linear_model.LinearRegression()

print np.shape(diabetes_X_train),np.shape(diabetes_y_train)
# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)
#
# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(diabetes_X_test) - diabetes_y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(diabetes_X_test, diabetes_y_test))

# Plot outputs
fig = plt.figure()
ax = plt.gca()
ax.scatter(diabetes_X_test, diabetes_y_test,  color='black', alpha=0.05, edgecolors='none')
plt.plot(diabetes_X_test, regr.predict(diabetes_X_test), color='blue',
         linewidth=3)
ax.set_yscale('log')
ax.set_xscale('log')
#
#plt.xticks(())
#plt.yticks(())
#
#plt.show()