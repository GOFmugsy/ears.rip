docker build -t ears-rip-update .
docker run -v /etc/localtime:/etc/localtime:ro -v ./cache:/usr/src/app/cache -v ./../tmp:/usr/src/tmp -v ~/.gitconfig:/etc/gitconfig -v ./../.git:/usr/src/.git -v ./../deploy:/usr/src/deploy -v ./events-ics:/usr/src/app/events-ics -it --rm --name ears-rip-updating ears-rip-update

