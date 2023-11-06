from abc import ABC, abstractmethod
import os
import time, datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

class Venue(ABC):
	def __init__(self, name, latlong, address, homepage, schedule):
		self.name = name
		self.latlong = latlong
		self.address = address
		self.homepage = homepage
		self.schedule = schedule
		self.venues = []
		self.gigs = []

	def __str__(self):
		return f" "

	def addGig(self, gig):
		self.gigs.append(gig)

	# universal check if the current venue's schedule page has already been checked in the last 24 hours
	# If it has been, use the cached version. If not, then pull it and cache it.
  # 
  # Returns a BeautifulSoup object
	def getPage(self):
		cache = '../tmp'
		soup = ''
		cachedFound = False
		html = ''

		for f in os.listdir(cache):
			if f == self.name + '.html':
				cachedPage = os.path.join(cache, f)
				print("Found cached " + cachedPage)
				# mTime = datetime.fromtimestamp(os.path.getmtime(cachedPage), tz=timezone.utc)
				mTime = datetime.datetime.fromtimestamp(os.path.getmtime(cachedPage))
				curTime = datetime.datetime.now()
				cacheAge = curTime - mTime
				print("Cached " + cachedPage + " is " + str(cacheAge) + " old")
				page = ''

				if os.path.isfile(cachedPage) and cacheAge < datetime.timedelta(hours = 24): # only use if less than 24 hours old
					print("loading cached: " + cachedPage)
					page = open(cachedPage)
					html = page.read()
					cachedFound = True
		
		if not cachedFound:
			print("writing to cache: " + os.path.join(cache, self.name + '.html'))
			page = urlopen(self.schedule)
			html = page.read().decode("utf-8")
			with open(os.path.join(cache, self.name + '.html'), 'w') as c:
				c.write(page.read().decode("utf-8"))

		soup = BeautifulSoup(html, "html.parser")
		return soup
		

	# Should return chronological list of all links for each show
	def getLinks(self):
		links = []
		for gig in self.gigs:
			links.append(gig.url)
		return links

	# Should return chronological datetime object with date and time of doors
	def getDoors(self):
		doors = []
		for gig in self.gigs:
			doors.append(gig.doors)
		return doors

	# Should return chronological cost for each show
	def getCost(self):
		costs = []
		for gig in self.gigs:
			costs.append(gig.cost)
		return costs

	# Should return a chronological list of ALL bands in the gig
	def getBands(self):
		bands = []
		for gig in self.gigs:
			bands.append(gig.bands)
		return bands

	# Should return a chronological list of ALL gigs
	def getGigs(self):
		return self.gigs

	# Should build, store, and return the list of all gigs as Gig objects
	@abstractmethod
	def fetchGigs(self):
		pass
