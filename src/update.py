#!/usr/bin/python3

import re
import pkgutil
import importlib
import dominate
from dominate.tags import *
import datetime

from cities.Venue import Venue
import cities.atl

disclaimer = "There is absolutely no guarantee of any kind provided with this page or any derivative of this page"

def main():
	venues = []
	
	# import all modules in city package
	for loader, name, ispkg in pkgutil.walk_packages(cities.atl.__path__):
		mod = importlib.import_module('.' + name, 'cities.atl')

	# instantiate all venue subclasses to list
	print("Fetching and parsing venue information ... ")
	venues = [cls() for cls in Venue.__subclasses__()]

	buildWebsite(venues)

def buildWebsite(venues):
	web = dominate.document(title = "EARS.RIP")
	daysInSched = 30
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
				for venue in venues:
					for gig in venue.getGigs():
						if gig.doors.date() == date.date():
							with div():
								attr(cls='gig')
								with div():
									attr(cls='bands')
									h4(a(gig.bands, href=gig.url))
								with div():
									attr(cls='info')
									str(a(venue.name, href=venue.url)) + str(p(' || ' + gig.cost + ' || ' + str(gig.doors.strftime("%A, %d. %B %Y %-I:%M%p"))))

				date += datetime.timedelta(days=1)

		with div():
			attr(cls='footer')
			str(p(disclaimer))
				

	with open('../deploy/dev/web/index.html', 'w') as index:
		index.write(str(web))

if __name__ == "__main__":
	main()
