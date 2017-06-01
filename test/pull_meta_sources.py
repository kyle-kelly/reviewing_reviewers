#!/usr/local/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "http://www.metacritic.com/movie/rogue-one-a-star-wars-story/critic-reviews"
xpath="//span[@class ='source']/a"

#List of all critic sources for a particular movie
driver = webdriver.Chrome()
driver.get(url)
sourceElements = driver.find_elements_by_xpath(xpath)
n_sources = len(sourceElements)
print n_sources

ratingElements = driver.find_elements_by_css_selector('.metascore_w.large.movie.indiv')
n_ratings = len(ratingElements)
print n_ratings

if n_sources == n_ratings:
	for i in range(len(sourceElements)):
		print sourceElements[i].text
		print ratingElements[i].text
else:
	print "ERROR: Sources don't match ratings!!"
