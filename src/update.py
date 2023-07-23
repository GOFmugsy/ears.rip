from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from Gig import Gig
from Venue import Venue

def main():
	for venue in venues:
		print("processing: " + venue.name)
		page = urlopen(venue.schedule)
		html = page.read().decode("utf-8")
		soup = BeautifulSoup(html, "html.parser")

		links = soup.find_all('a', 'cl-element-featured_media__anchor')
		dates = soup.find_all('p', 'show-listing-date')
		bands = soup.find_all('div', re.compile('show-listing-headliner|show-listing-support'))
		for link in links:
			url = re.search(r"https://badearl.com/show/.*?/", str(link))
			print(url.group())
		for date in dates:
			print(date)
		for band in bands:
			print(band)
		print('Number of show links: ' + str(len(links)))
		print('Number of dates: ' + str(len(dates)))
		print('bands: ' + str(len(bands)))
		

if __name__ == "__main__":
	main()
