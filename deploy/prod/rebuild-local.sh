#!/bin/bash
COMMIT=$(git rev-parse --short HEAD) docker compose -p "atl-ears-rip-prod" up -d --build
docker image prune -f
