from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class Earl(Venue):
	def __init__(self):
		self.name = "The Earl"
		self.geo = (33.740969965415346, -84.34589730897736)
		self.address = "488 Flat Shoals Ave SE, Atlanta, GA 30316"
		self.url = "https://badearl.com/"
		self.schedule = "https://badearl.com/"
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

	def getDoors(self):
		datePs = self.soup.find_all('p', 'show-listing-date')
		dates = []
		pass
		
	def getBands(self):
		bandsH = self.soup.find_all('div', re.compile('show-listing-headliner|show-listing-support'))
		bands = []
		for bandH in bandsH:
			band = re.search(r"(?<=>)(.*?)(?=<)", str(bandH))
			bands.append(band.group())
		return bands
	
	def getGigs(self):
		pass

