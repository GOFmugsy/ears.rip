#!/usr/bin/python3

import re
import pkgutil
import importlib
import dominate
from dominate.tags import *
import datetime
import icalendar
import git
import os
import uuid

city = "atl"
disclaimer = "There is absolutely no guarantee of any kind provided with this page or any derivative of this page"
aboutStr = ["This website is intentionally simple.",
						"It's purpose is to inform about shows in " + city + " in one location",
						"The list refreshes most nights and is mostly informed by what the venues are posting on their websites"]
daysInSched = 30

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

	# Run report
	for venue in venues:
		print(venue.name + ":")
		print("\tgigs: " + str(len(venue.gigs)))

	buildICSs(venues)
	buildWebsite(venues)

def buildICSs(venues):
	icsdirdev = '../deploy/dev/web/events-ics/'
	icsdirprod = '../deploy/prod/web/events-ics/'
	# Clear old ICS files
	oldICSdev = [ f for f in os.listdir(icsdirdev) if f.endswith(".ics") ]
	for f in oldICSdev:
		os.remove(os.path.join(icsdirdev, f))
	oldICSprod = [ f for f in os.listdir(icsdirprod) if f.endswith(".ics") ]
	for f in oldICSprod:
		os.remove(os.path.join(icsdirprod, f))

	# Build new ICS files
	for venue in venues:
		for gig in venue.gigs:
			cal = icalendar.Calendar()
			e = icalendar.Event()
			# tz = dateutil.tz.tzstr("America/New_York")
			e.add('summary', gig.bands)
			e["X-DT-DATEUTIL"] = icalendar.vDatetime(gig.doors)
			e['location'] = icalendar.vText(venue.name + ' - ' + venue.address)

			cal.add_component(e)

			f = open(icsdirdev + venue.name + '-' + gig.doors.strftime("%m%d%Y-%H:%M") + '.ics', 'wb')
			f.write(cal.to_ical())
			f.close()
			f = open(icsdirprod + venue.name + '-' + gig.doors.strftime("%m%d%Y-%H:%M") + '.ics', 'wb')
			f.write(cal.to_ical())
			f.close()

def buildWebsite(venues):
	web = dominate.document(title = city.upper() + ".EARS.RIP")
	venueList = dominate.document(title = city.upper() + ".EARS.RIP")
	about = dominate.document(title = city.upper() + ".EARS.RIP")

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

	with about.head:
		link(rel='stylesheet', type='text/css', href='/css/style.css')
		link(rel='icon', type='image/x-icon', href='/favicon.ico')

	with web:

		with div():
			attr(cls='title')
			h1(city.upper() + '.EARS.RIP')

		with div():
			attr(cls='nav')
			str(a('shows', href='index.html')) + ' || ' + str(a('venues', href='venues.html')) + ' || ' + str(a('about', href='about.html'))

		with div():
			attr(cls='schedule')
			with table().add(tbody()):
				for day in range(daysInSched):
					gigsToday = 0
					for venue in venues:
						curGigs = venue.getGigsByDate(date)
						if curGigs and len(curGigs) > 0:
							gigsToday += len(curGigs)
					gigCount = 0
					with tr():
						if gigsToday > 0:
							with td():
								attr(cls='date')
								with div():
									str(p(date.strftime("%a").upper()))
									str(p(date.strftime("%B %d")))
						with td():
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
													str(a(venue.name, href=venue.url)) + str(p(' || ' + gig.cost + ' || ' + str(gig.doors.strftime("%-I:%M%p"))))

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
			str(a('shows', href='index.html')) + ' || ' + str(a('venues', href='venues.html')) + ' || ' + str(a('about', href='about.html'))

		with div():
			attr(cls='schedule')
			with div():
				attr(cls='venueList')
				for venue in venues:
					p(a(venue.name, href=venue.url))

		with div():
			attr(cls='footer')
			str(p(disclaimer))
			str(p(now.strftime("%A, %d. %B %Y %-I:%M%p")))
			str(p(sha))

	with about:
		attr(cls='body')

		with div():
			attr(cls='title')
			h1(city.upper() + '.EARS.RIP')

		with div():
			attr(cls='nav')
			str(a('shows', href='index.html')) + ' || ' + str(a('venues', href='venues.html')) + ' || ' + str(a('about', href='about.html'))
			
		with div():
			attr(cls='schedule')
			with div().add(ul()):
				attr(cls='venueList')
				for i in aboutStr:
					li(i)

		with div():
			attr(cls='footer')
			str(p(disclaimer))
			str(p(now.strftime("%A, %d. %B %Y %-I:%M%p")))
			str(p(sha))

	with open('../deploy/dev/web/index.html', 'w') as index:
		index.write(str(web))

	with open('../deploy/dev/web/venues.html', 'w') as venuePage:
		venuePage.write(str(venueList))

	with open('../deploy/dev/web/about.html', 'w') as aboutPage:
		aboutPage.write(str(about))

	with open('../deploy/prod/web/index.html', 'w') as index:
		index.write(str(web))

	with open('../deploy/prod/web/venues.html', 'w') as venuePage:
		venuePage.write(str(venueList))
	
	with open('../deploy/prod/web/about.html', 'w') as aboutPage:
		aboutPage.write(str(about))
	
if __name__ == "__main__":
	main()
