# ears-rip
Website to provide central location to get all live music shows happening in a city

[ears.rip](http://ears.rip)

### Map
- ears.rip
	- city list
	- city.ears.rip
		- all venues all shows all dates
		- venue list
			- single venue all dates
		- date list
			- single date all venues

Thought process - Each city is deployed as its own container for scaling purposes and to simplify hosting. I don't mind hosting my home town, but someone else should host theirs

### Adding a Venue
- poke around and see if the schedule is coming from a json api to make life easier
- copy a similar venues py file and rename it and the object name
- build specifics into venues py file
- add import to `cities/[city]/__init__.py` file
- run update and build container

### Adding a City
Adding a new city:

### Dependencies and Notes
- Relies on certs from [certbot](https://certbot.eff.org/)
- [Dominate](https://pypi.org/project/dominate/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)
