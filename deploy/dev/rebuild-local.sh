COMMIT=$(git rev-parse --short HEAD) docker compose -p "atl-ears-rip-dev" up -d --build
docker image prune -f
