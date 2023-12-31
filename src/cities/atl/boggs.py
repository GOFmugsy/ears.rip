from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class Boggs(Venue):
	def __init__(self):
		self.name = "Boggs Social"
		self.geo = ('33.737481', '-84.430208')
		self.address = "1310 White St SW, Atlanta, GA 30310"
		self.url = "https://www.boggssocial.com/"
		self.schedule = "https://www.freshtix.com/search?category=&end=&query=Boggs%20Social&start=&state=GA"
		self.soup = self.getPage()
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigsH = self.soup.find_all('tr')
		gigs = []
		
		# Find bands
		for gigH in gigsH:
			bands = ''
			doors = ''
			url = ''
			cost = ''

			# Get band list
		
			# Build Door Datetime object

			# get Cost(s)

			# get Link
				
			# instantiate gig
			# gig = Gig(bands, dt, link, cost)
			# gigs.append(gig)

			gigs.append(gigH)

		return gigs










