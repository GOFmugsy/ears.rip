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
		self.schedule = "https://badearl.com/"
		self.soup = self.getPage()
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigsH = self.soup.find_all('div', 'show-listing-right')
		gigs = []
		
		for gigH in gigsH:
			bands = ''
			doors = ''
			url = ''
			cost = ''

			# Get band list
			bandH = gigH.find_all('div', re.compile('show-listing-headliner|show-listing-support'))
			headliner = re.search(r"(?<=>)(.*?)(?=<)", str(bandH[0])).group()
			support = ''
			if len(bandH) > 1:
				for i in range(1, len(bandH)):
					support = support + ' | ' + re.search(r"(?<=>)(.*?)(?=<)", str(bandH[i])).group()
			bands = headliner + support

			# Build doors datetime
			mxref = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
			'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

			dateH = gigH.find_all('p', 'show-listing-date')
			date = re.search(r"(?<=show-listing-date\">)(.*?)(?=<)", str(dateH)).group()
			dsplit = date.split(' ')

			timeH = gigH.find_all('p', 'show-listing-time')
			timestr = re.search(r"(?<=show-listing-time\">)(.*?)(?= *)([ap]m*)", str(timeH[0])).group()
			time = re.search("([0-9]+):([0-9]+)\s*([ap]m)", timestr)
			hour = int(time.group(1))
			minute = int(time.group(2))
			ampm = time.group(3)
			if ampm.lower() == 'pm' and hour < 12:
				hour = int(hour) + 12

			dt = datetime.datetime(int(dsplit[3]), int(mxref[dsplit[1][0:3].upper()]), int(re.search('[0-9]+', dsplit[2]).group()), hour=hour, minute=minute)

			# Get Cost(s)
			costH = gigH.find_all('p', 'show-listing-price')
			cost = 'NOT FOUND'
			try:
				cost = re.search(r"(\$[0-9]+)", str(costH[0])).group(0)
			except:
				print('can not find cost for gig at ' + self.name + ' on ' + str(dt))

			# Get Link
			linkH = gigH.find_all('a', string="More Info")
			link = 'NO LINK'
			try:
				link = re.search('(href=")(' + self.url + '.*?)(">)', str(linkH)).group(2)
			except:
				print('can not find link for gig at ' + self.name + ' on ' + str(dt))

			gig = Gig(bands, dt, link, cost)
			gigs.append(gig)

		return gigs

