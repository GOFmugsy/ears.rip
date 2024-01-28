#!/usr/bin/python3

import re
import pkgutil
import importlib
import dominate
from dominate.tags import *
import datetime
import git

city = "atl"
disclaimer = "There is absolutely no guarantee of any kind provided with this page or any derivative of this page"

import cities
from cities.Venue import Venue
from cities.Gig import Gig
importlib.import_module('cities.' + city)


def main():
	venues = []
	
	# import all modules in city package
	for loader, name, ispkg in pkgutil.walk_packages(path=['./cities/' + city + '/']):
		mod = importlib.import_module('.' + name, 'cities.' + city)

	# instantiate all venue subclasses to list
	print("Fetching and parsing venue information ... ")
	venues = [cls() for cls in Venue.__subclasses__()]

	buildWebsite(venues)

def buildWebsite(venues):
	web = dominate.document(title = city.upper() + ".EARS.RIP")
	venueList = dominate.document(title = city.upper() + ".EARS.RIP")

	daysInSched = 30
	date = datetime.datetime.now()
	now = datetime.datetime.now()
	repo = git.Repo(search_parent_directories=True)
	sha = repo.head.object.hexsha

	with web.head:
		link(rel='stylesheet', type='text/css', href='/css/style.css')
		link(rel='icon', type='image/x-icon', href='/favicon.ico')

	with venueList.head:
		link(rel='stylesheet', type='text/css', href='/css/style.css')
		link(rel='icon', type='image/x-icon', href='/favicon.ico')

	with web:

		with div():
			attr(cls='title')
			h1(city.upper() + '.EARS.RIP')

		with div():
			attr(cls='nav')
			str(a('shows', href='index.html')) + ' || ' + str(a('venues', href='venues.html'))

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
			str(p(now.strftime("%A, %d. %B %Y %-I:%M%p")))
			str(p(sha))

	with venueList:
		attr(cls='body')

		with div():
			attr(cls='title')
			h1(city.upper() + '.EARS.RIP')

		with div():
			attr(cls='nav')
			str(a('shows', href='index.html')) + ' || ' + str(a('venues', href='venues.html'))

		with div():
			attr(cls='schedule')
			with div():
				attr(cls='venueList')
				for venue in venues:
					p(a(venue.name, href=venue.url))

	with open('../deploy/dev/web/index.html', 'w') as index:
		index.write(str(web))

	with open('../deploy/dev/web/venues.html', 'w') as index:
		index.write(str(venueList))
	
	
if __name__ == "__main__":
	main()
