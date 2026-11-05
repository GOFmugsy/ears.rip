#!/bin/bash
# Scrape every venue in every city and write ../site/data/<city>/shows.json, then run ../start.sh to publish
docker build -t ears-rip-update .
docker run -v /etc/localtime:/etc/localtime:ro -v ./../tmp:/usr/src/tmp -v ./../site:/usr/src/site -t --rm --name ears-rip-updating ears-rip-update
