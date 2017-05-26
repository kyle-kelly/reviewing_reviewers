#!/usr/local/bin/python python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def get_reviewer_ratings(driver, xpath_titles, reviewers):
	"""Navigate to Metacritic and pull reviewer ratings"""

	ratings = []

	driver.find_element_by_xpath(xpath_titles).click()
	
	driver.find_element_by_class_name('titleReviewBarSubItem').click()
	xpath = "//div[@class='see-more']/a"
	urlElement = driver.find_element_by_xpath(xpath)
	url = urlElement.get_attribute("href")
	print url
	chars = set('?')
	if any((c in chars) for c in url):
		url, trash = url.split("?",1)			
	url = url + "/critic-reviews"
	print url
	driver.get(url)

	xpath = "//span[@class='source']"
	sourceElements = driver.find_elements_by_xpath(xpath)
	n_sources = len(sourceElements)
	print n_sources
	
	ratingElements = driver.find_elements_by_css_selector('.metascore_w.large.movie.indiv')
	n_ratings = len(ratingElements)
	print n_ratings
	
	if n_sources == n_ratings:
		for reviewer in reviewers:
			for i in range(len(sourceElements)):
				if reviewer == sourceElements[i].text:
					ratings.append(ratingElements[i].text)
		print ratings
	else:
		print "ERROR: Sources don't match ratings!!"


def get_title_IMDB_ratings(driver, urls, reviewers):
	"""Pull title and IMDB ratings"""

	titles = []
	ratings = []
	xpath_titles = "//h3[@class='lister-item-header']/a"

	for url in urls:		
		driver.get(url)
		get_reviewer_ratings(driver, xpath_titles, reviewers)


def main():
	"""Test to pull titles and IMDB rating from IMDB url"""

	#Initialize 
	driver = webdriver.Chrome()
	urls = ("http://www.imdb.com/search/title?year=2016,2016&title_type=feature&sort=boxoffice_gross_us,desc",
		"http://www.imdb.com/search/title?year=2015,2015&title_type=feature&sort=boxoffice_gross_us,desc",
		"http://www.imdb.com/search/title?year=2014,2014&title_type=feature&sort=boxoffice_gross_us,desc")
	reviewers = ("Washington Post",
		"The New York Times",
		"The Telegraph",
		"Los Angeles Times",
		"Wall Street Journal",
		"Chicago Tribune",
		"Boston Globe",
		"Rolling Stone",
		"RogerEbert.com")
	titles_per_year = 50
	n_total_titles = len(urls) * titles_per_year

	get_title_IMDB_ratings(driver, urls, reviewers)


if __name__ == "__main__":
    main()
