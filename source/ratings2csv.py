#!/usr/local/bin/python

"""
This program scrapes ratings from a number of IMDB webpages. It also pulls ratings for 
the corresponding movie from numerous reviewers on Metacritic. These are all written out
to the CSV file ratings_data.csv in the /data directory.
"""

from lxml import html
import requests
import numpy
import unicodecsv as csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def write_out_csv(ratings, titles, reviewers):
	"""Write title, reviewers and ratings to a ccsv file in the /data directory"""
	
	#Add IMDB as the first reviewer
	reviewers.insert(0, 'IMDB')

	#Add header to titles
	titles.insert(0, 'Titles / Reviewers')

	#Add reviewers as the first row
	ratings.insert(0, reviewers)

	#Add titles to the front of every list of ratings
	for title in range(len(titles)):
		ratings[title].insert(0, titles[title])
	print ratings

	with open("../data/ratings_data.csv", "wb") as f:
		writer = csv.writer(f)
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

	#Iterate through each Metacritic url to pull reviewers' corresponding rating
	for iteration in range(len(metacritic_urls)):

		url = metacritic_urls[iteration]
		xpath = "//span[@class='source']"
		#Had to switch to selenium. Trouble scraping - probably related to ToS for CBS
		driver = webdriver.Chrome()
		driver.get(url)
		time.sleep(3)

		#List of all critic sources for a particular movie
		sourceElements = driver.find_elements_by_xpath(xpath)
		number_of_sources = len(sourceElements)
		print number_of_sources

		#List of all critic ratings for a particular movie
		ratingElements = driver.find_elements_by_css_selector('.metascore_w.large.movie.indiv')
		number_of_ratings = len(ratingElements)
		print number_of_ratings
		
		#Check the number of sources match ratings and then add pertinent reviewer ratings to list
		if number_of_sources == number_of_ratings:
			#For each reviewer, iterate through the source elements to find its index
			for reviewer in reviewers:
				for i in range(len(sourceElements)):
					#Once found, append the rating to its spot in the list
					if reviewer == sourceElements[i].text:
						ratings[iteration].append(ratingElements[i].text.encode('utf8'))
						break
					#If the reviwer isn't found in the list of sources then place a -1
					else:
						if i == len(sourceElements) - 1:
							ratings[iteration].append('-1')
		else:
			print "ERROR: Sources don't match ratings!!"
		driver.quit()

	print metacritic_urls
	return

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
			#Each url holds 50 titles
			ratings[50*i + element].append(ratingElements[element].text.encode('utf8'))
	
	return titles


def main():
	
	urls = (
		"http://www.imdb.com/search/title?year=2016,2016&title_type=feature&sort=boxoffice_gross_us,desc",
		"http://www.imdb.com/search/title?year=2015,2015&title_type=feature&sort=boxoffice_gross_us,desc",
		"http://www.imdb.com/search/title?year=2014,2014&title_type=feature&sort=boxoffice_gross_us,desc",
		"http://www.imdb.com/search/title?year=2013,2013&title_type=feature&sort=boxoffice_gross_us,desc",
		"http://www.imdb.com/search/title?year=2012,2012&title_type=feature&sort=boxoffice_gross_us,desc"
		)
	
	reviewers = [
		"Washington Post",
		"The New York Times",
		"New York Post",
		"Los Angeles Times",
		"Wall Street Journal",
		"Chicago Tribune",
		"Boston Globe",
		"Rolling Stone",
		"RogerEbert.com",
		"USA Today",
		"Entertainment Weekly",
		"The A.V. Club"
		]
	
	titles_per_year = 50
	n_total_titles = len(urls) * titles_per_year
	
	ratings = []
	for n in range(n_total_titles):
		ratings.append([])
	
	titles =[]
	
	titles = get_title_IMDB_ratings(urls, ratings, reviewers)
	print titles, ratings
	get_reviewer_ratings(urls, reviewers, ratings)
	print ratings
	write_out_csv(ratings, titles, reviewers)

if __name__ == "__main__":
    main()
