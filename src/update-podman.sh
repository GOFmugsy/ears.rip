#!/bin/bash
# Scrape every venue and write ../site/data/shows.json, then run deploy/*/rebuild-local.sh to publish
/opt/homebrew/bin/podman build -t ears-rip-update .
/opt/homebrew/bin/podman run -v /etc/localtime:/etc/localtime:ro -v ./../tmp:/usr/src/tmp -v ./../site:/usr/src/site -t --rm --name ears-rip-updating ears-rip-update
