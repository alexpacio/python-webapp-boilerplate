#!/bin/sh
docker run --env-file .env --name boilerplate_backend_api -p 8000:8000 -t boilerplate/backend-svc