#!/usr/local/bin/python

"""
This program scrapes ratings from a number of IMDB webpages. It also pulls ratings for 
the corresponding movie from numerous reviewers on Metacritic. These are all written out
to the CSV file ratings_data.csv in the /data directory.
"""

from lxml import html
import requests
import numpy
import csv

def get_title_IMDB_ratings(urls, ratings, reviewers):
	"""Pull title and IMDB ratings"""

	titles = []
	xpath_titles = "//h3[@class='lister-item-header']/a"
	xpath_ratings =  "//div[@class='inline-block ratings-imdb-rating']/strong"

	for i in range(len(urls)):
		url = urls[i]
		page = requests.get(url)
		tree = html.fromstring(page.content)
		
		titleElements = tree.xpath(xpath_titles)
		for element in titleElements:
			titles.append(element.text)
		
		ratingElements = tree.xpath(xpath_ratings)
		for element in range(len(ratingElements)):
			ratings[50*i + element].append(ratingElements[element].text.encode('utf-8'))

	print titles, ratings
	
	return titles, ratings


def main():
	
	urls = (
		"http://www.imdb.com/search/title?year=2016,2016&title_type=feature&sort=boxoffice_gross_us,desc",
		"http://www.imdb.com/search/title?year=2015,2015&title_type=feature&sort=boxoffice_gross_us,desc",
		"http://www.imdb.com/search/title?year=2014,2014&title_type=feature&sort=boxoffice_gross_us,desc"
		)
	
	reviewers = (
		"Washington Post",
		"The New York Times",
		"The Telegraph",
		"Los Angeles Times",
		"Wall Street Journal",
		"Chicago Tribune",
		"Boston Globe",
		"Rolling Stone",
		"RogerEbert.com"
		)
	
	titles_per_year = 50
	n_total_titles = len(urls) * titles_per_year
	
	ratings = []
	for n in range(n_total_titles):
		ratings.append([])
	
	titles =[]
	
	titles, ratings = get_title_IMDB_ratings(urls, ratings, reviewers)

if __name__ == "__main__":
    main()
