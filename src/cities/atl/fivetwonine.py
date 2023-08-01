from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from ..Venue import Venue

class Fivetwonine(Venue):
	def __init__(self):
		self.name = "529"
		self.geo = ('33.739934', '-84.345148')
		self.address = "529 Flat Shoals Ave SE, Atlanta, GA 30316"
		self.url = "https://529atlanta.com/"
		self.schedule = "https://529atlanta.com/calendar/"
		self.page = urlopen(self.schedule)
		self.html = self.page.read().decode("utf-8")
		self.soup = BeautifulSoup(self.html, "html.parser")

	def getLinks(self):
		links = self.soup.find_all('a', 'cl-element-featured_media__anchor')
		urls = []
		for link in links:
			url = re.search(r"https://badearl.com/show/.*?/", str(link))
			urls.append(url)
		return urls

	def getDoors(self):
		# get Dates
		datesH = self.soup.find_all('h1', 'event-date-single')
		dates = []
		for dateH in datesH:
			date = re.search(r"(?<=>)(.*?)(?=<\/)", str(dateH))
			dates.append(date.group())
	
		# get Times
		timesH = self.soup.find_all('p', 'event-meta')
		times = []
		for timeH in timesH:
			time = re.search(r"[0-9]:[0-9][0-9] pm", str(timeH))
			times.append(time.group())

		# combine to get Doors
		doors = []
		for i in range(len(dates)):
			door = dates[i] + " @ " + times[i]
			doors.append(door)
		
		return doors

	def getCost(self):
		pass

	def getDoorCost(self):
		pass
		
	def getBands(self):
		bandsH = self.soup.find_all(re.compile('h[34]'), re.compile('event-headliners|event-bands'))
		bands = []
		for i in range(0, len(bandsH) - 1, 2):
			headliner = re.search(r"(?<=>)(.*?)(?=<)", str(bandsH[i]))
			support = re.search(r"(?<=>)(.*?)(?=<)", str(bandsH[i + 1]))
			bands.append(headliner.group() + " - " + support.group())

		return bands

	def getGigs(self):
		pass


