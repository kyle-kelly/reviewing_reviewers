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
			print meta_url
		
			#This cleans up the link
			chars = set('?')
			if any((c in chars) for c in meta_url):
				meta_url, trash = meta_url.split("?",1)

			#This modifies the link to direct us to critic reviews page
			meta_url = meta_url + "/critic-reviews"

			metacritic_urls.append(meta_url)

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
