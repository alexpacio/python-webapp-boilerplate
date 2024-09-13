#!/bin/sh

alias k='kubectl -n python-api '
docker build -t localhost:32000/backend-svc:latest -f ./backend-svc/Dockerfile backend-svc/
docker push localhost:32000/backend-svc:latest
k rollout restart deploy backend-svc
pkill 'port-forward'
sleep 3
k port-forward service/backend-svc 8000:8000 &
k logs deployment/backend-svc -f