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
		self.soup = self.getPage()
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigsH = self.soup.find_all('div', 'show-listing-right')
		gigs = []

		for gigH in gigsH:
			bands = ''
			doors = ''
			url = ''
			cost = ''

			bandH = gigH.find_all('div', re.compile('show-listing-headliner|show-listing-support'))
			headliner = re.search(r"(?<=>)(.*?)(?=<)", str(bandH[0])).group()
			support = ''
			if len(bandH) > 1:
				for i in range(1, len(bandH)):
					support = support + ' | ' + re.search(r"(?<=>)(.*?)(?=<)", str(bandH[i])).group()
			bands = headliner + support

			gigs.append(bands)
			
			

		
		return gigs

