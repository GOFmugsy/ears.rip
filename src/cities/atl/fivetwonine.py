from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class Fivetwonine(Venue):
	def __init__(self):
		self.name = "529"
		self.geo = ('33.739934', '-84.345148')
		self.address = "529 Flat Shoals Ave SE, Atlanta, GA 30316"
		self.url = "https://529atlanta.com/"
		self.schedule = "https://529atlanta.com/"
		self.soup = self.getPage()
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigsH = self.soup.find_all('div', 'event-card')
		gigs = []
		
		# Find bands
		for gigH in gigsH:
			bands = ''
			doors = ''
			url = ''
			cost = ''

			# Get band list
			headlinersH = gigH.find_all('h3', 'headliner')
			headliners = ""
			supportH = gigH.find_all('div', 'bands')
			support = ""
			for h in headlinersH:
				if len(headliners) < 1:
					headliners += h.get_text()
				else:
					headliners += " | " + h.get_text()
			for b in supportH:
				for bsplit in b.get_text().split(' | '):
					support += " | " + str(bsplit)
			bands = headliners + support
			bands.strip()
			
			# Build Door Datetime object
			mxref = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
				'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

			dateH = gigH.find('div', 'head')
			date = dateH.get_text().split('\n')[2]

			timeH = gigH.find_all('div', 'event-meta')
			time = re.search(r"[0-9]+:[0-9]+ [ap]m", str(timeH[0])).group()
			tsplit = time.split(' ')
			hour = re.search(r"(^[0-9]+)(:)", tsplit[0]).group(1)
			ampm = tsplit[1]
			if ampm == 'pm' and int(hour) != 12:
				hour = int(hour) + 12

			dsplit = date.split(' ')
			dt = datetime.datetime(int(dsplit[2]), int(mxref[dsplit[0].upper()]), int(dsplit[1][0:2]), hour=int(hour))

			# get Cost(s)
			costH = gigH.find_all('div', 'event-meta')
			cost = 'NOT FOUND'
			try:
				# pretty damn loose
				cost = re.search(r"(\$.*)|FREE", str(costH[0].get_text())).group(0)
			except:
				print('can not find cost for gig at ' + self.name + ' on ' + date)

			# get Link
			linkH = gigH.find('a', 'fl-button', string=re.compile('.*Info.*'))
			link = 'NO LINK'
			try:
				link = linkH['href']
			except:
				print('can not find link for gig at ' + self.name + ' on ' + date)
				
			# instantiate gig
			gig = Gig(bands, dt, link, cost)
			gigs.append(gig)

		return gigs










