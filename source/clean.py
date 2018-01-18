from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

DATA = np.genfromtxt('../data/ratings_data.csv', delimiter=',')
		
X = DATA[1:,2:]
y = DATA[1:,1]

# Missing values (-1) become row mean

for row in X:
	if np.where(row == -1):
		ratings = np.delete(row,np.where(row == -1))
		row[np.where(row == -1)] = ratings.mean()

# Standardize the data (mean=0, variance=1)
	
X_std = StandardScaler().fit_transform(X)


def linear():

	X_train, X_test, y_train, y_test = train_test_split(X_std, y,
                                                test_size=0.25,
                                                random_state=42)

	linreg = LinearRegression()

	linreg.fit(X_train, y_train)
	print("Linear Regression Train/Test: %.3f/%.3f" %
      (linreg.score(X_train, y_train),
       linreg.score(X_test, y_test)))

	y_pred = linreg.predict(X_test)

	# The coefficients
	print("Coefficients: \n", linreg.coef_)
	# The mean squared error
	print("Mean squared error: %.2f" %
		mean_squared_error(y_test, y_pred))
	# The mean absolute error
	print("Mean absolute error: %.2f" %
		mean_absolute_error(y_test, y_pred))
	# R2 score: 1 is perfect prediction
	print("R2 score: %.2f" % 
		r2_score(y_test, y_pred))
	# Explained variance score: 1 is perfect prediction
	print("Explained variance score: %.2f" % 
		explained_variance_score(y_test, y_pred))

	plt.plot(range(len(y_test)), y_test, 'o', label='data', markersize=8)
	plt.plot(range(len(y_pred)), y_pred, 's', label='prediction', markersize=4)

	plt.legend(loc='best')
	plt.title('Linear Regression')
	plt.xlabel('Movie')
	plt.ylabel('Rating')
	plt.show()


def	knn(n_neighbors=7):
			

	X_train, X_test, y_train, y_test = train_test_split(X_std, y,
                                                test_size=0.25,
                                                random_state=42)

	kneighbor_regression = KNeighborsRegressor(n_neighbors=n_neighbors, weights='distance')

	kneighbor_regression.fit(X_train, y_train)
	print("K-NN Regression Train/Test: %.3f/%.3f" %
      (kneighbor_regression.score(X_train, y_train),
       kneighbor_regression.score(X_test, y_test)))

	y_pred = kneighbor_regression.predict(X_test)

	# The mean squared error
	print("Mean squared error: %.2f" %
		mean_squared_error(y_test, y_pred))
	# The mean absolute error
	print("Mean absolute error: %.2f" %
		mean_absolute_error(y_test, y_pred))
	# R2 score: 1 is perfect prediction
	print("R2 score: %.2f" % 
		r2_score(y_test, y_pred))
	# Explained variance score: 1 is perfect prediction
	print("Explained variance score: %.2f" % 
		explained_variance_score(y_test, y_pred))

	plt.plot(range(len(y_test)), y_test, 'o', label="data", markersize=8)
	plt.plot(range(len(y_pred)), y_pred, 's', label="prediction", markersize=4)
	
	plt.legend(loc='best')
	plt.title('K-Nearest Neighbor Regression')
	plt.xlabel('Movie')
	plt.ylabel('Rating')
	plt.show()


def nn(hidden_layer_sizes=(3), activation='relu', solver='adam'):

	# TODO: 
	# - create option to standardize the data using StandardScaler().fit_transform(X)
	# - add hidden layers: try (500,100), (500,50), (500,50,50)

	X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                test_size=0.25,
                                                random_state=42)

	nn = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver)

	nn.fit(X_train, y_train)
	print("NN Regression Train/Test: %.3f/%.3f" %
      (nn.score(X_train, y_train),
       nn.score(X_test, y_test)))

	y_pred = nn.predict(X_test)

	# The mean squared error
	print("Mean squared error: %.2f" %
		mean_squared_error(y_test, y_pred))
	# The mean absolute error
	print("Mean absolute error: %.2f" %
		mean_absolute_error(y_test, y_pred))
	# R2 score: 1 is perfect prediction
	print("R2 score: %.2f" % 
		r2_score(y_test, y_pred))
	# Explained variance score: 1 is perfect prediction
	print("Explained variance score: %.2f" % 
		explained_variance_score(y_test, y_pred))

	# Plot actual and predicted values
	plt.plot(range(len(y_test)), y_test, 'o', label="data", markersize=8)
	plt.plot(range(len(y_pred)), y_pred, 's', label="prediction", markersize=4)
	
	plt.legend(loc='best')
	plt.title('Neural Network Regression')
	plt.xlabel('Movie')
	plt.ylabel('Rating')
	plt.show()


def run_pca():

	pca = PCA(n_components=12, svd_solver='full')
	X_proj = pca.fit_transform(X_std)

	print("Explained Variance Ratio:")
	print(pca.explained_variance_ratio_)
	print("Cumulative Explained Variance:")
	print(np.cumsum(pca.explained_variance_ratio_))

	plt.plot(X_proj[:,0], X_proj[:,1], 'o', label='All Events',markersize=6)
	plt.title('PCA on Standardized Data')
	plt.legend(loc='best');
	plt.show()