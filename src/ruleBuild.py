import re
import pkgutil
import importlib

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

	for venue in venues:
		print(venue.name)
		if venue.name == "529":
			for band in venue.getBands():
				print(band)

	

if __name__ == "__main__":
	main()
