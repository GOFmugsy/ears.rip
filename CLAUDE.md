# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

ears.rip lists every live music show in a city on one static site per city. Python scrapers pull each venue's schedule, Hugo renders the site with the [risotto](https://github.com/joeroe/risotto) theme, and the result is served by nginx behind Traefik. Each city has a three letter code (`atl` Atlanta, `avl` Asheville), its own `<code>.ears.rip` site, and its own nginx container.

## Commands

There are no tests or linters. Verify changes by scraping, building, and looking at the output.

```sh
git submodule update --init                # fetch the risotto theme (site/themes/risotto) on a fresh clone

# Scrape venues -> site/data/<city>/shows.json. Must run from src/ (paths are relative), and ../tmp must exist.
cd src && python3 update.py                # every city; deps: pip install -r requirements.txt
cd src && python3 update.py avl            # just one city
cd src && ./update-container.sh            # same, in a container (update-podman.sh for podman)

# Try one venue scraper
cd src && python3 -c "from cities.atl.earl import Earl; v = Earl(); print(len(v.gigs)); print(v.gigs[0])"

# Site. Every hugo command needs --environment <city> (or landing, for the ears.rip page); without it the site builds with no shows.
cd site && hugo server --environment atl                     # local preview
cd site && hugo --environment atl --minify -d /tmp/public    # full build; check the page count isn't ~8

# Hosting stack (traefik, nginx site, prometheus, grafana)
./start.sh          # prod
./start.sh dev      # dev: HTTP only, root-relative URLs, answers on localhost / *.ears.rip.local
```

## Architecture

```
src/update.py ──> site/data/<city>/shows.json ──> Hugo --environment <city> ──> <city>-ears-rip nginx image ──> Traefik (<city>.ears.rip)
```

### Scraping (`src/`)
- Each city is a package `src/cities/<code>/` whose `__init__.py` sets `timezone`. `update.py` treats every package in `cities/` as a city.
- Each venue is a `Venue` subclass in `src/cities/<city>/`. Its `__init__` sets `name`, `geo`, `address`, `url`, `schedule`, then does `self.soup = self.getPage()` and `self.gigs = self.fetchGigs()`. Scraping happens in the constructor.
- `update.py` imports every module in the city's folder (`pkgutil.walk_packages`) and runs that city's `Venue.__subclasses__()`, filtered by module path so cities don't mix. Any `.py` file in the folder runs whether or not `__init__.py` imports it, which is why disabled or retired scrapers are moved to `src/parse-stash/`.
- Venues that list shows at other venues filter them out (Masquerade by stage, The Orange Peel keeps itself and Pulp but skips Hellbender).
- Some venue sites omit the year from dates. Infer it (see `OrangePeel.inferDate`, which matches the weekday); don't hardcode a year.
- `Venue.getPage()` / `getJSON()` cache responses in `../tmp/<venue name>.html|.json` for 23 hours. Delete the cache file to force a refetch while working on a scraper.
- Scrapers produce naive local `datetime`s for `Gig.doors`. `update.py` attaches the city's timezone, keeps only the next 30 days (`daysInSched`), and writes `shows.json`.
- `Gig.uid` is a deterministic hash of doors/url/bands. It becomes the show's URL path and the calendar UID, so it must stay stable between runs (calendar subscribers would otherwise get duplicates).
- Python files are indented with tabs.

