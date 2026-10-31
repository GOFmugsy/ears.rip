#!/usr/bin/python3

import datetime
import importlib
import json
import os
import pkgutil
from zoneinfo import ZoneInfo

city = "atl"
timezone = ZoneInfo("America/New_York")
daysInSched = 30
dataFile = '../site/data/shows.json'

import cities
from cities.Venue import Venue
from cities.Gig import Gig
importlib.import_module('cities.' + city)

def main():
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

	writeData(venues)

# Write every venue and upcoming gig to a JSON file that hugo builds the site from
def writeData(venues):
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
				'cost': gig.cost,
			})

	data['shows'].sort(key = lambda s: s['doors'])

	os.makedirs(os.path.dirname(dataFile), exist_ok = True)
	with open(dataFile, 'w') as f:
		json.dump(data, f, indent = 1)
	print("wrote " + str(len(data['shows'])) + " shows to " + dataFile)

if __name__ == "__main__":
	main()
