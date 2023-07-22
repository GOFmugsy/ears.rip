from .. import Venue

class Earl(Venue):
	def __init__(self):
		self.name = "The Earl"
		self.geo = (33.740969965415346, -84.34589730897736)
		self.address = "488 Flat Shoals Ave SE, Atlanta, GA 30316"
		self.url = "https://badearl.com/"
		self.schedule = "https://badearl.com/"
		self.page = urlopen(venue.schedule)
		self.html = page.read().decode("utf-8")
		self.soup = BeautifulSoup(html, "html.parser")

	def getLinks(self):
		links = self.soup.find_all('a', 'cl-element-featured_media__anchor')
		urls = []
		for link in links:
			url = re.search(r"https://badearl.com/show/.*?/", str(link))
			urls.append(url)
		return urls

	def getDates(self):
		datePs = soup.find_all('p', 'show-listing-date')
		dates = []
		
		

