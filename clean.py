from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
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


def	knn(n_neighbors=9,weights='distance'):
			

	X_train, X_test, y_train, y_test = train_test_split(X_std, y,
                                                test_size=0.25,
                                                random_state=42)

	kneighbor_regression = KNeighborsRegressor(n_neighbors=n_neighbors, weights=weights)

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


def nn(hidden_layer_sizes=(3), activation='relu', solver='lbfgs', random_state=638):

	# TODO: 
	# - create option to standardize the data using StandardScaler().fit_transform(X)
	# - add hidden layers: try (500,100), (500,50), (500,50,50)

	X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                test_size=0.25,
                                                random_state=42)

	nn = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver, random_state=random_state)

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

	for i in range(len(y_test)):
		plt.plot([i, i], [y_test[i], y_pred[i]], color='g')
	
	plt.legend(loc='best')
	plt.title('Neural Network Regression')
	plt.xlabel('Movie')
	plt.ylabel('Rating')
	plt.show()

	# Plot actual and predicted values
	plt.plot(y_test, y_pred, 'o', markersize=8)

	plt.title('Neural Network Regression')
	plt.xlabel('IMDB Rating')
	plt.ylabel('Predicted Rating')
	plt.show()


def run_pca():

	# Run PCA
	pca = PCA(n_components=12, svd_solver='full')
	X_proj = pca.fit_transform(X_std)

	# Print variance
	print("Explained Variance Ratio:")
	print(pca.explained_variance_ratio_)
	print("Cumulative Explained Variance:")
	print(np.cumsum(pca.explained_variance_ratio_))

	# Plot first two PCs
	plt.plot(X_proj[:,0], X_proj[:,1], 'o', label='All Events',markersize=6)
	plt.title('PCA on Standardized Data')
	plt.legend(loc='best');
	plt.show()

	# Plot variances and cumulative variance
	sing_vals = np.array(range(len(pca.explained_variance_ratio_))) + 1
	plt.bar(sing_vals, pca.explained_variance_ratio_, align='center', alpha=0.5)
	plt.plot(sing_vals, np.cumsum(pca.explained_variance_ratio_), 'ro-', linewidth=2)
	plt.title('Explained Variance by Different Principal Components')
	plt.xlabel('Principal Component')
	plt.ylabel('Explained Variance')

	leg = plt.legend(['Cumulative Explained Variance'], loc='best', borderpad=0.3, 
		         shadow=False, prop=matplotlib.font_manager.FontProperties(size='small'),
		         markerscale=0.4)
	leg.get_frame().set_alpha(0.4)
	leg.draggable(state=True)
	plt.show()


def mean():

	# Compare data mean to IMDB scores

	y_pred = np.array([X.mean() for x in X])

	print("Data Mean")
	# R2 score: 1 is perfect prediction
	print("R2 score: %.2f" % 
		r2_score(y, y_pred/10))
	# The mean absolute error
	print("Mean absolute error: %.2f" %
		mean_absolute_error(y, y_pred/10))

	# Compare title means to IMDB scores

	y_pred = X.mean(axis=1)

	print("Title Mean")
	# R2 score: 1 is perfect prediction
	print("R2 score: %.2f" % 
		r2_score(y, y_pred/10))
	# The mean absolute error
	print("Mean absolute error: %.2f" %
		mean_absolute_error(y, y_pred/10))