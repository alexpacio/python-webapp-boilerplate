#!/bin/sh

# usage: build_docker_image.sh <image-registry-socket-addr>

set -e
docker build -t $1/backend-svc:latest -f ./backend-svc/Dockerfile backend-svc/
docker push $1/backend-svc:latest
docker build -t $1/pulumi:latest -f ./pulumi/Dockerfile pulumi/
docker push $1/pulumi:latest
docker build -t $1/backend-svc-k6:latest -f ./k6/Dockerfile k6/
docker push $1/backend-svc-k6:latest