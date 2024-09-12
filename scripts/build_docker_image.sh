#!/bin/sh
docker build -t localhost:32000/backend-api:latest -f ./backend-api/Dockerfile backend-api/
docker push localhost:32000/backend-api:latest
docker build -t localhost:32000/aws-bootstrapper:latest -f ./aws-bootstrapper/Dockerfile aws-bootstrapper/
docker push localhost:32000/aws-bootstrapper:latest