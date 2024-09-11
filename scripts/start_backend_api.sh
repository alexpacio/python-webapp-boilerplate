#!/bin/bash
source ./scripts/build_docker_image.sh
CONT_ID=$(docker ps -a | grep boilerplate_backend_api | awk '{print $1}')
if [ ! -z "$CONT_ID" ]
then
    docker stop $CONT_ID
    docker rm $CONT_ID
fi
source ./scripts/run_app_tests.sh
source ./scripts/start_docker_container_locally.sh