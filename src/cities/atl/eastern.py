from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class Eastern(Venue):
	def __init__(self):
		self.name = "The Eastern"
		self.geo = ('33.745379', '-84.360534')
		self.address = "800 Old Flat Shoals Rd SE, Atlanta, GA 30316"
		self.url = "https://www.easternatl.com/"
		self.schedule = "https://www.easternatl.com/calendar/"
		self.soup = self.getPage()
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigs = []

		# same AXS json api as Terminal West and Variety Playhouse
		# get json file location
		jsonLocH = self.soup.find_all('div', 'c-axs-events__container js-axs-events-section')
		jsonLoc = re.search(r"(?<=data-file=\")(.*?)(\")", str(jsonLocH)).group(1)

		# retreive json file using cache if possible
		json = self.getJSON(jsonLoc)

		# iterate across gigs
		for gigJ in json['events']:
			# Build band list
			bands = gigJ['title']['headlinersText']
			if gigJ['title']['supportingText']:
				bands += " | " + gigJ['title']['supportingText']

			# Build door datetime object
			try:
				dt = datetime.datetime.fromisoformat(gigJ['doorDateTime']) # yyyy-mm-ddTHH:mm:ss
			except (TypeError, ValueError):
				print("Time not found for show at " + self.name)
				continue

			# Get link
			link = "https://www.easternatl.com/events/detail/?event_id=" + gigJ['eventId']

			# instantiate gig
			gig = Gig(bands, dt, link)

			gigs.append(gig)

		return gigs
