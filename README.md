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
1. `src/update.py` scrapes every venue in each `src/cities/<city>/` and writes `site/data/<city>/shows.json`
2. `site/` is a [Hugo](https://gohugo.io/) site using the [risotto](https://github.com/joeroe/risotto) theme. `site/content/shows/_content.gotmpl` turns each show in `shows.json` into a page, with `venues` and `dates` taxonomies and an ics calendar for each show, venue, date, and the whole city
3. `deploy/<env>/Dockerfile.nginx` builds one city's Hugo site (`--environment <city>`, which selects `site/config/<city>/hugo.toml`) and copies it into an nginx image. Each city is its own container behind Traefik

Publishing new shows:
```
git submodule update --init      # first time only, fetches the theme
cd src && ./update-container.sh  # or update-podman.sh; scrapes every city
cd .. && ./start.sh              # rebuilds and starts every city's site
```

To preview a city locally: `cd site && hugo server --environment atl`

### Adding a Venue
- poke around and see if the schedule is coming from a json api to make life easier
- copy a similar venues py file and rename it and the object name
- build specifics into venues py file
- add import to `cities/[city]/__init__.py` file
- run update and preview with `hugo server --environment [city]`, then rebuild the container

### Adding a City
Each city is named by a three letter code (e.g. `atl`, `avl`), used for its folders and its `<code>.ears.rip` hostname.
- create `src/cities/[city]/__init__.py` with the city's `timezone` (e.g. `timezone = "America/New_York"`) and add at least one venue
- copy `site/config/atl/hugo.toml` to `site/config/[city]/hugo.toml` and change the code, city name, and timezone
- run update, which writes `site/data/[city]/shows.json`, and preview with `hugo server --environment [city]`
- in both `deploy/dev/docker-compose.yml` and `deploy/prod/docker-compose.yml`, copy the `avl-ears-rip` and `nginx-exporter-avl` services for the new city, and add its exporter to `deploy/*/web/prometheus.yml`
- point DNS for `[city].ears.rip` at the server before deploying to prod, so Let's Encrypt can issue its certificate

### Dependencies and Notes
- [Hugo](https://gohugo.io/) (extended, 0.146 or newer) with the [risotto](https://github.com/joeroe/risotto) theme as a git submodule in `site/themes/risotto`
- TLS certs from Let's Encrypt via [Traefik](https://traefik.io/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)
