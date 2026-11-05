import hashlib

class Gig:
	def __init__(self, bands, doors, url):
		self.bands = bands
		self.doors = doors
		self.url = url
		# Stable across runs so page URLs and calendar UIDs don't change every night
		key = doors.isoformat() + '|' + url + '|' + bands
		self.uid = doors.strftime('%Y-%m-%d') + '-' + hashlib.sha1(key.encode()).hexdigest()[:10]

	def __str__(self):
		return r"bands: " + self.bands + "\ndoors: " + str(self.doors) + "\nurl: " + self.url + "\n"
