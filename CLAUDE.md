# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

ears.rip lists every live music show in a city on one static site (currently only Atlanta: atl.ears.rip). Python scrapers pull each venue's schedule, Hugo renders the site with the [risotto](https://github.com/joeroe/risotto) theme, and the result is served by nginx behind Traefik. The intent is one deployment per city.

## Commands

There are no tests or linters. Verify changes by scraping, building, and looking at the output.

```sh
git submodule update --init                # fetch the risotto theme (site/themes/risotto) on a fresh clone

# Scrape venues -> site/data/shows.json. Must run from src/ (paths are relative), and ../tmp must exist.
cd src && python3 update.py                # deps: pip install -r requirements.txt
cd src && ./update-container.sh            # same, in a container (update-podman.sh for podman)

# Try one venue scraper
cd src && python3 -c "from cities.atl.earl import Earl; v = Earl(); print(len(v.gigs)); print(v.gigs[0])"

# Site
cd site && hugo server                     # local preview
cd site && hugo --minify -d /tmp/public    # full build; check the page count is in the hundreds, not ~8

# Hosting stack (traefik, nginx site, prometheus, grafana)
./start.sh          # prod
./start.sh dev      # dev: HTTP only, root-relative URLs, answers on localhost / *.ears.rip.local
```

## Architecture

```
src/update.py ──> site/data/shows.json ──> Hugo (site/) ──> nginx image (deploy/<env>/Dockerfile.nginx) ──> Traefik
```

### Scraping (`src/`)
- Each venue is a `Venue` subclass in `src/cities/<city>/`. Its `__init__` sets `name`, `geo`, `address`, `url`, `schedule`, then does `self.soup = self.getPage()` and `self.gigs = self.fetchGigs()`. Scraping happens in the constructor.
- `update.py` discovers venues with `Venue.__subclasses__()` after importing the city package. A venue only runs if it is imported in `cities/<city>/__init__.py`. Disabled or retired scrapers live in `src/parse-stash/`.
- `Venue.getPage()` / `getJSON()` cache responses in `../tmp/<venue name>.html|.json` for 23 hours. Delete the cache file to force a refetch while working on a scraper.
- Scrapers produce naive local `datetime`s for `Gig.doors`. `update.py` attaches America/New_York, keeps only the next 30 days (`daysInSched`), and writes `shows.json`.
- `Gig.uid` is a deterministic hash of doors/url/bands. It becomes the show's URL path and the calendar UID, so it must stay stable between runs (calendar subscribers would otherwise get duplicates).
- Python files are indented with tabs.

### Site (`site/`)
- `site/data/shows.json` is generated and gitignored. Without it the site builds with no shows.
- `content/shows/_content.gotmpl` is a Hugo content adapter that creates one page per show from `hugo.Data.shows`. Taxonomies `venues` and `dates` (configured in `hugo.toml`) produce the per-venue and per-day pages.
- `buildFuture = true` is required: every show is dated in the future, so Hugo would otherwise silently drop them all.
- Venue details (address, url, geo) are not on show pages. Templates look them up by venue name via `_partials/venue.html`.
- Templates build venue links as `/venues/<urlize name>/`, which must match Hugo's taxonomy term URLs.
- Calendar (`.ics`) output uses Hugo's built-in `calendar` output format for home, terms, and show pages. `_partials/ics/calendar.ics` builds the file and handles RFC 5545 escaping, 70-char line folding, and CRLF line endings. Times are emitted in UTC.
- Project layouts use Hugo's 0.146+ template system (`layouts/_partials/`, `home.html`, `<section>/page.html`, `<taxonomy>/term.html`). The theme still uses the old `_default/` structure, and project files override it. Use `hugo.Data`, not the deprecated `site.Data`. Theme CSS overrides go in `site/assets/css/custom.css`.
- The footer's build commit comes from the `HUGO_PARAMS_COMMIT` env var.

### Deploy (`deploy/dev`, `deploy/prod`)
- dev and prod are near-duplicate copies (compose file, `Dockerfile.nginx`, `web/nginx.conf`). Change both unless the change is environment-specific.
- The nginx image is a multi-stage build: `ghcr.io/gohugoio/hugo` (pinned version) builds `site/`, then nginx serves the output. The compose build context is the repo root (`context: ../..`), filtered by the root `.dockerignore`. `BASE_URL` is `/` for dev and `https://atl.ears.rip/` for prod.
- Show data only goes live when the nginx image is rebuilt (`start.sh`).
- Traefik must stay on v3.6+ (v2 cannot talk to Docker Engine 29's API, which leaves every route as a 404). v3 rule syntax is one host per matcher: `` Host(`a`) || Host(`b`) ``.
- Prod Traefik routes by hostname only (`atl.ears.rip`, `ears.rip`, `grafana.*`), so requests by IP get a 404.
- Let's Encrypt certs are persisted in the `traefik-acme` volume. Don't use `compose down -v` or anything else that recreates that volume: re-requesting certs quickly hits Let's Encrypt's 5-duplicate-certs-per-week limit.
- The grafana compose volume `grafana-data` is external. `start.sh` creates it if it is missing.
- Files in `deploy/*/web/` other than `nginx.conf` and `prometheus.yml` (old `*.html`, `events-ics/`) are leftovers from the pre-Hugo generator and are ignored.

### Single city assumption
"atl" is hardcoded in several places: `city` in `src/update.py`, `site/hugo.toml`, compose project/container names, and Traefik host rules. The README's "Adding a City" section is still empty.

## Known issues
`src/todo` tracks broken scrapers. At the time of writing, Star Community Bar returns 2024 dates and Aisle 5 is blocked by a Cloudflare challenge.
