#!/usr/local/bin/python python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy
import csv


def write_out_csv(ratings):
	with open("../data/test_ratings_data.csv", "wb") as f:
		writer = csv.writer(f, delimiter = ',')
		for j in range(len(ratings)):
		    ratings[j] = map(float, ratings[j])
		writer.writerows(ratings)


ratings = [['8.1', '63', '50', '80', '70', '40', '75', '63', '88', '88'],
['7.4', '75', '90', '80', '70', '80', '75', '88', '88', '75'],
['7.9', '75', '70', '100', '70', '80', '75', '75', '88', '75'],
['6.6', '50', '60', '60', '30', '40', '-1', '63', '75', '75'],
['7.5', '88', '50', '80', '90', '100', '75', '75', '88', '100']]

write_out_csv(ratings)
