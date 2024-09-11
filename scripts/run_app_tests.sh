#!/bin/sh
docker run --entrypoint /bin/sh primasre/backend-api -c "poetry run pytest"