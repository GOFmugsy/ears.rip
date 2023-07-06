from urllib.request import urlopen
from Gig import Gig
from Venue import Venue

venues = [ Venue("The Earl", "33.740969965415346, -84.34589730897736", "488 Flat Shoals Ave SE, Atlanta, GA 30316", "https://badearl.com/", "https://badearl.com/"),
	Venue("Bogg's Social & Supply", "33.73754843540693, -84.43040579023476", "1310 White St SW, Atlanta, GA 30310", "https://www.boggssocial.com/", "https://www.boggssocial.com/live-music")
]

def main():
	for venue in venues:
		print("processing: " + venue.name)

if __name__ == "__main__":
	main()
