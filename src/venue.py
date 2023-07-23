from abc import ABC, abstractmethod

class Venue(ABC):
	def __init__(self, name, latlong, address, homepage, schedule):
		self.name = name
		self.latlong = latlong
		self.address = address
		self.homepage = homepage
		self.schedule = schedule

	def __str__(self):
		return f" "

	def addGig(self, gig):
		self.gigs.append(gig)

	@abstractmethod
	def getLinks(self):
		pass

	@abstractmethod
	def getDates(self):
		pass
