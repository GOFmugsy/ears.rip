from bs4 import BeautifulSoup
import re
import datetime

from ..Venue import Venue
from ..Gig import Gig

class GreyEagle(Venue):
	def __init__(self):
		self.name = "The Grey Eagle"
		self.geo = ('35.587114', '-82.564460')
		self.address = "185 Clingman Ave, Asheville, NC 28801"
		self.url = "https://www.thegreyeagle.com/"
		self.schedule = "https://www.thegreyeagle.com/calendar/"
		# the site returns 403 to the default requests user agent
		self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'}
		self.soup = self.getPage(self.headers)
		self.gigs = self.fetchGigs()

	def fetchGigs(self):
		# wordpress with the Rockhouse Partners events plugin, same as The Orange Peel. Each
		# event is rendered twice (list and grid views), so only read the list view.
		# Every event is at the Grey Eagle (Music Hall, Special Event, or Patio Stage)
		gigsH = self.soup.find_all('div', 'rhp-event__single-event--list')
		gigs = []

		for gigH in gigsH:
			# Get band list
			bands = gigH.find('h2', 'rhp-event__title--list').get_text(strip=True)
			# support acts are separated by <br/> and start with "with" or "ft.", e.g.
			# "with Madeleine Kelson". Some events put the promoter here instead of a band
			supportH = gigH.find('h4', 'rhp-event__subheader--list')
			if supportH:
				for band in supportH.stripped_strings:
					if re.search(r"presents?$", band, re.IGNORECASE):
						continue
					band = re.sub(r"^(with|w/|ft\.?|feat\.?|featuring)\s+", "", band, flags=re.IGNORECASE)
					bands += " | " + band

			# Build door datetime object
			# date has no year, e.g. "Thu, Nov 05". Time is "Doors: 7 pm // Show: 8 pm"
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
