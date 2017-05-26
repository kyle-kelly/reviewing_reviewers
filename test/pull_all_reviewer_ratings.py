#!/usr/local/bin/python python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_reviewer_ratings(driver, url, ratings, reviewers, iter):
	"""Navigate to Metacritic and pull reviewer ratings"""

	xpath_titles = "//h3[@class='lister-item-header']/a"
	titleElements = driver.find_elements_by_xpath(xpath_titles)

	for j in range(0,len(titleElements)):
		driver.get(url)
		titleElements = driver.find_elements_by_xpath(xpath_titles)
		titleElements[j].click()
		driver.find_element_by_class_name('titleReviewBarSubItem').click()
		xpath = "//div[@class='see-more']/a"
		urlElement = driver.find_element_by_xpath(xpath)
		meta_url = urlElement.get_attribute("href")
		print meta_url
		chars = set('?')
		if any((c in chars) for c in meta_url):
			meta_url, trash = meta_url.split("?",1)			
		meta_url = meta_url + "/critic-reviews"
		print meta_url
		driver.get(meta_url)

		#List of all critic sources for a particular movie
		xpath = "//span[@class='source']"
		sourceElements = driver.find_elements_by_xpath(xpath)
		n_sources = len(sourceElements)
		print n_sources
		
		#List of all critic ratings for a particular movie
		ratingElements = driver.find_elements_by_css_selector('.metascore_w.large.movie.indiv')
		n_ratings = len(ratingElements)
		print n_ratings
		
		#Check the number of sources match ratings and then add pertinent reviews to list
		if n_sources == n_ratings:
			for reviewer in reviewers:
				for i in range(len(sourceElements)):
					if reviewer == sourceElements[i].text:
						ratings[50*iter + j+1].append(ratingElements[i].text)
						break
					else:
						if i == len(sourceElements) - 1:
							ratings[50*iter + j+1].append('N/A')
			print ratings[50*iter + j+1]
		else:
			print "ERROR: Sources don't match ratings!!"


def get_title_IMDB_ratings(driver, urls, ratings, reviewers):
	"""Pull title and IMDB ratings"""

	titles = []
	xpath_titles = "//h3[@class='lister-item-header']/a"

	for i in range(len(urls)):
		driver.get(urls[i])
		titleElements = driver.find_elements_by_xpath(xpath_titles)
		for element in titleElements:
			titles.append(element.text)
		ratingElements = driver.find_elements_by_class_name('ratings-imdb-rating')
		for element in ratingElements:
			ratings[0].append(element.get_attribute('data-value'))

		get_reviewer_ratings(driver, urls[i], ratings, reviewers, i)

	print titles
	print ratings

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
	ratings = []
	for n in range(n_total_titles + 1):
		ratings.append([])

	get_title_IMDB_ratings(driver, urls, ratings, reviewers)


if __name__ == "__main__":
    main()
