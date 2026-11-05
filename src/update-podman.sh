#!/bin/bash
# Scrape every venue in every city and write ../site/data/<city>/shows.json, then run ../start.sh to publish
/opt/homebrew/bin/podman build -t ears-rip-update .
/opt/homebrew/bin/podman run -v /etc/localtime:/etc/localtime:ro -v ./../tmp:/usr/src/tmp -v ./../site:/usr/src/site -t --rm --name ears-rip-updating ears-rip-update
