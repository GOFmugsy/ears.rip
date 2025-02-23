from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class AisleFive(Venue):
	def __init__(self):
		self.name = "Aisle 5"
		self.geo = (33.764263, -84.350276)
		self.address = "1123 Euclid Ave NE, Atlanta, GA 30307"
		self.url = "https://aisle5atl.com/"
		self.schedule = "https://aisle5atl.com/"
		self.soup = self.getPage()
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigsH = self.soup.find_all('div', 'mdc-card')
		gigs = []
		
		for gigH in gigsH:
			bands = ''
			doors = ''
			url = ''
			cost = ''

			# Get band list
			bandH = gigH.find_all('div', re.compile('event-info-block'))
			headliner = gigH.find('p', 'headliners')
			support = gigH.find('p', 'supporting-talent')
			bands = headliner.get_text()
			if(support.get_text()):
				bands += " | " + support.get_text()

			# Build doors datetime
			mxref = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
			'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

			dateH = gigH.find('p', 'event-date').get_text()
			dsplit = dateH.split(' ')
			dow = dsplit[0]
			month = dsplit[1]
			day = dsplit[2]

			timeH = gigH.find('span', 'see-showtime').get_text()
			tsplit = timeH.split(':')
			hour = int(tsplit[0])
			minute = int(tsplit[1][0:2])
			ampm = tsplit[1][-2:]
			if ampm.lower() == 'pm' and hour < 12:
				hour = int(hour) + 12

			dt = datetime.datetime(2025, mxref[month.upper()], int(day), hour=int(hour), minute=int(minute))

			# Get Cost(s)
			costH = gigH.find_all('span', 'price')
			cost = 'NOT FOUND'
			try:
				cost = re.search(r"(\$[0-9]+)", str(costH[0])).group(0)
			except:
				print('can not find cost for gig at ' + self.name + ' on ' + str(dt))

			# Get Link
			linkH = gigH.find('p', 'event-title')
			link = 'NO LINK'
			try:
				link = re.search('(href=")(.*?)(" target)', str(linkH)).group(2)
			except:
				print('can not find link for gig at ' + self.name + ' on ' + str(dt))

			gig = Gig(bands, dt, link, cost)
			gigs.append(gig)

		return gigs

