import csv
import numpy
from matplotlib.mlab import PCA
import matplotlib.pyplot as plt
import matplotlib


def plot_PCA_variance(fracs, figure):
	"""Scree plot of the fractions of variance explained by each principal component"""

	cummulative_fracs = []
	value = 0
	for variance in fracs:
		value = value + variance
		cummulative_fracs.append(value)

	fig = plt.figure(figure, figsize=(8,5))
	sing_vals = numpy.arange(len(fracs)) + 1
	plt.bar(sing_vals, fracs, align='center', alpha=0.5)
	plt.plot(sing_vals, cummulative_fracs, 'ro-', linewidth=2)
	plt.title('Explained Variance by Different Principal Components')
	plt.xlabel('Principal Component')
	plt.ylabel('Explained Variance')

	leg = plt.legend(['Cumulative Explained Variance'], loc='best', borderpad=0.3, 
		         shadow=False, prop=matplotlib.font_manager.FontProperties(size='small'),
		         markerscale=0.4)
	leg.get_frame().set_alpha(0.4)
	leg.draggable(state=True)
	plt.show()


def pca_IMDB_means(data, IMDB_title_means):
	"""Center and mormalize data and then perform SVD"""

	#Center the data around the IMDB mean
	centered_IMDB_data = center_data(data, IMDB_title_means)
	#Create numpy array
	myData = numpy.array(centered_IMDB_data) 
	#Normalize
	myData = myData / myData.std(axis=0)
	#Perform SVD
	U, s, Vh = numpy.linalg.svd(myData, full_matrices=False)
	#The weight vector for projecting a numdims point or array into PCA space.
	#The factor loadings for the first principal component are given by Wt[0]. 
	#This row is also the first eigenvector.
	Wt = Vh
	#Save the transposed coordinates
	Y = numpy.dot(Vh, myData.T).T
	#Save the eigenvalues
	s = s**2
	#Contribution of the individual components
	vars = s/float(len(s))
	fracs = vars/vars.sum()

	return Wt, fracs

def center_data(data, means):
	"""Subtract off means from the data and turn missing values (-1) to 0"""

	centered_data = []

	for row in data:
		centered_row = []
		for rating in row:
			if float(rating) == -1:
				centered_rating = 0
			else:
				centered_rating = float(rating) - means[0]
			centered_row.append(centered_rating)
		centered_data.append(centered_row)

	return centered_data


def format_data(reader):
	"""Strip header, titles and IMDB rating to leave a 2D array of only the data"""

	data = []
	HEADER_FLAG = True

	for row in reader:
		if HEADER_FLAG == True:
			HEADER_FLAG = False
		elif HEADER_FLAG == False:
			row.pop(0)
			row.pop(0)
			data.append(row)

	return data


def calculate_title_means(reader, type):
	"""Pull IMDB rating and scale or average the rating between all reviewers for each title"""

	means = []
	HEADER_FLAG = True

	if type == 'IMDB':
		for row in reader:
			if HEADER_FLAG == True:
				HEADER_FLAG = False
			elif HEADER_FLAG == False:
				means.append(float(row[1])*10)
		return means


def main():

	numpy.set_printoptions(suppress=True)

	with open("../data/ratings_data.csv", "rb") as csv_file:
		reader = csv.reader(csv_file)

		csv_file.seek(0)
		IMDB_title_means = calculate_title_means(reader, 'IMDB')

		csv_file.seek(0)
		data = format_data(reader)

		#Perform PCA and return weight matrix and fractions of total variance
		Wt, fracs = pca_IMDB_means(data, IMDB_title_means)
		print "Loadings for the first principal component = ", Wt[0]
		print "The proportion of variance of each of the principal components = ", fracs
		plot_PCA_variance(fracs, 1)

		#This will center and normalize the data before performing the SVD
		myData = numpy.array(data).astype(numpy.float)
		results = PCA(myData)
		print "Loadings for the first principal component = ", results.Wt[0]
		print "The proportion of variance of each of the principal components = ", results.fracs
		plot_PCA_variance(results.fracs, 2)


if __name__ == "__main__":
    main()
