#!/usr/local/bin/python python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import gettext


def get_title_IMDB_ratings(driver, urls):
	"""Pull title"""

	titles = []
	xpath = "//h3[@class='lister-item-header']/a"

	for url in urls:
		driver.get(url)
		titleElements = driver.find_elements_by_xpath(xpath)
		for element in range(len(titleElements)):
			titles.append(titleElements[element].text)
	print titles
	print len(titles)


def main():
	"""Test to pull titles from IMDB url"""

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
