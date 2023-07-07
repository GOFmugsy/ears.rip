from urllib.request import urlopen
from bs4 import BeautifulSoup
from Gig import Gig
from Venue import Venue

venues = [ Venue("The Earl", "33.740969965415346, -84.34589730897736", "488 Flat Shoals Ave SE, Atlanta, GA 30316", "https://badearl.com/", "https://badearl.com/"),
	# Venue("Bogg's Social & Supply", "33.73754843540693, -84.43040579023476", "1310 White St SW, Atlanta, GA 30310", "https://www.boggssocial.com/", "https://www.boggssocial.com/live-music")
]

def main():
	for venue in venues:
		print("processing: " + venue.name)
		page = urlopen(venue.schedule)
		html = page.read().decode("utf-8")
		soup = BeautifulSoup(html, "html.parser")

		links = soup.find_all('a', 'cl-element-featured_media__anchor')
		dates = soup.find_all('p', 'show-listing-date')
		headliners = soup.find_all('div', 'show-listing-headliner')
		for link in links:
			print(link)
		for date in dates:
			print(date)
		for band in headliners:
			print(band)
		print('Number of show links: ' + str(len(links)))
		print('Number of dates: ' + str(len(dates)))
		

if __name__ == "__main__":
	main()
