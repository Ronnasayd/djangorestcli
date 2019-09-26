docker build . --tag=poetry
docker run -ti --name=poetry -v "$(pwd)/app:/tmp/app:" poetry /bin/sh
docker rm poetry