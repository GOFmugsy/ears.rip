import datetime

class Gig:
	def __init__(self, bands, doors, url, cost):
		self.bands = bands
		self.doors = doors
		self.url = url
		self.cost = cost

	def __str__(self):
		return r"bands: " + self.bands + "\ndoors: " + str(self.doors) + "\nurl: " + self.url + "\ncost: " + self.cost + "\n"

	def getHTML(self):
		return r" "
		
