#!/bin/bash
# Scrape every venue and write ../site/data/shows.json, then run deploy/*/rebuild-local.sh to publish
docker build -t ears-rip-update .
docker run -v /etc/localtime:/etc/localtime:ro -v ./../tmp:/usr/src/tmp -v ./../site:/usr/src/site -t --rm --name ears-rip-updating ears-rip-update
