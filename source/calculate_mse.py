import csv
import math

IMDB = 0
REVIEWER = 1


def calculate_mse(sse, total_number_of_reviews_per_reviewer):

	mse = []

	if len(sse) != len(total_number_of_reviews_per_reviewer):
		print "ERROR! MSE lengths don't match."
	else:
		for i in range(len(sse)):
			mse.append(sse[i] / total_number_of_reviews_per_reviewer[i])

	print "MSE =", mse
	return mse


def calculate_reviews_per_reviewer(reader, total_number_of_reviewers):

	number_of_reviews = []

	for reviewer in range(total_number_of_reviewers):
		number_of_reviews.append(0)

	for row in reader:
		if len(row) != 1:
			for rating in range(len(row)-1):
				if float(row[rating+1]) != -1:
					number_of_reviews[rating] += 1

	print "Reviews per reviewer =", number_of_reviews
	return number_of_reviews

def calculate_sse(reader, means, total_number_of_reviewers):

	sse = []

	for reviewer in range(total_number_of_reviewers):
		sse.append(0)

	for row in reader:
		reviewer_counter = 0
		if len(row) != -1:
			for rating in range(len(row)-1):
				if float(row[rating+1]) != -1:
					error = float(row[rating+1]) - means[0]
					squared_error = error**2
					sse[reviewer_counter] += squared_error
				reviewer_counter += 1
		means.pop()

	print "SSE =", sse
	return sse

def calculate_total_reviewers(reader):

	max_reviewers = 0

	for row in reader:
		column_count = len(row)
		if column_count > max_reviewers:
			max_reviewers = column_count

	print "Reviewers =", max_reviewers - 1
	return max_reviewers - 1



def calculate_title_means(reader, type):
	"""Pull IMDB rating and scale or average the rating between all reviewers for each title"""

	means = []

	if type == IMDB:
		for row in reader:
			means.append(float(row[0])*10)

		return means

	if type == REVIEWER:
		for row in reader:
			title_rating_sum = 0
			rating_counter = 0
			if len(row) != 1:
				for rating in range(len(row)-1):
					if float(row[rating+1]) != -1:
						title_rating_sum += float(row[rating+1])
						rating_counter += 1
				reviewer_title_mean = title_rating_sum / rating_counter
				means.append(reviewer_title_mean)
			elif len(row) == 1:
				means.append(-1)

		return means


def main():

	mse_IMDB = []
	mse_reviewer = []

	with open("../data/ratings_data.csv", "rb") as file:

		reader = csv.reader(file)

		file.seek(0)
		IMDB_title_means = calculate_title_means(reader, IMDB)
		file.seek(0)
		reviewer_title_means = calculate_title_means(reader, REVIEWER)
		file.seek(0)
		total_number_of_reviewers = calculate_total_reviewers(reader)
		file.seek(0)
		total_number_of_reviews_per_reviewer = calculate_reviews_per_reviewer(reader, total_number_of_reviewers)
		file.seek(0)
		sse_IMDB = calculate_sse(reader, IMDB_title_means, total_number_of_reviewers)
		file.seek(0)
		sse_reviewer = calculate_sse(reader, reviewer_title_means, total_number_of_reviewers)

		mse_IMDB = calculate_mse(sse_IMDB, total_number_of_reviews_per_reviewer)
		mse_reviewer = calculate_mse(sse_reviewer, total_number_of_reviews_per_reviewer)

if __name__ == "__main__":
    main()
