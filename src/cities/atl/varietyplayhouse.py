from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class VarietyPlayhouse(Venue):
	def __init__(self):
		self.name = "Variety Playhouse"
		self.geo = ('33.763732', '-84.351125')
		self.address = "1099 Euclid Ave NE, Atlanta, GA 30307"
		self.url = "https://www.variety-playhouse.com/"
		self.schedule = "https://www.variety-playhouse.com/calendar/"
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
			bands = gigJ['title']['headlinersText']
			if gigJ['title']['supportingText'] is not None:
				bands += " | " + gigJ['title']['supportingText']

			# Build door datetime object
			doors = gigJ['doorDateTime'] # yyyy-mm-ddTHH:mm:ss
			try:
				year = re.search('^[0-9]{4}', doors).group()
				month = re.search('(-)([0-9]{2})(-)', doors).group(2)
				day = re.search('(-)([0-9]{2})(T)', doors).group(2)
				hour = re.search('(T)([0-9]{2})(:)', doors).group(2)
				minute = re.search('([0-9]{2}:)([0-9]{2})(:)', doors).group(2)
				dt = datetime.datetime(int(year), int(month), int(day), hour=int(hour), minute=int(minute))
			except:
				print("Time not found for show at " + self.name)
				continue

			# Get costs(s)
			cost = "NOT FOUND"
			if gigJ['ticketPrice'] != None:
				cost = gigJ['ticketPrice']
			if gigJ['doorPrice'] != None:
				cost += " - " + gigJ['doorPrice']

			# Get link
			link = gigJ['ticketing']['url']

			# instantiate gig
			gig = Gig(bands, dt, link, cost)
				
			gigs.append(gig)

		return gigs










