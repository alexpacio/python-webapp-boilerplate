#!/bin/sh
docker run --entrypoint /bin/sh boilerplate/backend-api -c "poetry run pytest"