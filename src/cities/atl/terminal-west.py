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
		jsonLocH = self.soup.find_all('div', 'c-axs-events__container js-axs-events-section')
		jsonLoc = re.search(r"(?<=data-file=\")(.*?)(\")", str(jsonLocH)).group(1)
		gigs.append(jsonLoc)

		return gigs