### Site (`site/`)
- Config is `site/config/_default/hugo.toml` (shared) plus `site/config/<city>/hugo.toml` (title, baseURL, timezone, `cityName`), selected with `--environment <city>`. Each city config mounts `data/<city>/` as Hugo's data directory, so templates read `hugo.Data.shows` without knowing the city.
- `site/data/<city>/shows.json` is generated and gitignored. Without it that city builds with no shows.
- `site/config/landing/` is not a city: it builds the ears.rip landing page (home page only, `params.landing = true`). `_partials/cities.html` lists every `config/<dir>/hugo.toml` that sets `params.city`, with show counts from `data/<city>/shows.json` (the landing build has no data mount, so it sees every city's data). Skip `landing` and `_default` anywhere that loops over cities.
- Links between the landing page and cities use `params.homeURL` and `params.cityURL` (a `%s` format for the code). They default to the prod hostnames; the dev Dockerfile overrides both with `HUGO_PARAMS_*` env vars. Each city's "all cities" nav link comes from the overridden `_partials/header.html`.
- Content is shared by every city. Use `site.Params.cityName` (or `{{< param "cityName" >}}` in markdown) instead of naming a city.
- `content/shows/_content.gotmpl` is a Hugo content adapter that creates one page per show from `hugo.Data.shows`. Taxonomies `venues` and `dates` (configured in `hugo.toml`) produce the per-venue and per-day pages.
- `buildFuture = true` is required: every show is dated in the future, so Hugo would otherwise silently drop them all.
- Venue details (address, url, geo) are not on show pages. Templates look them up by venue name via `_partials/venue.html`.
- Link to a show's venue with `range .GetTerms "venues"` → `.RelPermalink`. Don't build `/venues/<urlize name>/` by hand: Hugo's term slugs differ for names with punctuation (`Boggs Social & Supply` → `boggs-social--supply`).
- Calendar (`.ics`) output uses Hugo's built-in `calendar` output format for home, terms, and show pages. `_partials/ics/calendar.ics` builds the file and handles RFC 5545 escaping, 70-char line folding, and CRLF line endings. Times are emitted in UTC.
- Project layouts use Hugo's 0.146+ template system (`layouts/_partials/`, `home.html`, `<section>/page.html`, `<taxonomy>/term.html`). The theme still uses the old `_default/` structure, and project files override it. Use `hugo.Data`, not the deprecated `site.Data`. Theme CSS overrides go in `site/assets/css/custom.css`.
- The footer's build commit comes from the `HUGO_PARAMS_COMMIT` env var.

### Deploy (`deploy/dev`, `deploy/prod`)
- dev and prod are near-duplicate copies (compose file, `Dockerfile.nginx`, `web/nginx.conf`). Change both unless the change is environment-specific.
- Each city is a compose service (`atl-ears-rip`, `avl-ears-rip`), and the landing page is `ears-rip` (`CITY: landing`, `BASE_URL: https://ears.rip/` in prod), built from the same `Dockerfile.nginx` with a `CITY` build arg, plus its own nginx-prometheus-exporter listed in `web/prometheus.yml`. The nginx image is a multi-stage build: `ghcr.io/gohugoio/hugo` (pinned version) builds `site/` for that city, then nginx serves the output. The compose build context is the repo root (`context: ../..`), filtered by the root `.dockerignore`. `BASE_URL` is `/` for dev and defaults to `https://<city>.ears.rip/` for prod.
- Show data only goes live when the nginx image is rebuilt (`start.sh`).
- Traefik must stay on v3.6+ (v2 cannot talk to Docker Engine 29's API, which leaves every route as a 404). v3 rule syntax is one host per matcher: `` Host(`a`) || Host(`b`) ``.
- Prod Traefik routes by hostname only (`ears.rip` to the landing page, `atl.ears.rip`, `avl.ears.rip`, `grafana.*`), so requests by IP get a 404. Dev uses `<city>.ears.rip.local`, and `ears.rip.local` / `localhost` go to the landing page.
- The compose project is still named `atl-ears-rip-<env>` (`start.sh`). Renaming it would start a duplicate stack whose fixed `container_name`s clash with the running one.
- Let's Encrypt certs are persisted in the `traefik-acme` volume. Don't use `compose down -v` or anything else that recreates that volume: re-requesting certs quickly hits Let's Encrypt's 5-duplicate-certs-per-week limit.
- The grafana compose volume `grafana-data` is external. `start.sh` creates it if it is missing.
- Files in `deploy/*/web/` other than `nginx.conf` and `prometheus.yml` (old `*.html`, `events-ics/`) are leftovers from the pre-Hugo generator and are ignored.

### Adding a city
Follow the README's "Adding a City" checklist: city package with `timezone`, `site/config/<code>/hugo.toml`, a compose service and exporter in both dev and prod, prometheus target, and DNS for `<code>.ears.rip` before deploying to prod.

## Known issues
`src/todo` tracks broken scrapers. At the time of writing, Star Community Bar returns 2024 dates and Aisle 5 is blocked by a Cloudflare challenge.
