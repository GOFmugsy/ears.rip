from bs4 import BeautifulSoup
import re
import datetime
import json
from zoneinfo import ZoneInfo

from ..Venue import Venue
from ..Gig import Gig

class Eulogy(Venue):
	def __init__(self):
		self.name = "Eulogy"
		self.geo = ('35.588375', '-82.553912')
		self.address = "10 Buxton Ave, Asheville, NC 28801"
		self.url = "https://burialbeer.com/pages/eulogy"
		self.schedule = "https://dice.fm/venue/eulogy-7bd7?lng=en-US"
		# dice.fm is behind cloudflare, which challenges the default requests user agent
		self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'}
		self.soup = self.getPage(self.headers)
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigs = []

		# tickets are sold on dice.fm. The venue page includes its upcoming events as
		# schema.org json-ld: a Place with an 'event' list
		place = None
		for script in self.soup.find_all('script', type='application/ld+json'):
			data = json.loads(script.string)
			if isinstance(data, dict) and data.get('@type') == 'Place':
				place = data
		if place is None:
			print("can not find event list for " + self.name)
			return gigs

		for gigJ in place.get('event', []):
			# Get band list - the name is the lineup, e.g. "Havok w/ Hellripper, Slackjaw & Xoth"
			bands = re.sub(r"\s+w/\s+", " | ", gigJ['name'].strip())

			# Build door datetime object. dice only lists the start time, with a utc offset
			try:
				dt = datetime.datetime.fromisoformat(gigJ['startDate'])
				dt = dt.astimezone(ZoneInfo("America/New_York")).replace(tzinfo=None)
			except (KeyError, ValueError):
				print("Time not found for show at " + self.name)
				continue

			# get Link
			link = gigJ['url']

			# instantiate gig
			gig = Gig(bands, dt, link)
			gigs.append(gig)

		return gigs
