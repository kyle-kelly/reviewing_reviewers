#!/usr/local/bin/python python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy
import csv


def write_out_csv(ratings):
	with open("../data/ratings_data.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ',')
		for j in range(len(ratings)):
		    ratings[j] = map(float, ratings[j])
		writer.writerows(ratings)


def get_reviewer_ratings(driver, urls, ratings, reviewers):
	"""Navigate to Metacritic and pull reviewer ratings"""

	for iteration in range(len(urls)):

		url = urls[iteration]
		driver.get(url)
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
							ratings[50*iteration + j].append(ratingElements[i].text.encode('utf-8'))
							break
						else:
							if i == len(sourceElements) - 1:
								ratings[50*iteration + j].append('-1')
				write_out_csv(ratings)
			
			else:
				print "ERROR: Sources don't match ratings!!"

	return ratings


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
		for element in range(len(ratingElements)):
			ratings[50*i + element].append(ratingElements[element].get_attribute('data-value').encode('utf-8'))

	print ratings
	
	return titles, ratings


def main():

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
	for n in range(n_total_titles):
		ratings.append([])
	titles =[]
	
	titles, ratings = get_title_IMDB_ratings(driver, urls, ratings, reviewers)
	ratings = get_reviewer_ratings(driver, urls, ratings, reviewers)


if __name__ == "__main__":
    main()
