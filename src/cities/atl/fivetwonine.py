from urllib.request import urlopen
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
		self.schedule = "https://529atlanta.com/calendar/"
		self.soup = self.getPage()
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigsH = self.soup.find_all('div', 'event-container-single')
		gigs = []
		
		# Find bands
		for gigH in gigsH:
			bands = ''
			doors = ''
			url = ''
			cost = ''

			# Get band list
			bandH = gigH.find_all(re.compile('h[34]'), re.compile('event-headliners|event-bands'))
			headliner = re.search(r"(?<=>)(.*?)(?=<)", str(bandH[0])).group()
			support = ''
			if len(bandH) > 1:
				support = ' | ' + re.search(r"(?<=>)(.*?)(?=<)", str(bandH[1])).group()
			bands = headliner + support
		
			# Build Door Datetime object
			mxref = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
				'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

			dateH = gigH.find_all('h1', 'event-date-single')
			date = re.search(r"(?<=span class=\"right\">)(.*?)(?=<)", str(dateH)).group()

			timeH = gigH.find_all('p', 'event-meta')
			time = re.search(r"[0-9]+:[0-9]+ [ap]m", str(timeH[0])).group()
			tsplit = time.split(' ')
			hour = re.search(r"(^[0-9]+)(:)", tsplit[0]).group(1)
			ampm = tsplit[1]
			if ampm == 'pm':
				hour = int(hour) + 12

			dsplit = date.split(' ')
			dt = datetime.datetime(int(dsplit[2]), int(mxref[dsplit[0]]), int(dsplit[1][0:2]), hour=hour)

			# get Cost(s)
			costH = gigH.find_all('p', 'event-meta')
			cost = 'NOT FOUND'
			try:
				# pretty damn loose
				cost = re.search(r"(\$.*)|FREE", str(costH[0])).group(0)
			except:
				print('can not find cost for gig at ' + self.name + ' on ' + date)

			# get Link
			linkH = gigH.find_all('a', 'button')
			link = 'NO LINK'
			try:
				link = re.search('(href=")(' + self.url + '.*?)(">Info)', str(linkH)).group(2)
			except:
				print('can not find link for gig at ' + self.name + ' on ' + date)
				
			# instantiate gig
			gig = Gig(bands, dt, link, cost)
			gigs.append(gig)

		return gigs










