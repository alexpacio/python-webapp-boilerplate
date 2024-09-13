#!/bin/sh
docker run --env-file .env --entrypoint /bin/sh localhost:32000/backend-svc:latest -c "poetry run pytest"