#!/usr/local/bin/python python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import gettext


def get_title_IMDB_ratings(driver, urls):
	"""Pull title"""

	titles = []
	ratings = []
	xpath_titles = "//h3[@class='lister-item-header']/a"

	for url in urls:
		driver.get(url)
		titleElements = driver.find_elements_by_xpath(xpath_titles)
		for element in titleElements:
			titles.append(element.text)
		ratingElements = driver.find_elements_by_class_name('ratings-imdb-rating')
		for element in ratingElements:
			ratings.append(element.get_attribute('data-value'))
	print titles
	print ratings
	print len(titles)
	print len(ratings)


def main():
	"""Test to pull titles and IMDB rating from IMDB url"""

	#Initialize 
	driver = webdriver.Chrome()
	urls = ("http://www.imdb.com/search/title?year=2016,2016&title_type=feature&sort=boxoffice_gross_us,desc",
		"http://www.imdb.com/search/title?year=2015,2015&title_type=feature&sort=boxoffice_gross_us,desc",
		"http://www.imdb.com/search/title?year=2014,2014&title_type=feature&sort=boxoffice_gross_us,desc")
	titles_per_year = 50
	n_total_titles = len(urls) * titles_per_year

	get_title_IMDB_ratings(driver, urls)


if __name__ == "__main__":
    main()
