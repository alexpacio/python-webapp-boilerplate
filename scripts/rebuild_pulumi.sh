#!/bin/sh

# usage: rebuild_pulumi.sh <k8s-namespace> <image-registry-socket-addr>

alias k="kubectl -n $1"
docker build -t $2/pulumi:latest -f ./pulumi/Dockerfile pulumi/
docker push $2/pulumi:latest
k rollout restart deploy pulumi
sleep 3
k logs job.batch/pulumi-job -f