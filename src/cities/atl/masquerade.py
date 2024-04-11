from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class Masquerade(Venue):
	def __init__(self):
		self.name = "Masquerade"
		self.geo = ('33.751410','-84.389935')
		self.address = "75 Martin Luther King Jr Dr SW, Atlanta, GA 30303"
		self.url = "https://www.masqueradeatlanta.com/"
		self.schedule = "https://www.masqueradeatlanta.com/events/"
		self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'}
		self.soup = self.getPage(self.headers)
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		gigsH = self.soup.find_all('article', 'event')
		gigs = []
		# Masquerade lists shows they promote at other locations
		# Limit the list to the Masquerade stages
		stageList = "Heaven|Hell|Purgatory|Altar"

		for gigH in gigsH:
			bands = ''
			doors = ''
			url = ''
			cost = ''

			# Get list of bands
			headlinerH = gigH.find('h2', 'js-listTitle')
			supportH = gigH.find('h4', 'js-listSupport')
			headliner = headlinerH.get_text()
			support = ''
			if supportH:
				support = " | " + supportH.get_text()
			bands = headliner + support

			# Build Doors Datetime object
			mxref = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
				'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
			dateH = gigH.find('div', 'eventStartDate')
			date = re.search(r"(content=\")(.*?)(\")", str(dateH)).group(2)
			dsplit = date.split(' ')

			month = int(mxref[dsplit[0]])
			day = int(dsplit[1][:-1])
			year = int(dsplit[2])
			tsplit = dsplit[3].split(':')
			hour = int(tsplit[0])
			minute = int(tsplit[1])
			ampm = dsplit[4]
			if ampm == 'pm':
				hour = hour + 12

			dt = datetime.datetime(year, month, day, hour=hour, minute=minute)

			# get Cost(s)
			costComp = gigH.find('div', 'time-show').get_text()
			costs = re.findall(r"\$[0-9]+|FREE", costComp)
			cost = ''
			if len(costs) > 1:
				cost = costs[0] + ' - ' + costs[-1]
			else:
				cost = costs[0]

			# Check stage in whitelist
			# Skip iteration if location isn't in stageList
			locationH = gigH.find('span', 'js-listVenue').get_text()
			if not re.search(stageList, locationH):
				continue

			# get Link to tickets
			linkH = gigH.find('a', 'btn btn-purple btn-full')
			url = linkH['href']

			# instantiate gig
			gig = Gig(bands, dt, url, cost)
			gigs.append(gig)

		return gigs











