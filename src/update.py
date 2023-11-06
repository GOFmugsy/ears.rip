import re
import pkgutil
import importlib
import dominate
from dominate.tags import *
import datetime

from cities.Venue import Venue
import cities.atl

def main():
	venues = []
	
	# import all modules in city package
	for loader, name, ispkg in pkgutil.walk_packages(cities.atl.__path__):
		mod = importlib.import_module('.' + name, 'cities.atl')

	# instantiate all venue subclasses to list
	print("Fetching and parsing venue information ... ")
	venues = [cls() for cls in Venue.__subclasses__()]

	buildWebsite(venues)

	for venue in venues:
		print(venue.name)
		if venue.name == "529":
			for band in venue.getBands():
				print(band)

def buildWebsite(venues):
	web = dominate.document(title = "EARS.RIP")
	daysInSched = 7
	date = datetime.datetime.now()

	with web.head:
		link(rel='stylesheet', href='css/style.css')

	with web:
		attr(cls='body')

		with div():
			attr(cls='title')
			h1('EARS.RIP')

		with div():
			attr(cls='schedule')
			
			for day in range(daysInSched):
				print(date)

				date += datetime.timedelta(days=1)
				

	with open('../deploy/dev/web/index.html', 'w') as index:
		index.write(str(web))

if __name__ == "__main__":
	main()
