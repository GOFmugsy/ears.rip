from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class OrangePeel(Venue):
	def __init__(self):
		self.name = "The Orange Peel"
		self.geo = ('35.591406', '-82.551151')
		self.address = "101 Biltmore Ave, Asheville, NC 28801"
		self.url = "https://theorangepeel.net/"
		self.schedule = "https://theorangepeel.net/events/"
		# the site returns 403 to the default requests user agent
		self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'}
		self.soup = self.getPage(self.headers)
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		# wordpress with the Rockhouse Partners events plugin. Each event is rendered twice
		# (list and grid views), so only read the list view
		gigsH = self.soup.find_all('div', 'rhp-event__single-event--list')
		gigs = []
		# The Orange Peel lists shows they promote at other Asheville venues (Hellbender)
		# Limit the list to The Orange Peel and Pulp, its downstairs room
		stageList = "The Orange Peel|Pulp"

		for gigH in gigsH:
			# Check venue in whitelist
			venueH = gigH.find('div', 'rhp-event__venue-text--list')
			if not venueH or not re.search(stageList, venueH.get_text()):
				continue

			# Get band list
			bands = gigH.find('h2', 'rhp-event__title--list').get_text(strip=True)
			# support acts are separated by <br/>
			supportH = gigH.find('h4', 'rhp-event__subheader--list')
			if supportH:
				for band in supportH.stripped_strings:
					bands += " | " + band

			# Build door datetime object
			# date has no year, e.g. "Thu, Nov 05". Time is "Show: 8 pm | Doors: 7 pm"
			dateStr = gigH.find('div', 'rhp-event__date--list').get_text(strip=True)
			timeStr = gigH.find('span', 'rhp-event__time-text--list').get_text(strip=True)
			try:
				date = self.inferDate(dateStr)
				# use doors time, or show time if doors isn't listed
				time = re.search(r"Doors: ([0-9:]+ [ap]m)", timeStr) or re.search(r"Show: ([0-9:]+ [ap]m)", timeStr)
				timeFormat = "%I:%M %p" if ':' in time.group(1) else "%I %p"
				t = datetime.datetime.strptime(time.group(1), timeFormat).time()
				dt = datetime.datetime.combine(date, t)
			except (AttributeError, ValueError):
				print("Time not found for show at " + self.name + " on " + dateStr)
				continue

			# get Link
			link = gigH.find('a', id='eventTitle')['href']

			# instantiate gig
			gig = Gig(bands, dt, link)
			gigs.append(gig)

		return gigs

	# "Thu, Nov 05" -> the soonest date on or after yesterday that falls on that weekday
	def inferDate(self, dateStr):
		weekday, month, day = re.match(r"(\w+), (\w+) (\d+)", dateStr).groups()
		today = datetime.date.today()
		for year in range(today.year, today.year + 3):
			try:
				d = datetime.datetime.strptime(str(year) + " " + month + " " + day, "%Y %b %d").date()
			except ValueError:
				continue
			if d.strftime("%a") == weekday and d >= today - datetime.timedelta(days = 1):
				return d
		raise ValueError("can not work out year for " + dateStr)
