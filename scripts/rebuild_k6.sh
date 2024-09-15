#!/bin/sh

# usage: rebuild-k6.sh <image-registry-socket-addr>

set -e
docker build -t $1/backend-svc-k6:latest -f ./k6/Dockerfile k6/
docker push $1/backend-svc-k6:latest