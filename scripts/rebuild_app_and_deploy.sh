#!/bin/sh

alias k='kubectl -n python-api '
./scripts/build_docker_image.sh
k rollout restart deploy backend-svc
pkill 'port-forward'
sleep 3
k port-forward service/backend-svc 8000:8000 &
k logs deployment/backend-svc -f