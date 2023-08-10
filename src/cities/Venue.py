from abc import ABC, abstractmethod

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

	# Should return chronological list of all links for each show
	@abstractmethod
	def getLinks(self):
		pass

	# Should return chronological datetime object with date and time of doors
	@abstractmethod
	def getDoors(self):
		pass

	# Should return chronological cost for each show
	@abstractmethod
	def getCost(self):
		pass

	# Should return a chronological list of ALL bands in the gig
	@abstractmethod
	def getBands(self):
		pass

	# Should build, store, and return the list of all gigs as Gig objects
	@abstractmethod
	def getGigs(self):
		pass
