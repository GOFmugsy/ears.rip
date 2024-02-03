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
		self.schedule = "https://www.freshtix.com/search?utf8=%E2%9C%93&query=The+EARL&start=&end=&state=GA&category=&commit=Search"
		self.soup = self.getPage()
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		json = self.getJSON(self.schedule)
		gigs = []
		
		# Find bands
		for gigJ in json['events']:
			bands = ''
			doors = ''
			url = ''
			cost = ''

			# Get band list
			bands = gigJ['name']
		
			# Build Door Datetime object
			doorsStr = gigJ['start_time']
			year = re.search('^[0-9]{4}', doorsStr).group()
			month = re.search('(-)([0-9]{2})(-)', doorsStr).group(2)
			day = re.search('(-)([0-9]{2})(T)', doorsStr).group(2)
			hour = re.search('(T)([0-9]{2})(:)', doorsStr).group(2)
			minute = re.search('([0-9]{2}:)([0-9]{2})(:)', doorsStr).group(2)
			dt = datetime.datetime(int(year), int(month), int(day), hour=int(hour), minute=int(minute))

			# get Cost(s)
			descStr = gigJ['long_description']
			if descStr:
				dollars = re.findall(r"\$[0-9]+", descStr)
				if len(dollars) == 1:
					cost = str(dollars[0])
				elif len(dollars) > 1:
					cost = str(dollars[0]) + ' - ' + str(dollars[-1])
				else:
					cost = "cost not found"
			else:
				cost = "cost not found"
			
			# get Link
			urlPrefix = 'https://www.freshtix.com/events/'
			urlPostfix = gigJ['url_name']
			url = urlPrefix + urlPostfix
				
			# instantiate gig
			gig = Gig(bands, dt, url, cost)
			gigs.append(gig)

		return gigs










