from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class StarBar(Venue):
	def __init__(self):
		self.name = "Star Community Bar"
		self.geo = ('33.766278', '-84.348883')
		self.address = "437 Moreland Ave NE, Atlanta, GA 30307"
		self.url = "https://www.starbaratl.bar/"
		self.schedule = "https://www.freshtix.com/search?utf8=%E2%9C%93&query=Star+Bar&start=&end=&state=GA&category=&commit=Search"
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
			dollars = "not found"
			try:
				dollars = re.findall(r"\$[0-9]+", descStr)[0]
			except:
				print("dollars not found for: " + str(bands))

			if len(dollars) == 1:
				cost = str(dollars[0])
			else:
				cost = str(dollars[0]) + ' - ' + str(dollars[-1])
			
			# get Link
			urlPrefix = 'https://www.freshtix.com/events/'
			urlPostfix = gigJ['url_name']
			url = urlPrefix + urlPostfix
				
			# instantiate gig
			gig = Gig(bands, dt, url, cost)
			gigs.append(gig)

		return gigs










