#!/bin/bash
# Build and start the ears.rip web hosting stack (traefik, nginx site, prometheus, grafana).
#
# usage: ./start.sh [prod|dev]   (default: prod)
#
# Uses docker if its daemon is running, otherwise podman.
# New shows are published by running src/update-container.sh (or update-podman.sh) first.
set -euo pipefail

env="${1:-prod}"
if [[ "$env" != "prod" && "$env" != "dev" ]]; then
	echo "usage: $0 [prod|dev]" >&2
	exit 1
fi

root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$root"

# The hugo theme is a git submodule; fetch it if this is a fresh clone
if [[ ! -f site/themes/risotto/theme.toml ]]; then
	echo "Fetching risotto theme ..."
	git submodule update --init site/themes/risotto
fi

# every city has a site/config/<city>/ hugo config and its scraped shows in site/data/<city>/
for config in site/config/*/; do
	city="$(basename "$config")"
	[[ "$city" == "_default" ]] && continue
	if [[ ! -f "site/data/$city/shows.json" ]]; then
		echo "warning: site/data/$city/shows.json not found, $city.ears.rip will have no shows." >&2
		echo "         run src/update-container.sh (or src/update-podman.sh) to scrape venues." >&2
	fi
done

if docker info >/dev/null 2>&1; then
	runtime=docker
elif command -v podman >/dev/null 2>&1; then
	runtime=podman
else
	echo "error: neither a running docker daemon nor podman was found" >&2
	exit 1
fi
echo "Using $runtime to start atl-ears-rip-$env"

# grafana's data volume is declared external in docker-compose.yml, so it must already exist
if ! "$runtime" volume inspect grafana-data >/dev/null 2>&1; then
	"$runtime" volume create grafana-data >/dev/null
fi

cd "deploy/$env"
COMMIT="$(git rev-parse --short HEAD)" "$runtime" compose -p "atl-ears-rip-$env" up -d --build
"$runtime" image prune -f >/dev/null

echo "atl-ears-rip-$env is up"
