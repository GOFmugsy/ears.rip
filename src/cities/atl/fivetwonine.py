from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from ..Venue import Venue

class Fivetwonine(Venue):
	def __init__(self):
		self.name = "529"
		self.geo = ('33.739934', '-84.345148')
		self.address = "529 Flat Shoals Ave SE, Atlanta, GA 30316"
		self.url = "https://529atlanta.com/"
		self.schedule = "https://529atlanta.com/calendar/"
		self.page = urlopen(self.schedule)
		self.html = self.page.read().decode("utf-8")
		self.soup = BeautifulSoup(self.html, "html.parser")

	def getLinks(self):
		links = self.soup.find_all('a', 'cl-element-featured_media__anchor')
		urls = []
		for link in links:
			url = re.search(r"https://badearl.com/show/.*?/", str(link))
			urls.append(url)
		return urls

	def getDates(self):
		datePs = self.soup.find_all('p', 'show-listing-date')
		dates = []
	
	def getDoors(self):
		pass
		
	def getBands(self):
		bands = self.soup.find_all('div', re.compile('show-listing-headliner|show-listing-support'))
		return bands

	def getGigs(self):
		pass


