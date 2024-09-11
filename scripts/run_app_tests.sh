#!/bin/sh
docker run --env-file .env --entrypoint /bin/sh boilerplate/backend-api -c "poetry run pytest"