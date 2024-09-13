#!/bin/sh
docker run --env-file .env --entrypoint /bin/sh boilerplate/backend-svc -c "poetry run pytest"