from bs4 import BeautifulSoup
import re
import datetime
from zoneinfo import ZoneInfo

from ..Venue import Venue
from ..Gig import Gig

class Boggs(Venue):
	def __init__(self):
		self.name = "Boggs Social & Supply"
		self.geo = ('33.737481', '-84.430208')
		self.address = "1310 White St SW, Atlanta, GA 30310"
		self.url = "https://www.boggssocial.com/"
		self.schedule = "https://www.boggssocial.com/events"
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigs = []

		# squarespace site - the events page returns its data as json with ?format=json
		# 'upcoming' covers a couple months, 'past' and pagination are for older events
		json = self.getJSON(self.schedule + "?format=json")

		for gigJ in json['upcoming']:
			# Title is the lineup (or the event name for non-band nights)
			bands = gigJ['title'].strip()

			# Build door datetime object. startDate is epoch milliseconds (UTC) with stray
			# milliseconds, so round to the minute to keep Gig.uid stable
			dt = datetime.datetime.fromtimestamp(gigJ['startDate'] / 1000, ZoneInfo("America/New_York"))
			dt = dt.replace(tzinfo=None, second=0, microsecond=0)

			# get Link - the event page on boggssocial.com has the ticket link
			link = "https://www.boggssocial.com" + gigJ['fullUrl']

			# instantiate gig
			gig = Gig(bands, dt, link)
			gigs.append(gig)

		return gigs
