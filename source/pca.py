import csv
import numpy
from matplotlib.mlab import PCA


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

	if type == 'REVIEWER':
		for row in reader:
			if HEADER_FLAG == True:
				HEADER_FLAG = False
			elif HEADER_FLAG == False:
				title_rating_sum = 0
				rating_counter = 0
				for rating in range(1, len(row)-1):
					if float(row[rating]) != -1:
						title_rating_sum += float(row[rating])
						rating_counter += 1
				reviewer_title_mean = title_rating_sum / rating_counter
				means.append(reviewer_title_mean)
		return means


def main():

	with open("../data/ratings_data.csv", "rb") as csv_file:
		reader = csv.reader(csv_file)

		IMDB_title_means = calculate_title_means(reader, 'IMDB')
		csv_file.seek(0)
		reviewer_title_means = calculate_title_means(reader, 'REVIEWER')
		csv_file.seek(0)
		data = format_data(reader)
		
		centered_IMDB_data = center_data(data, IMDB_title_means)
		myData = numpy.array(centered_IMDB_data) 
		results = PCA(myData)
		print results.fracs

		centered_reviewer_data = center_data(data, reviewer_title_means)
		myData = numpy.array(centered_reviewer_data) 
		results = PCA(myData)
		print results.fracs


if __name__ == "__main__":
    main()
