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

def write_out_csv(ratings):
	"""Write title, reviewers and ratings to a ccsv file in the /data directory"""
	with open("../data/ratings_data.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ',')
		for j in range(len(ratings)):
		    ratings[j] = map(float, ratings[j])
		writer.writerows(ratings)

def get_reviewer_ratings(urls, reviewers, ratings):
	"""Navigate to Metacritic and pull reviewer ratings"""

	#This list will hold urls to IMDB critic review page of each movie
	title_urls = []
	#This list will hold urls to Metacritic for each movie
	metacritic_urls = []

	#Iterate through each of the main IMDB urls
	for iteration in range(len(urls)):

		url = urls[iteration]
		page = requests.get(url)
		tree = html.fromstring(page.content)
		
		xpath_title_links = "//h3[@class='lister-item-header']/a/@href"
		titleElementLinks = tree.xpath(xpath_title_links)

		#Create a list of urls to all IMDB title critic review pages
		for link in titleElementLinks:
			link, trash = link.split("?",1)
			title_url = "http://imdb.com" + link + "criticreviews"
			title_urls.append(title_url)

	#Iterate through each title critic review url to pull Metacritic url
	for iteration in range(len(title_urls)):

		url = title_urls[iteration]
		page = requests.get(url)
		tree = html.fromstring(page.content)

		xpath_metacritic = "//div[@class='see-more']/a[@class='offsite-link']/@href"
		metaElementLink = tree.xpath(xpath_metacritic)
		
		for meta_url in metaElementLink:
		
			#This cleans up the link
			chars = set('?')
			if any((c in chars) for c in meta_url):
				meta_url, trash = meta_url.split("?",1)

			#This modifies the link to direct us to critic reviews page
			meta_url = meta_url + "/critic-reviews"

			metacritic_urls.append(meta_url)

	#Iterate through each Metacritic url to pull reviewers and ratings
	for iteration in range(len(metacritic_urls)):

		url = metacritic_urls[iteration]
		page = requests.get(url)
		tree = html.fromstring(page.content)

		#List of all critic sources for a particular movie
		xpath_sources = "//span[@class='source']/a"
		sourceElements = tree.xpath(xpath_sources)
		print sourceElements
		number_of_sources = len(sourceElements)
		print number_of_sources

		"""
		#List of all critic ratings for a particular movie
		ratingElements = driver.find_elements_by_css_selector('.metascore_w.large.movie.indiv')
		n_ratings = len(ratingElements)
		print number_of_ratings
		
		#Check the number of sources match ratings and then add pertinent reviews to list
		if number_of_sources == number_of_ratings:
			for reviewer in reviewers:
				for i in range(len(sourceElements)):
					if reviewer == sourceElements[i].text:
						ratings[50*iteration + j].append(ratingElements[i].text.encode('utf-8'))
						break
					else:
						if i == len(sourceElements) - 1:
							ratings[50*iteration + j].append('-1')
			write_out_csv(ratings)
		
		else:
			print "ERROR: Sources don't match ratings!!"
		"""

	print metacritic_urls
	return ratings

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
	ratings = get_reviewer_ratings(urls, reviewers, ratings)

if __name__ == "__main__":
    main()
