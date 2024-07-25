from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class Eulogy(Venue):
	def __init__(self):
		self.name = "Eulogy"
		self.geo = ('35.588552', '-82.553934')
		self.address = "10 Buxton Ave, Asheville, NC 28801"
		self.url = "https://burialbeer.com/pages/eulogy"
		self.schedule = "https://dice.fm/venue/eulogy-7bd7"
		self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'}
		self.soup = self.getPage(self.headers)
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigsH = self.soup.find_all('div', 'EventParts__EventBlock-sc-db999af1-9 gZUtAO') # Seems consistent but need to keep an eye on it
		gigs = []
		
		for gigH in gigsH:
			bands = ''
			doors = ''
			url = ''
			cost = ''

			# Get band list
			bandH = gigH.find('a', 'EventParts__EventName-sc-db999af1-0 iOiUbH')
			bands = bandH.get_text()

			print("DEBUG: " + bands)

			# Build doors datetime
			mxref = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
			'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

			dateH = gigH.find('time', 'event-date').get_text()
			dsplit = dateH.split(' ')
			dow = dsplit[0][0:-1]
			month = dsplit[1]
			if(len(month) > 3):
				month = month[0:3]
			day = dsplit[2][0:-1]

			timeH = gigH.find('time', re.compile('event-time-localized'))
			time = timeH.get_text()
			tsplit = time.split(':')
			hour = int(tsplit[0])
			minute = int(tsplit[1][0:2])
			ampm = tsplit[1][-2:]
			if ampm.lower() == 'pm' and hour < 12:
				hour = int(hour) + 12

			dt = datetime.datetime(2024, mxref[month.upper()], int(day), hour=int(hour), minute=int(minute))

			# Get Cost(s)
			costH = gigH.find_all('p', {'style': 'white-space:pre-wrap;'})
			cost = 'NOT FOUND'
			try:
				for i in costH:
					if re.search('\$[0-9]+', i.get_text()):
						cost = re.search(r"(\$[0-9]+)", i.get_text()).group(0)
			except:
				print('can not find cost for gig at ' + self.name + ' on ' + str(dt))

			# Get Link
			linkH = gigH.find('a', 'eventlist-title-link')
			link = 'NO LINK'
			try:
				link = self.url[0:-1] + linkH['href']
			except:
				print('can not find link for gig at ' + self.name + ' on ' + str(dt))

			gig = Gig(bands, dt, link, cost)
			gigs.append(gig)

		return gigs

