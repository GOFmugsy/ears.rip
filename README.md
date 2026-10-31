# ears-rip
Website to provide central location to get all live music shows happening in a city

[ears.rip](http://ears.rip)

### Map
- ears.rip
	- city list
	- city.ears.rip
		- all venues all shows all dates (`/`, plus `/index.ics` with every show)
		- venue list (`/venues/`)
			- single venue all dates (`/venues/<venue>/`, plus `index.ics`)
		- date list (`/dates/`)
			- single date all venues (`/dates/<yyyy-mm-dd>/`)
		- single show (`/shows/<id>/`, plus `index.ics`)

Thought process - Each city is deployed as its own container for scaling purposes and to simplify hosting. I don't mind hosting my home town, but someone else should host theirs

### How it fits together
1. `src/update.py` scrapes every venue in `src/cities/<city>/` and writes `site/data/shows.json`
2. `site/` is a [Hugo](https://gohugo.io/) site using the [risotto](https://github.com/joeroe/risotto) theme. `site/content/shows/_content.gotmpl` turns each show in `shows.json` into a page, with `venues` and `dates` taxonomies and an ics calendar for each show, venue, date, and the whole city
3. `deploy/<env>/Dockerfile.nginx` builds the Hugo site and copies it into an nginx image

Publishing new shows:
```
git submodule update --init      # first time only, fetches the theme
cd src && ./update-container.sh  # or update-podman.sh
cd ../deploy/prod && ./rebuild-local.sh
```

To preview locally: `cd site && hugo server`

### Adding a Venue
- poke around and see if the schedule is coming from a json api to make life easier
- copy a similar venues py file and rename it and the object name
- build specifics into venues py file
- add import to `cities/[city]/__init__.py` file
- run update and preview with `hugo server`, then rebuild the container

### Adding a City
Adding a new city:

### Dependencies and Notes
- [Hugo](https://gohugo.io/) (extended, 0.146 or newer) with the [risotto](https://github.com/joeroe/risotto) theme as a git submodule in `site/themes/risotto`
- TLS certs from Let's Encrypt via [Traefik](https://traefik.io/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)
