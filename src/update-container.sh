docker build -t ears-rip-update .
docker run -v /etc/localtime:/etc/localtime:ro -v ./cache:/usr/src/app/cache -v ./../tmp:/usr/src/tmp -v ./../.git:/usr/src/.git -v ./../deploy:/usr/src/deploy -it --rm --name ears-rip-updating ears-rip-update

