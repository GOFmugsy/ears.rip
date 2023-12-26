from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class Fivetwonine(Venue):
	def __init__(self):
		self.name = "Terminal West"
		self.geo = ('33.781358', '-84.415787')
		self.address = "887 West Marietta St NW STE C, Atlanta, GA 30318"
		self.url = "https://terminalwestatl.com/"
		self.schedule = "https://terminalwestatl.com/calendar"
		self.soup = self.getPage()
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigs = []

		# uses a json api for the sckhedule
		# get json file location
		jsonLocH = self.soup.find_all('div', 'c-axs-events__container js-axs-events-section')
		jsonLoc = re.search(r"(?<=data-file=\")(.*?)(\")", str(jsonLocH)).group(1)

		# retreive json file using cache if possible
		json = self.getJSON(jsonLoc)

		# iterate across gigs
		for gigJ in json['events']:
			bands = ''
			doors = ''
			url = ''
			cost = ''

			# Build band list
			print(gigJ['title']['headlinersText'])
			bands = gigJ['title']['headlinersText']
			if gigJ['title']['supportingText'] is not None:
				bands += " | " + gigJ['title']['supportingText']

			# Build door datetime object
			doors = gigJ['doorDateTime']

			gigs.append(bands)

		return gigs










