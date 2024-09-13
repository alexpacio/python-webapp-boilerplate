#!/bin/sh
docker build -t localhost:32000/backend-svc:latest -f ./backend-svc/Dockerfile backend-svc/
docker push localhost:32000/backend-svc:latest
docker build -t localhost:32000/pulumi:latest -f ./pulumi/Dockerfile pulumi/
docker push localhost:32000/pulumi:latest