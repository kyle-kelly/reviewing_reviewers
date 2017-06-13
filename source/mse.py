import csv
import math
import matplotlib.pyplot as plt
import numpy as np


def plot_MSE(reader, mse, figure):
	
	for row in reader:
		reviewers = row
		reviewers.pop(0)
		reviewers.pop(0)
		break
	y_pos = np.arange(len(reviewers))

	plt.figure(figure)
	plt.bar(y_pos, mse, align='center', alpha=0.5)
	plt.xticks(y_pos, reviewers, rotation=30)
	plt.ylabel('Mean Squared Error')
	plt.title('Mean Squared Error per Reviewer')

	plt.show()


def calculate_mse(sse, total_number_of_reviews_per_reviewer):

	mse = []

	if len(sse) != len(total_number_of_reviews_per_reviewer):
		print "ERROR! MSE lengths don't match."
	else:
		for i in range(len(sse)):
			mse.append(sse[i] / total_number_of_reviews_per_reviewer[i])

	return mse


def calculate_sse(reader, means, total_number_of_reviewers):

	sse = []
	HEADER_FLAG = True

	for reviewer in range(total_number_of_reviewers):
		sse.append(0)

	for row in reader:
		if HEADER_FLAG == True:
			HEADER_FLAG = False
		elif HEADER_FLAG == False:
			for reviewer in range(total_number_of_reviewers):
				if float(row[reviewer+2]) != -1:
					error = float(row[reviewer+2]) - means[0]
					squared_error = error**2
					sse[reviewer] += squared_error
			means.pop(0)

	return sse


def calculate_reviews_per_reviewer(reader, total_number_of_reviewers):

	number_of_reviews = []
	HEADER_FLAG = True

	for reviewer in range(total_number_of_reviewers):
		number_of_reviews.append(0)

	for row in reader:
		if HEADER_FLAG == True:
			HEADER_FLAG = False
		elif HEADER_FLAG == False:
			for reviewer in range(total_number_of_reviewers):
				if float(row[reviewer+2]) != -1:
					number_of_reviews[reviewer] += 1

	return number_of_reviews


def calculate_total_number_of_reviewers(reader):

	max_reviewers = 0

	for row in reader:
		column_count = len(row)
		number_of_reviewers = column_count - 2
		break
	return number_of_reviewers


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

		csv_file.seek(0)
		IMDB_title_means = calculate_title_means(reader, 'IMDB')
		print IMDB_title_means
		csv_file.seek(0)
		reviewer_title_means = calculate_title_means(reader, 'REVIEWER')
		print reviewer_title_means
		csv_file.seek(0)
		total_number_of_reviewers = calculate_total_number_of_reviewers(reader)
		print total_number_of_reviewers
		csv_file.seek(0)
		total_number_of_reviews_per_reviewer = calculate_reviews_per_reviewer(reader, total_number_of_reviewers)
		print total_number_of_reviews_per_reviewer
		csv_file.seek(0)
		sse_IMDB = calculate_sse(reader, IMDB_title_means, total_number_of_reviewers)
		print sse_IMDB
		csv_file.seek(0)
		sse_reviewer = calculate_sse(reader, reviewer_title_means, total_number_of_reviewers)
		print sse_reviewer

		mse_IMDB = calculate_mse(sse_IMDB, total_number_of_reviews_per_reviewer)
		print "MSE IMDB Means =", mse_IMDB
		mse_reviewer = calculate_mse(sse_reviewer, total_number_of_reviews_per_reviewer)
		print "MSE Reviewer Means = ", mse_reviewer

		csv_file.seek(0)
		plot_MSE(reader, mse_IMDB, 1)
		csv_file.seek(0)
		plot_MSE(reader, mse_reviewer, 2)

if __name__ == "__main__":
    main()