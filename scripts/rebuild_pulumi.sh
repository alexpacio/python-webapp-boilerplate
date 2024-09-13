#!/bin/sh

alias k='kubectl -n python-api '
docker build -t localhost:32000/pulumi:latest -f ./pulumi/Dockerfile pulumi/
docker push localhost:32000/pulumi:latest
k rollout restart deploy pulumi
sleep 3
k logs job.batch/pulumi-job -f