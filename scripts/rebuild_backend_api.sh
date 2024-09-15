#!/bin/sh

# usage: rebuild_backend_api.sh <k8s-namespace> <image-registry-socket-addr>

alias k="kubectl -n $1"
docker build -t $2/backend-svc:latest -f ./backend-svc/Dockerfile backend-svc/
docker push $2/backend-svc:latest
k rollout restart deploy backend-svc
sleep 3
k port-forward service/backend-svc 8000:8000 &
k logs deployment/backend-svc -f