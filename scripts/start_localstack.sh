#!/bin/sh
docker run -d --rm --name localstack -it -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack