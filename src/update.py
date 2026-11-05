#!/usr/bin/python3
#
# usage: python3 update.py [city ...]
# Scrapes every venue in each city (default: every package in cities/) and writes
# ../site/data/<city>/shows.json for hugo to build that city's site from.

import datetime
import importlib
import json
import os
import pkgutil
import sys
from zoneinfo import ZoneInfo

daysInSched = 30
dataDir = '../site/data'

import cities
from cities.Venue import Venue
from cities.Gig import Gig

def main():
	failed = []
	for city in sys.argv[1:] or allCities():
		# one city's broken scraper shouldn't stop the other cities from updating
		try:
			updateCity(city)
		except Exception as e:
			print("ERROR updating " + city + ": " + repr(e))
			failed.append(city)
	if failed:
		sys.exit("failed: " + ", ".join(failed))

# every package in cities/ is a city, named by its three letter code
def allCities():
	return sorted(name for loader, name, ispkg in pkgutil.iter_modules(['./cities']) if ispkg)

def updateCity(city):
	package = importlib.import_module('cities.' + city)

	# import all modules in city package
	for loader, name, ispkg in pkgutil.walk_packages(path=['./cities/' + city + '/']):
		mod = importlib.import_module('.' + name, 'cities.' + city)

	# instantiate this city's venue subclasses to list
	print("Fetching and parsing venue information for " + city + " ... ")
	venues = [cls() for cls in Venue.__subclasses__() if cls.__module__.startswith('cities.' + city + '.')]

	# Run report
	for venue in venues:
		print(venue.name + ":")
		print("\tgigs: " + str(len(venue.gigs)))

	writeData(city, ZoneInfo(package.timezone), venues)

# Write every venue and upcoming gig to a JSON file that hugo builds the site from
def writeData(city, timezone, venues):
	now = datetime.datetime.now(timezone)
	start = datetime.datetime.combine(now.date(), datetime.time())
	end = start + datetime.timedelta(days = daysInSched)

	data = {
		'city': city,
		'generated': now.isoformat(),
		'venues': [],
		'shows': [],
	}

	for venue in venues:
		geo = getattr(venue, 'geo', None)
		data['venues'].append({
			'name': venue.name,
			'address': venue.address,
			'url': venue.url,
			'geo': [float(g) for g in geo] if geo else None,
		})

		for gig in venue.gigs:
			if not start <= gig.doors < end:
				continue
			data['shows'].append({
				'id': gig.uid,
				'bands': gig.bands.strip(),
				'venue': venue.name,
				'doors': gig.doors.replace(tzinfo = timezone).isoformat(),
				'url': gig.url if gig.url.startswith('http') else None,
			})

	data['shows'].sort(key = lambda s: s['doors'])

	dataFile = os.path.join(dataDir, city, 'shows.json')
	os.makedirs(os.path.dirname(dataFile), exist_ok = True)
	with open(dataFile, 'w') as f:
		json.dump(data, f, indent = 1)
	print("wrote " + str(len(data['shows'])) + " shows to " + dataFile)

if __name__ == "__main__":
	main()
