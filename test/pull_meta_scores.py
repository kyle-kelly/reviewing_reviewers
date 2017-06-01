from lxml import html
import requests

url = "http://www.metacritic.com/movie/rogue-one-a-star-wars-story/critic-reviews"
page = requests.get(url)
tree = html.fromstring(page.content)

#List of all critic sources for a particular movie
xpathselector="//div[@class='metascore_w large movie negative indiv']/text()"
metaElement = tree.xpath(xpathselector)
print metaElement
